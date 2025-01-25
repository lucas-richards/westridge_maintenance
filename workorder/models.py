
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
from users.models import Department, User
import datetime as dt

CRITICALITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]

STATUS = [
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('done', 'Done'),
        ('scheduled', 'Scheduled'),
        ('cancelled', 'Cancelled'),
    ]

STATUS2 = [
    ('online', 'Online'),
    ('offline', 'Offline'),
    ('do_not_track', 'Do Not Track'),
    ]

RECURRENCE = [
    ('Once', 'Once'),
    ('Daily', 'Daily'),
    ('Weekly', 'Weekly'),
    ('Monthly', 'Monthly'),
    ('Quarterly', 'Quarterly'),
    ('Biannually', 'Biannually'),
    ('Yearly', 'Yearly'),
    ('3 Years', '3 Years'),
]

NOTIFICATION = [
    ('none', 'None'),
    ('day of event', 'Day Of Event'),
    ('day before', 'Day Before'),
    ('week before', 'Week Before'),
    ('month before', 'Month Before'),
]

# KPI models
class KPI(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class KPIValue(models.Model):
    kpi = models.ForeignKey(KPI, on_delete=models.CASCADE)
    value = models.FloatField()
    date = models.DateField()

    def __str__(self):
        return f"{self.kpi.name} - {self.date}: {self.value}"


# vendor model
class Vendor(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    contact = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

def asset_attachment_path(instance, filename):
    return f'asset_attachments/{instance.code}/{filename}'

class Asset(models.Model):
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS2,
        default='online',
    )
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.CharField(
        max_length=20,
        choices=[
            ('warehouse', 'Warehouse'),
            ('office', 'Office'),
            ('quality lab', 'Quality Lab'),
            ('bulding', 'Building'),
            ('production Line #1', 'Production Line #1'),
            ('production Line #2', 'Production Line #2'),
            ('production Line #3', 'Production Line #3'),
            ('assembly', 'Assembly'),
            ('roof', 'Roof'),
            # Add more choices here
        ],
        null=False,
        blank=False,
        default='office',
    )
    description = models.TextField(null=True, blank=True)
    serial_number = models.CharField(max_length=255, null=True, blank=True)
    model = models.CharField(max_length=255, null=True, blank=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    department_in_charge = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    vendors = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='asset_images/', null=True, blank=True)
    # criticality of the asset with an array of three options low medium and high
    criticality = models.CharField(
        max_length=6,
        choices=CRITICALITY_CHOICES,
        default='medium',
    )
    attachments = models.FileField(upload_to=asset_attachment_path, null=True, blank=True)

    def __str__(self):
        return self.code + ' - ' + self.name 

def workorder_attachment_path(instance, filename):
    return f'asset_attachments/{instance.title}/{filename}'

class WorkOrder(models.Model):
    title = models.CharField(max_length=255)
    priority = models.CharField(
        max_length=20,
        choices=CRITICALITY_CHOICES,
        default='medium',
    )
    description = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorders')
    department_assigned_to = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_workorders')
    created_on = models.DateTimeField(auto_now_add=True)
    first_due_date = models.DateTimeField(default=timezone.now)
    notification = models.CharField(
        max_length=20,
        choices=NOTIFICATION,
        default='none',
    )
    last_updated = models.DateTimeField(auto_now=True)
    recurrence = models.CharField(
        max_length=20,
        choices=RECURRENCE,
        default='Once',
    )
    asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='wo_images/', null=True, blank=True)
    attachments = models.FileField(upload_to=workorder_attachment_path, null=True, blank=True)


    def __str__(self):
        return 'WO' + str(self.id) + '-' + self.title 

    #  when a work order is created, 
    # I want to automatically create a work order record with same due date and assigned to the same person
    def save(self, *args, **kwargs):
        super(WorkOrder, self).save(*args, **kwargs)
        if not self.workorderrecord_set.exists():
            WorkOrderRecord.objects.create(workorder=self, due_date=self.first_due_date, assigned_to=self.assigned_to)

        # workorder date is overdue and the asset is critical update critical kpi if it's not critical update overdue kpi
        kpi = KPI.objects.get(name='Overdue')
        kpi_critical = KPI.objects.get(name='Overdue High Criticality')
        today = timezone.now().date()
        work_order = self
        if work_order.first_due_date.date() < today:
            kpi_value = KPIValue.objects.filter(kpi=kpi, date=today).first()
            kpi_critical_value = KPIValue.objects.filter(kpi=kpi_critical, date=today).first()
            if not kpi_critical_value:
                kpi_value.value += 1
            else:
                kpi_critical_value.value += 1
            kpi_value.save()
            kpi_critical_value.save()
        

    

