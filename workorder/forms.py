from django import forms
from workorder.models import Asset, Vendor, WorkOrder, WorkOrderRecord, STATUS, STATUS2, CRITICALITY_CHOICES, ProdItemStd, ProdItem, DayProductivity
from users.models import Department, User



class AssetEditForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name','location', 'description', 'status', 'image', 'serial_number', 'model', 'manufacturer', 'year', 'department_in_charge', 'criticality', 'attachments']
        widgets = {
            'status': forms.Select(choices=STATUS2),
            'location': forms.Select(choices=Asset.objects.values_list('location', 'location')),
            'parent': forms.Select(choices=Asset.objects.values_list('name', 'name')),
            'department_in_charge': forms.Select(choices=Department.objects.values_list('name', 'name')),
            'vendors': forms.Select(choices=Vendor.objects.values_list('name', 'name')),
            'criticality': forms.Select(choices=CRITICALITY_CHOICES),
            'name': forms.TextInput(attrs={'placeholder': 'Example: Automatic Filling Machine 4-nozzles'}),
            'description': forms.Textarea(attrs={'placeholder': 'Example: This machine is used to fill bottles automatically. It is setup in Line 1 and only runs with Glide'}),
            'serial_number': forms.TextInput(attrs={'placeholder': 'Example: 123456'}),
            'model': forms.TextInput(attrs={'placeholder': 'Example: mty-123'}),
            'manufacturer': forms.TextInput(attrs={'placeholder': 'Who made this machine? or who service this machine?'}),
            'year': forms.NumberInput(attrs={'placeholder': 'When was this machine purchased?'}),
        }

        

class WorkOrderEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['asset','recurrence','first_due_date','title','assigned_to','lockout','notification', 'department_assigned_to','image','description', 'priority', 'attachments', ]
        widgets = {
            'priority': forms.Select(choices=CRITICALITY_CHOICES),
            'first_due_date': forms.DateInput(attrs={'type': 'date'}),
            'title': forms.TextInput(attrs={'placeholder': 'Example: Change oil'}),
            'description': forms.Textarea(attrs={'placeholder': 'Example: 1) Change oil in the engine 2) Change oil in the transmission'}),
        }
        # Define the assigned_to field with an ordered queryset
        assigned_to = forms.ModelChoiceField(
            queryset=User.objects.order_by('-username'),
            widget=forms.Select(),
            empty_label="Select User"  # Optional, you can customize the empty label
            
        )

class AssetWorkOrderNewForm(forms.ModelForm):
    class Meta:
        model = WorkOrder
        fields = ['recurrence','first_due_date','title','assigned_to','lockout','notification', 'department_assigned_to','image','description', 'priority', 'attachments', ]
        widgets = {
            'priority': forms.Select(choices=CRITICALITY_CHOICES),
            'first_due_date': forms.DateInput(attrs={'type': 'date'}),
            'assigned_to': forms.Select(choices=User.objects.order_by('username').values_list('username', 'username')),
            'title': forms.TextInput(attrs={'placeholder': 'Example: Change oil'}),
            'description': forms.Textarea(attrs={'placeholder': 'Example: 1) Change oil in the engine 2) Change oil in the transmission'}),
        }

# form to create a work order record
class WorkOrderRecordForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRecord
        fields = ['workorder', 'due_date', 'comments']
        widgets = {
            'workorder': forms.Select(choices=WorkOrder.objects.values_list('asset')),
            'due_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


# form to edit work order record
class WorkOrderRecordEditForm(forms.ModelForm):
    class Meta:
        model = WorkOrderRecord
        fields = ['status', 'completed_on', 'attachments','comments']
        widgets = {
            'status': forms.Select(choices=STATUS),
            'completed_on': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

# form to update standard item 
class ProdItemStdForm(forms.ModelForm):
    class Meta:
        model = ProdItemStd
        fields = ['sku', 'description', 'kind', 'formula', 'pph', 'people_inline', 'setup_time', 'setup_people','notes', 'image']
        widgets = {
            'kind': forms.Select(choices=[
                ('tube', 'Tube'),
                ('foil', 'Foil'),
                ('bottle', 'Bottle'),
                ('replenishment', 'Replenishment'),
            ]),
        }

class ProdItemForm(forms.ModelForm):
    class Meta:
        model = ProdItem
        fields = ['item', 'qty_produced', 'people_inline', 'produced_time', 'setup_time', 'setup_people', 'completed_date']
        widgets = {
            'completed_date': forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }


class DayProductivityForm(forms.ModelForm):
    class Meta:
        model = DayProductivity  
        fields = [
            'people', 'extra_hours'
        ]
        widgets = {
            'productivity': forms.NumberInput(attrs={'step': '0.01'}),
            'extra_hours': forms.NumberInput(attrs={'step': '0.01'}),
        }