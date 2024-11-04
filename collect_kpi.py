import os
import django


# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_projects.settings')
django.setup()

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import date
from training.models import KPI, KPIValue, Profile, TrainingEvent, TrainingModule, ProfileTrainingEvents
from workorder.models import WorkOrder, WorkOrderRecord, KPI as KPI2, KPIValue as KPIValue2, CheckListItem, PurchasePart
import datetime as dt
from django.utils import timezone

class Command(BaseCommand):
    help = 'Calculate and save daily KPI values'
    
    def save_kpi(self, kpi_name, value):
        kpi, created = KPI.objects.get_or_create(name=kpi_name)
        today = timezone.now().date()
        KPIValue.objects.update_or_create(
            kpi=kpi,
            date=today,
            defaults={'value': value}
        )

    def save_kpi2(self, kpi_name, value):
        kpi, created = KPI2.objects.get_or_create(name=kpi_name)
        today = timezone.now().date()
        KPIValue2.objects.update_or_create(
            kpi=kpi,
            date=today,
            defaults={'value': value}
        )

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        profiles = Profile.objects.all()
        active_profiles = profiles.filter(active=True)
        training_modules = TrainingModule.objects.filter(other=False).order_by('name')

        training = {
            'performed': 0,
            'not_performed': 0,
            'total': 0
        }
        retraining = {
            'performed': 0,
            'overdue': 0,
            'not_performed': 0,
            'total': 0
        }
        profiles_fully_trained = 0
        training_not_performed_users = []
        retraining_not_performed_users = []
        retraining_overdue_users = []

        for profile in active_profiles:
            try:
                profile_training_events = ProfileTrainingEvents.objects.filter(profile=profile).first()
                training_events_now = profile_training_events.row.split(',')
                fully_trained = True

                for i, training_module in enumerate(training_modules):
                    if training_events_now[i] == '-':
                        continue
                    elif training_events_now[i][0] == 'T':
                        fully_trained = False
                        if training_module.retrain_months:
                            retraining['total'] += 1
                            retraining['not_performed'] += 1
                            retraining_not_performed_users.append(profile.user)
                        else:
                            training['total'] += 1
                            training['not_performed'] += 1
                            training_not_performed_users.append(profile.user)
                        continue

                    try:
                        parsed_date = dt.datetime.strptime(training_events_now[i], '%m/%d/%y')
                        current_date = dt.datetime.now()
                        delta = current_date - parsed_date
                        months_difference = delta.days // 30

                        if training_module.retrain_months:
                            if months_difference > training_module.retrain_months:
                                retraining['overdue'] += 1
                                fully_trained = False
                                retraining_overdue_users.append(profile.user)
                            else:
                                retraining['performed'] += 1
                            retraining['total'] += 1
                        else:
                            training['performed'] += 1
                            training['total'] += 1

                    except ValueError:
                        continue
            except:
                print('Error for:', profile.user.username)
                continue

            if fully_trained:
                profiles_fully_trained += 1

        perc_fully_trained = round(profiles_fully_trained / active_profiles.count() * 100) if active_profiles.count() else 0
        training_not_performed_users = list(set(training_not_performed_users))
        retraining_not_performed_users = list(set(retraining_not_performed_users))
        retraining_overdue_users = list(set(retraining_overdue_users))

        training['performed'] = round(training['performed'] / training['total'] * 100) if training['total'] else 0
        retraining['performed'] = round(retraining['performed'] / retraining['total'] * 100) if retraining['total'] else 0
        retraining['overdue'] = round(retraining['overdue'] / retraining['total'] * 100) if retraining['total'] else 0
        training['not_performed'] = round(training['not_performed'] / training['total'] * 100) if training['total'] else 0
        retraining['not_performed'] = round(retraining['not_performed'] / retraining['total'] * 100) if retraining['total'] else 0

        self.save_kpi('Training Performed', training['performed'])
        self.save_kpi('Retraining Performed', retraining['performed'])
        self.save_kpi('Retraining Overdue', retraining['overdue'])
        self.save_kpi('Training Not Performed', training['not_performed'])
        self.save_kpi('Retraining Not Performed', retraining['not_performed'])
        self.save_kpi('Percentage Fully Trained', perc_fully_trained)
        
        self.stdout.write(self.style.SUCCESS('Successfully saved daily training KPI values'))


        
        # Maintenance APP
        # schedule a work order record according to the recurrence and if the last work order record is done or cancelled
        work_orders = WorkOrder.objects.all()
        for work_order in work_orders:
            last_work_order_record = work_order.workorderrecord_set.last()
            if last_work_order_record:
                print('last_work_order_record:', last_work_order_record, work_order.recurrence)
                if last_work_order_record.status in ['done', 'cancelled']:
                    if work_order.recurrence == 'Daily':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=1))
                    elif work_order.recurrence == 'Weekly':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=7))
                    elif work_order.recurrence == 'Monthly':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=30))
                    elif work_order.recurrence == 'Quarterly':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=90))
                    elif work_order.recurrence == 'Biannually':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=180))
                    elif work_order.recurrence == 'Yearly':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=365))
                    elif work_order.recurrence == '3 Years':
                        new = WorkOrderRecord.objects.create(workorder=work_order, due_date=timezone.now() + dt.timedelta(days=1095))
                    
                    if last_work_order_record.checklist_items.exists():
                        for item in last_work_order_record.checklist_items.all():
                            item_data = {
                                'workorder_record': new,
                                'title': item.title,
                                'description': item.description,
                                'status': '',  # Set the status to empty
                                # Add any other fields that need to be copied
                            }
                            new_checklist = CheckListItem.objects.create(**item_data)
                            print('new_checklist:', new_checklist)
                            print('new record:', new)

                    #  if last record purchase parts exist add them to the new record
                    if last_work_order_record.purchase_parts.exists():
                        for part in last_work_order_record.purchase_parts.all():
                            part_data = {
                                'workorder_record': new,
                                'title': part.title,
                                'description': part.description,
                                # Add any other fields that need to be copied
                            }
                            new_part = PurchasePart.objects.create(**part_data)
                            print('new_part:', new_part)
                            print('new record:', new)

            else:
                WorkOrderRecord.objects.create(work_order=work_order, due_date=timezone.now())


        # get the last record or each work order and check for those with status different from done and cancelled if they are overdue by checking if the due date is later than today
        work_orders = WorkOrder.objects.all()
        overdue = 0
        for work_order in work_orders:
            last_work_order_record = work_order.workorderrecord_set.last()
            if last_work_order_record and last_work_order_record.status not in ['done', 'cancelled'] and last_work_order_record.due_date.date() < timezone.now().date():
                overdue += 1
        # save to over due kpi
        self.save_kpi2('Overdue', overdue)
        print('overdue:', overdue)


        # if there are no work orders records for today, then set the productivity kpi value to 0
        
        work_order_records_today = WorkOrderRecord.objects.filter(completed_on=today).count()
        self.save_kpi2('Productivity', work_order_records_today)

        # count how many work order records have status done and create a kpivalue with that number
        value = WorkOrderRecord.objects.filter(status='done').count()
        self.save_kpi2('Status Done', value)

        #  count how many work orders have the last work order record are on time and create a kpivalue with that number in timing kpi
        work_orders_records = WorkOrderRecord.objects.all()
        on_time = round(work_orders_records.filter(due_date__gte=timezone.now()).exclude(status__in=['done', 'cancelled']).count(), 0)
        work_orders_excluding = work_orders_records.exclude(status__in=['done', 'cancelled'])

        #  get percentage rounded to 0 decimals
        percentage = round(on_time / work_orders_excluding.count() * 100) if work_orders_excluding.count() else 0
        self.save_kpi2('Timing On Time', percentage)

        self.stdout.write(self.style.SUCCESS('Successfully saved daily maintenance KPI values'))

                    

# Call the function to calculate and save daily KPI values
if __name__ == '__main__':
    Command().handle()