class WorkOrderRecord(models.Model):
    workorder = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=STATUS,
        default='scheduled',
    )
    created_on = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(default=timezone.now)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_workorders_record')
    completed_on = models.DateTimeField(null=True, blank=True)
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    time_to_complete = models.DurationField(null=True, blank=True)
    attachments = models.FileField(upload_to=f'records', null=True, blank=True)
    comments = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"#{self.id} - {self.workorder.asset} - {self.workorder.title} - {self.due_date}"

    # when saved check how many records are with status done today and update the kpi
    def save(self, *args, **kwargs):
        super(WorkOrderRecord, self).save(*args, **kwargs)
        today = timezone.now().date()
        productivity_value = WorkOrderRecord.objects.filter(status='done', completed_on__date=today).count()
        overdue = WorkOrderRecord.objects.filter(status__in=['in_progress', 'on_hold', 'scheduled'], due_date__lt=today).exclude(workorder__asset__criticality='high').count()
        overdue_high = WorkOrderRecord.objects.filter(status__in=['in_progress', 'on_hold', 'scheduled'], due_date__lt=today, workorder__asset__criticality='high').count()

        kpi_productivity, _ = KPI.objects.get_or_create(name='Productivity')
        kpi_overdue, _ = KPI.objects.get_or_create(name='Overdue')
        kpi_overdue_high, _ = KPI.objects.get_or_create(name='Overdue High Criticality')

        KPIValue.objects.update_or_create(kpi=kpi_productivity, date=today, defaults={'value': productivity_value})
        KPIValue.objects.update_or_create(kpi=kpi_overdue, date=today, defaults={'value': overdue})
        KPIValue.objects.update_or_create(kpi=kpi_overdue_high, date=today, defaults={'value': overdue_high})

class CheckListItem(models.Model):
    workorder_record = models.ForeignKey(WorkOrderRecord, on_delete=models.CASCADE, related_name='checklist_items')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(
        max_length=6,
        choices=[
            ('pass', 'Pass'),
            ('fail', 'Fail'),
            ('flag', 'Flag'),
        ],
        null=True,
        blank=True,
        )
    due_date = models.DateTimeField(default=timezone.now)
    attachments = models.FileField(upload_to=f'records', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
            
class PurchasePart(models.Model):
    workorder_record = models.ForeignKey(WorkOrderRecord, on_delete=models.CASCADE, related_name='purchase_parts')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    purchased = models.BooleanField(default=False)
    eta = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
            

class ProdItemStd(models.Model):
    sku = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)
    kind = models.CharField(
        max_length=20,
        choices=[
            ('tube', 'Tube'),
            ('foil', 'Foil'),
            ('bottle', 'Bottle'),
            ('replenishment', 'Replenishment'),
        ],
        null=False,
        blank=False,
        default='bottle',
    )
    pph = models.IntegerField(null=True, blank=True)
    formula = models.CharField(
        max_length=255,
        choices=[
            ('glide', 'Glide'),
            ('silicone A', 'Silicone A'),
            ('free', 'Free'),
            ('sanitaizer A', 'Sanitaizer A'),
            ('t-glide', 'T-Glide'),
        ],
        null=True,
        blank=True,

    )
    people_inline = models.FloatField(null=True, blank=True)
    setup_time = models.FloatField(null=True, blank=True)
    setup_people = models.IntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='prod_item_images/', null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.sku + ' - ' + self.description

class ProdItem(models.Model):
    item = models.ForeignKey(ProdItemStd, on_delete=models.CASCADE)
    qty_produced = models.IntegerField(null=True, blank=True)
    people_inline = models.FloatField(null=True, blank=True)
    produced_time = models.FloatField(null=True, blank=True)
    setup_time = models.FloatField(null=True, blank=True)
    setup_people = models.IntegerField(null=True, blank=True)
    completed_date = models.DateTimeField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return str(self.completed_date) + ' - ' + self.item.sku + ' - ' + self.item.description

    
        


class DayProductivity(models.Model):
    date = models.DateField()
    people = models.IntegerField(null=True, blank=True)
    extra_hours = models.FloatField(null=True, blank=True)
    earned_hours = models.FloatField(null=True, blank=True)
    total_produced_tube = models.IntegerField(null=True, blank=True)
    total_produced_foil = models.IntegerField(null=True, blank=True)
    total_produced_bottle = models.IntegerField(null=True, blank=True)
    total_produced_replenishment = models.IntegerField(null=True, blank=True)
    productivity_tube = models.FloatField(null=True, blank=True)
    productivity_foil = models.FloatField(null=True, blank=True)
    productivity_bottle = models.FloatField(null=True, blank=True)
    productivity_replenishment = models.FloatField(null=True, blank=True)
    productivity = models.FloatField(null=True, blank=True)
    total_produced = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return str(self.date)