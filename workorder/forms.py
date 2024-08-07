from django import forms
from workorder.models import Asset, Location, Vendor, WorkOrder, WorkOrderRecord, STATUS, STATUS2, CRITICALITY_CHOICES
from users.models import Department, User



class AssetEditForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['code', 'name', 'description', 'status', 'image','location', 'serial_number', 'model', 'manufacturer', 'year', 'parent', 'department_in_charge', 'vendors', 'criticality', 'attachments']
        widgets = {
            'status': forms.Select(choices=STATUS2),
            'location': forms.Select(choices=Location.objects.values_list('name', 'name')),
            'parent': forms.Select(choices=Asset.objects.values_list('name', 'name')),
            'department_in_charge': forms.Select(choices=Department.objects.values_list('name', 'name')),
            'vendors': forms.Select(choices=Vendor.objects.values_list('name', 'name')),
            'criticality': forms.Select(choices=CRITICALITY_CHOICES),
        }

class WorkOrderEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['status','recurrence','title','work_type', 'due_date','assigned_to', 'department_assigned_to','image','description','asset', 'priority', 'attachments', ]
        widgets = {
            'status': forms.Select(choices=STATUS),
            'priority': forms.Select(choices=CRITICALITY_CHOICES),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# form to edit work order record
class WorkOrderRecordEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRecord
        fields = ['status', 'completed_on', 'completed_by', 'comments']
        widgets = {
            'status': forms.Select(choices=STATUS),
            'completed_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'completed_by': forms.Select(choices=User.objects.values_list('username', 'username')),
        }