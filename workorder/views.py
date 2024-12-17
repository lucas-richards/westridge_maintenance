from django.shortcuts import render
from .models import Asset, Vendor, WorkOrder, WorkOrderRecord, KPI, KPIValue, CheckListItem, PurchasePart, ProdItemStd, ProdItem, DayProductivity
from users.models import Department
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import redirect
import json
from .forms import AssetEditForm, WorkOrderEditForm, WorkOrderRecordForm, WorkOrderRecordEditForm, AssetWorkOrderNewForm, ProdItemStdForm, ProdItemForm, DayProductivityForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import datetime
from users.models import User
import datetime as dt
from django.core.paginator import Paginator
from django.db.models.functions import TruncDate
from django.core.mail import send_mail
import os

# Create your views here.

def dashboard(request):
    # get the work orders records status and count
    work_orders_records = WorkOrderRecord.objects.all()
    assets = Asset.objects.all()

    # create a dictionary to store how many assets have 0 workorders, 1, 2, 3 or more
    assets_workorders_count = {
        'total': assets.count(),
        'zero': 0,
        'one': 0,
        'two': 0,
        'three': 0,
        'more': 0,
    }
    for asset in assets:
        workorders_count = WorkOrder.objects.filter(asset=asset).exclude(recurrence='Once').count()
        if workorders_count == 0:
            assets_workorders_count['zero'] += 1
        elif workorders_count == 1:
            assets_workorders_count['one'] += 1
        elif workorders_count == 2:
            assets_workorders_count['two'] += 1
        elif workorders_count == 3:
            assets_workorders_count['three'] += 1
        else:
            assets_workorders_count['more'] += 1

    work_orders_records_status = {
        'done': work_orders_records.filter(status='done').count(),
        'in_progress': work_orders_records.filter(status='in_progress').count(),
        'on_hold': work_orders_records.filter(status='on_hold').count(),
        'scheduled': work_orders_records.filter(status='scheduled').count(),
        'cancelled': work_orders_records.filter(status='cancelled').count(),
        'overdue': round(work_orders_records.filter(due_date__lt=timezone.now()- datetime.timedelta(days=1)).exclude(status__in=['done', 'cancelled']).count(), 0),
        'overdue_high_criticality': round(work_orders_records.filter(due_date__lt=timezone.now()- datetime.timedelta(days=1), workorder__asset__criticality='high').exclude(status__in=['done', 'cancelled']).count(), 0),
        'on_time': round(work_orders_records.filter(due_date__gte=timezone.now()- datetime.timedelta(days=1)).exclude(status__in=['done', 'cancelled']).count(), 0),
        'total': work_orders_records.count(),
        'total_exclude_done_cancelled': work_orders_records.exclude(status__in=['done', 'cancelled']).count(),
    }

    # calculate the percentages
    work_orders_records_status['overdue_percentage'] = round((work_orders_records_status['overdue'] / work_orders_records_status['total_exclude_done_cancelled']) * 100) if work_orders_records_status['total_exclude_done_cancelled'] != 0 else 0
    work_orders_records_status['on_time_percentage'] = round((work_orders_records_status['on_time'] / work_orders_records_status['total_exclude_done_cancelled']) * 100) if work_orders_records_status['total_exclude_done_cancelled'] != 0 else 0
    work_orders_records_status['done_percentage'] = round((work_orders_records_status['done'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['in_progress_percentage'] = round((work_orders_records_status['in_progress'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['on_hold_percentage'] = round((work_orders_records_status['on_hold'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['scheduled_percentage'] = round((work_orders_records_status['scheduled'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
    work_orders_records_status['cancelled_percentage'] = round((work_orders_records_status['cancelled'] / work_orders_records_status['total']) * 100) if work_orders_records_status['total'] != 0 else 0
 

    # get the KPI values
    status_kpi = KPIValue.objects.filter(kpi__name='Status Done').order_by('date')
    status_kpi_values = [value.value for value in status_kpi]
    status_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in status_kpi]
    timing_kpi = KPIValue.objects.filter(kpi__name='Timing On Time').order_by('date')
    timing_kpi_values = [value.value for value in timing_kpi]
    timing_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in timing_kpi]
    productivity_kpi = KPIValue.objects.filter(kpi__name='Productivity', date__gte=timezone.now() - datetime.timedelta(days=30)).order_by('date')
    productivity_kpi_values = [value.value for value in productivity_kpi]
    productivity_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in productivity_kpi]
    overdue_kpi = KPIValue.objects.filter(kpi__name='Overdue', date__gte=timezone.now() - datetime.timedelta(days=30)).order_by('date')
    overdue_kpi_values = [value.value for value in overdue_kpi]
    overdue_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in overdue_kpi]
    overdueH_kpi = KPIValue.objects.filter(kpi__name='Overdue High Criticality', date__gte=timezone.now() - datetime.timedelta(days=30)).order_by('date')
    overdueH_kpi_values = [value.value for value in overdueH_kpi]
    overdueH_kpi_dates = overdue_kpi_dates
    while len(overdueH_kpi_values) < len(overdue_kpi_dates):
        overdueH_kpi_values.insert(0, 0)
    wordordersqty_kpi_values = [value.value for value in KPIValue.objects.filter(kpi__name='Work Orders Qty', date__gte=timezone.now() - datetime.timedelta(days=7)).order_by('date')]
    wordordersqty_kpi_dates = [value.date.strftime('%m-%d-%Y') for value in KPIValue.objects.filter(kpi__name='Work Orders Qty', date__gte=timezone.now() - datetime.timedelta(days=7)).order_by('date')]


    context = {
        'title': 'Dashboard',
        'work_orders_records_status': work_orders_records_status,
        'status_kpi_values': status_kpi_values,
        'status_kpi_dates': status_kpi_dates,
        'timing_kpi_values': timing_kpi_values,
        'timing_kpi_dates': timing_kpi_dates,
        'productivity_kpi_values': productivity_kpi_values,
        'productivity_kpi_dates': productivity_kpi_dates,
        'overdue_kpi_values': overdue_kpi_values,
        'overdue_kpi_dates': overdue_kpi_dates,
        'overdueH_kpi_values': overdueH_kpi_values,
        'overdueH_kpi_dates': overdueH_kpi_dates,
        'assets_workorders_count': assets_workorders_count,
        'wordordersqty_kpi_values': wordordersqty_kpi_values,
        'wordordersqty_kpi_dates': wordordersqty_kpi_dates,
        
    }
    return render(request, 'workorder/dashboard.html', context)

@csrf_exempt
@require_http_methods(["GET", "PUT"])
def asset_json(request, id):
    try:
        asset = Asset.objects.get(id=id)
        workorders_all = WorkOrder.objects.filter(asset=asset)
        workorders = []
        for wo in workorders_all:
            workorder = {
            'id': wo.id,
            'title': wo.title,
            'priority': wo.get_priority_display(),
            'recurrence': wo.get_recurrence_display(),
            'last_record_status': wo.workorderrecord_set.order_by('-created_on').first().status if wo.workorderrecord_set.order_by('-created_on').first() else '',
            'last_record_due_date': wo.workorderrecord_set.order_by('-created_on').first().due_date.strftime('%m-%d-%Y') if wo.workorderrecord_set.order_by('-created_on').first() else '',
            }
            workorders.append(workorder)

        if request.method == "GET":
            data = {
                'id': asset.id,
                'code': asset.code,
                'name': asset.name,
                'status': asset.status,
                'description': asset.description,
                'image_url': asset.image.url if asset.image else '',
                'serial_number': asset.serial_number,
                'model': asset.model,
                'manufacturer': asset.manufacturer,
                'year': asset.year,
                'location': asset.location if asset.location else '',
                'parent': asset.parent.name if asset.parent else '',
                'department_in_charge': asset.department_in_charge.name if asset.department_in_charge else '',
                'vendors': asset.vendors.name if asset.vendors else '',
                'created_by': asset.created_by.username if asset.created_by else '',
                'created_on': asset.created_on.strftime('%m-%d-%Y %H:%M:%S'),
                'last_updated': asset.last_updated.strftime('%m-%d-%Y %H:%M:%S'),
                'criticality': asset.criticality,
                'attachments': asset.attachments.url if asset.attachments else '',
                'workorders': workorders,
            }
            return JsonResponse(data)
    except Asset.DoesNotExist:
        return JsonResponse({'error': 'Asset not found'}, status=404)
    except ( Asset.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def asset_page(request, id):
    # This is the view that renders the full page
    try:
        asset = Asset.objects.get(id=id)
        return redirect('workorder-assets')
    except Asset.DoesNotExist:
        return render(request, '404.html', status=404)

def assets(request):
    assets = Asset.objects.all().order_by('code')
    # add an extra property to each asset 'workorders_count'
    for asset in assets:
        asset.workorders_count = WorkOrder.objects.filter(asset=asset).exclude(recurrence='Once').count()

    current_time = timezone.now()

    context = {
        'title': 'Assets',
        'assets': assets,
        'current_time': current_time
    }

    return render(request, 'workorder/assets.html', context)

@login_required
def add_asset(request):
    if request.method == 'POST':
        form = AssetEditForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        # if the location is warehouse, then find the last code that starts with W and increment it by 1. If last code is O-003 then the new code will be O-004
        if form.is_valid():
            location = request.POST['location']
            prefix = ''
            if location == 'warehouse':
                prefix = 'W'
            elif location == 'office':
                prefix = 'O'
            elif location in ['production Line #1', 'production Line #2', 'production Line #3']:
                prefix = 'P'
            elif location == 'assembly':
                prefix = 'A'
            elif location == 'bulding':
                prefix = 'B'
            elif location == 'roof':
                prefix = 'F'
            elif location == 'quality lab':
                prefix = 'Q'
            elif location == 'scale':
                prefix = 'SC'
            else:
                messages.error(request, 'Error adding asset')
            
            last_code = Asset.objects.filter(code__startswith=prefix).order_by('-code').first()
            if last_code:
                last_code = last_code.code.split('-')[1]
                form.instance.code = f'{prefix}-{str(int(last_code) + 1).zfill(3)}'
            else:
                form.instance.code = f'{prefix}-001'
            
            form.save()
            return redirect('workorder-assets')
    else:
        form = AssetEditForm()
    context = {
        'title': 'Add Asset',
        'form': form,
    }
    return render(request, 'workorder/new_asset.html', context)

@login_required
def edit_asset(request, id):
    assets = Asset.objects.all().order_by('code')
    asset = Asset.objects.get(id=id)

    if request.method == 'POST':
        form = AssetEditForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('workorder-assets')
    else:
        form = AssetEditForm(instance=asset)
    context = {
        'title': 'Edit Asset',
        'asset': asset,
        'form': form,
    }
    return render(request, 'workorder/edit_asset.html', context) 

@login_required
def delete_asset(request, id):
    asset = Asset.objects.get(id=id)
    try:
        asset.delete()
        messages.success(request, 'Asset deleted successfully')
    except Exception as e:
        messages.error(request, 'Error deleting asset')
    return redirect('workorder-assets')

@login_required
def asset_workorders_new(request, id):
    asset = Asset.objects.get(id=id)
    if request.method == 'POST':
        form = AssetWorkOrderNewForm(request.POST, request.FILES)
        # add created by
        form.instance.asset = asset
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order added successfully')
            # redirect to asset
            return redirect('workorder-assets')
    else:
        form = AssetWorkOrderNewForm()
        
        # order by assigned to
        form.fields['assigned_to'].queryset = User.objects.order_by('username')
    context = {
        'title': 'Add Work Order',
        'form': form,
        'asset': asset,
    }
    return render(request, 'workorder/new_workorder.html', context)

@login_required
def vendors(request):
    vendors = Vendor.objects.all()
    context = {
        'title': 'Vendors',
        'vendors': vendors,
    }

    return render(request, 'workorder/vendors.html', context)

@login_required
def vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/vendor.html', context)

@login_required
def add_vendor(request):
    if request.method == 'POST':
        pass
    context = {
        'title': 'Add Vendor',
    }

    return render(request, 'workorder/add_vendor.html', context)

@login_required
def edit_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    context = {
        'title': 'Edit Vendor',
        'vendor': vendor,
    }

    return render(request, 'workorder/edit_vendor.html', context)

@login_required
def delete_vendor(request, id):
    vendor = Vendor.objects.get(id=id)
    vendor.delete()
    return redirect('workorder-vendors')

def workorders(request):
    # set idwo to whatever the request has
    idwo = request.GET.get('idwo')
    workorders = WorkOrder.objects.all()
    workorders_with_last_record = []
    form = WorkOrderEditForm()
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order added successfully')
            return redirect('workorder-workorders')
        else:
            print(form.errors)


    for workorder in workorders:
        last_record = workorder.workorderrecord_set.order_by('-created_on').first()
        workorders_with_last_record.append({
            'workorder': workorder,
            'last_record': last_record,
            'recurrence': workorder.get_recurrence_display(),
        })

    # order workorders_by_last_record based on the last_record.due_date
    workorders_with_last_record = sorted(workorders_with_last_record, key=lambda x: x['last_record'].due_date if x['last_record'] else None)
    
    context = {
        'title': 'Work Orders',
        'workorders': workorders_with_last_record,
        'form': form,
        'idwo':idwo
    }

    return render(request, 'workorder/workorders.html', context)


@csrf_exempt
@require_http_methods(["GET", "PUT"])
def workorder(request, id):
    try:
        workorder = WorkOrder.objects.get(id=id)
        records = WorkOrderRecord.objects.filter(workorder=workorder).order_by('-due_date')
        last_record = records.first()

        if request.method == "GET":
            data = {
                'id': workorder.id,
                'code': workorder.asset.code if workorder.asset else '',
                'asset': workorder.asset.name if workorder.asset else '',
                'title': workorder.title,
                'notification': workorder.notification,
                'priority': workorder.priority,
                'description': workorder.description,
                'assigned_to': workorder.assigned_to.username if workorder.assigned_to else '',
                'department_assigned_to': workorder.department_assigned_to.name if workorder.department_assigned_to else '',
                'created_by': workorder.created_by.username if workorder.created_by else '',
                'created_on': workorder.created_on.strftime('%m-%d-%Y %H:%M:%S'),
                'last_updated': workorder.last_updated.strftime('%m-%d-%Y %H:%M:%S'),
                'recurrence': workorder.get_recurrence_display(),
                'asset': workorder.asset.name if workorder.asset else '',
                'image_url': workorder.image.url if workorder.image else '',
                'attachments': workorder.attachments.url if workorder.attachments else '',
                'time_until_due': (last_record.due_date - timezone.now() + dt.timedelta(days=1) ).days if last_record.due_date else '',
                'records': [
                            {
                                'id': record.id, 
                                'created_on': record.created_on.strftime('%m-%d-%Y'), 
                                'status': record.status, 
                                'due_date': record.due_date.strftime('%m-%d-%Y') if record.due_date else '', 
                                'completed_on': record.completed_on.strftime('%m-%d-%Y') if record.completed_on else '', 
                                'completed_by': record.completed_by.username if record.completed_by else '', 
                                'time_to_complete': record.time_to_complete.total_seconds() if record.time_to_complete else '', 
                                'attachments': record.attachments.url if record.attachments else '', 
                                'comments': record.comments,
                                'checklist_items': [
                                    {
                                        'id': item.id, 
                                        'title': item.title, 
                                        'description': item.description, 
                                        'status': item.status, 
                                        'due_date': item.due_date.strftime('%m-%d-%Y') if item.due_date else '', 
                                        'attachments': item.attachments.url if item.attachments else '', 
                                        'notes': item.notes
                                    }
                                    for item in CheckListItem.objects.filter(workorder_record=record).order_by('created_on')
                                ]
                            } 
                            for record in records
                        ],
                'last_record_status': last_record.status if last_record else '',
                'last_record_checklist_items': [
                    {
                        'id': item.id, 
                        'title': item.title, 
                        'description': item.description, 
                        'status': item.status, 
                        'due_date': item.due_date.strftime('%m-%d-%Y') if item.due_date else '', 
                        'attachments': item.attachments.url if item.attachments else '', 
                        'notes': item.notes
                    }
                    for item in CheckListItem.objects.filter(workorder_record=last_record).order_by('created_on')
                ],
                'last_record_purchase_parts': [
                    {
                        'id': part.id, 
                        'title': part.title, 
                        'description': part.description, 
                        'purchased': part.purchased
                    }
                    for part in last_record.purchase_parts.all()
                ],
            }
            return JsonResponse(data)
    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except (WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def workorder_page(request, id):
    # This is the view that renders the full page
    try:
        workorder = WorkOrder.objects.get(id=id)
        return redirect('workorder-workorders')
    except WorkOrder.DoesNotExist:
        return render(request, '404.html', status=404)

@login_required
def add_workorder(request):
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order added successfully')
            return redirect('workorder-workorders')
    else:
        form = WorkOrderEditForm()
        # order by assigned to
        form.fields['assigned_to'].queryset = User.objects.order_by('username')
    context = {
        'title': 'Add Work Order',
        'form': form,
    }
    return render(request, 'workorder/new_workorder.html', context)

@login_required
def copy_workorder(request, id):
    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            messages.success(request, 'Work Order added successfully')
            return redirect('workorder-workorders')
    else:
        workorder = WorkOrder.objects.get(id=id)
        form = WorkOrderEditForm(instance=workorder)
        # reorder assets in the form by code
        form.fields['asset'].queryset = Asset.objects.order_by('code')
        # clear the asset form value
        form.fields['asset'].initial = None
    
    context = {
        'title': 'Add Work Order',
        'form': form,
    }
    return render(request, 'workorder/new_workorder.html', context)

@login_required
def edit_workorder(request, id):
    workorders = WorkOrder.objects.all().order_by('created_on')
    workorder = WorkOrder.objects.get(id=id)

    if request.method == 'POST':
        form = WorkOrderEditForm(request.POST, request.FILES, instance=workorder)
        if form.is_valid():
            form.save()
            return redirect('workorder-workorders')
    else:
        form = WorkOrderEditForm(instance=workorder)
    context = {
        'title': 'Edit workorder',
        'workorder': workorder,
        'form': form,
    }
    return render(request, 'workorder/edit_workorder.html', context) 

@login_required
def delete_workorder(request, id):
    workorder = WorkOrder.objects.get(id=id)
    if request.user.is_superuser:
        workorder.delete()
        messages.success(request, 'Work Order deleted successfully')
    else:
        email_user = os.environ.get('EMAIL_USER')
        email_password = os.environ.get('EMAIL_PASS')
        author_email = 'lrichards@westridgelabs.com'
        recipients = ['lrichards@westridgelabs.com']
        send_mail(
            'Work Order Deletion Request',
            f'User {request.user.username} has requested to delete work order {workorder.id}.',
            author_email,
            recipients,
            fail_silently=False,
        )
        messages.info(request, 'Request to delete work order has been sent to the administrator.')
    return redirect('workorder-workorders')


def workorder_records(request):
    idwor = request.GET.get('idwor')
    workorders = WorkOrder.objects.all()
    records = []
    for workorder in workorders:
        last_record = WorkOrderRecord.objects.filter(workorder=workorder).order_by('-due_date').first()
        if last_record:
            records.append(last_record)
    records = sorted(records, key=lambda x: x.due_date)
    # rearrange the records list so records with status cancelled or done are at the end
    records = sorted(records, key=lambda x: x.status in ['cancelled', 'done'])
    # add this to each record 'time_until_due': (record.due_date - timezone.now() ).days if record.due_date else '',
    for record in records:
        record.time_until_due = (record.due_date - timezone.now() + dt.timedelta(days=1) ).days if record.due_date else ''
        record.status = record.get_status_display()

    context = {
        'title': 'Work Order Records',
        'records': records,
        'idwor':idwor
    }

    return render(request, 'workorder/workorder_records.html', context)

@login_required
@csrf_exempt
@require_http_methods(["GET", "POST", "PUT"])
def workorder_record(request, id):
    try:
        record = WorkOrderRecord.objects.get(id=id)
        checklist_items = CheckListItem.objects.filter(workorder_record=record).order_by('created_on')

        
        data = {
                'id': record.id,
                'workorder_id': record.workorder.id if record.workorder else '',
                'workorder_title': record.workorder.title if record.workorder else '',
                'workorder_assigned_to': record.workorder.assigned_to.username if record.workorder.assigned_to else '',
                'workorder_recurrence': record.workorder.get_recurrence_display() if record.workorder else '',
                'workorder_description': record.workorder.description if record.workorder else '',
                'workorder_image': record.workorder.image.url if record.workorder.image else '',
                'workorder_attachment': record.workorder.attachments.url if record.workorder.attachments else '',
                'workorder_asset': record.workorder.asset.code if record.workorder.asset else '',
                'workorder_asset_name': record.workorder.asset.name if record.workorder.asset else '',
                'status': record.status,
                'due_date': record.due_date.strftime('%m-%d-%Y') if record.due_date else '',
                'completed_on': record.completed_on.strftime('%Y-%m-%d') if record.completed_on else '',
                'attachments': record.attachments.url if record.attachments else '',
                'comments': record.comments if record.comments else '',
                'time_until_due': (record.due_date - timezone.now()- datetime.timedelta(days=1) ).days if record.due_date else '',
                'checklist_items': [{'id': item.id, 'title': item.title, 'description': item.description, 'status': item.status, 'due_date': item.due_date.strftime('%m-%d-%Y') if item.due_date else '', 'attachments': item.attachments.url if item.attachments else '', 'notes': item.notes} for item in checklist_items],
                'purchase_parts': [{'id': part.id, 'title': part.title, 'description': part.description, 'purchased': part.purchased } for part in record.purchase_parts.all()],
        }     

        status = request.POST.get('status')

        if request.method == "POST":
            user_assigned_to = record.workorder.assigned_to
            user_logged_in = request.user


            if status:
                if user_assigned_to == user_logged_in:
                    # get user
                    user = User.objects.get(username=request.user)
                    record.completed_by = user
                    record.status = status
                    completed_on = request.POST.get('completed_on')
                    if completed_on:
                        # Convert string to a timezone-aware datetime
                        record.completed_on = timezone.make_aware(
                            timezone.datetime.strptime(completed_on, '%Y-%m-%d')
                        )
                    # Handle file upload
                    if 'attachments' in request.FILES:
                        record.attachments = request.FILES['attachments']
                    record.comments = request.POST.get('comments')
                    for item in checklist_items:
                        item_status = request.POST.get(f'checklist_item_{item.id}')
                        if item_status:
                            item.status = item_status
                            item.notes = request.POST.get(f'checklist_item_{item.id}_notes', '')
                            item.save()
                    print('parts', record.purchase_parts.all())
                    print('request.POST', request.POST)
                    for part in record.purchase_parts.all():
                        value = request.POST.get(f'purchase_part_{part.id}', False)
                        part.purchased = True if value == 'on' else False
                        part.save()
                    record.save()
                    messages.success(request, 'Record updated successfully')
                else:
                    messages.error(request, 'Error updating record. Only the assigned user can update it')
                return redirect('workorder-workorder-records')

            
        if request.method == "GET":
            return JsonResponse(data)

    except WorkOrder.DoesNotExist:
        return JsonResponse({'error': 'workorder not found'}, status=404)
    except ( WorkOrder.DoesNotExist, Department.DoesNotExist, Vendor.DoesNotExist):
        return JsonResponse({'error': 'Related entity not found'}, status=404)

def workorder_record_page(request, id):
    # This is the view that renders the full page
    try:
        record = WorkOrderRecord.objects.get(id=id)
        return redirect('workorder-workorder-records')
    except WorkOrderRecord.DoesNotExist:
        return render(request, '404.html', status=404)

def add_workorder_record(request):
    if request.method == 'POST':
        form = WorkOrderRecordForm(request.POST, request.FILES)
        # add created by
        form.instance.created_by = request.user
        if form.is_valid():
            form.save()
            return redirect('workorder-workorder-records')
    else:
        form = WorkOrderRecordForm()
    context = {
        'title': 'Add Work Order Record',
        'form': form,
    }
    return render(request, 'workorder/new_workorder_record.html', context)


@login_required
def production(request):
    items = ProdItemStd.objects.all().order_by('sku')

    context = {
        'title': 'Production',
        'items': items,
    }
    return render(request, 'workorder/production.html', context)

@login_required
def add_production_entry(request):
    if request.method == 'POST':
        items = ProdItemStd.objects.all()
        for i in range(1, len(items) + 1):
            item_id = request.POST.get(f'item{i}')
            qty = request.POST.get(f'qty{i}')
            start_time = request.POST.get(f'start_time{i}')
            end_time = request.POST.get(f'end_time{i}')
            break_minutes = request.POST.get(f'break_minutes{i}')
            people_inline = request.POST.get(f'people_inline{i}')
            setup_time = request.POST.get(f'setup_time{i}')
            setup_people = request.POST.get(f'setup_time_people{i}')
            completed_date = request.POST.get('completed_date')

            if item_id and qty and start_time and end_time and break_minutes and people_inline and completed_date:
                try:
                    qty = int(qty)
                    start_time = timezone.datetime.strptime(start_time, '%H:%M')
                    end_time = timezone.datetime.strptime(end_time, '%H:%M')
                    break_minutes = int(break_minutes)
                    produced_time = round((end_time - start_time).total_seconds() / 3600 - (break_minutes / 60), 1)  # Convert to hours and subtract break time
                    people_inline = float(people_inline)
                    setup_time = float(setup_time)
                    setup_people = int(setup_people)
                    completed_date = timezone.datetime.strptime(completed_date, '%Y-%m-%d')
                    
                    ProdItem.objects.create(
                        item_id=item_id,
                        qty_produced=qty,
                        produced_time=produced_time,
                        people_inline=people_inline,
                        setup_time=setup_time,
                        setup_people=setup_people,
                        completed_date=completed_date,
                    )
                except ValueError:
                    messages.error(request, f'Invalid data for item {i} ')

            people = request.POST.get('people')
            extra_hours = request.POST.get('extra_hours') if request.POST.get('extra_hours') else 0
            if people:
                try:
                    people = int(people)
                    extra_hours = float(extra_hours)
                    day_productivity, created = DayProductivity.objects.get_or_create(
                        date=completed_date,
                        defaults={'people': people, 'extra_hours': extra_hours, 'productivity': 0}
                    )
                    if not created:
                        day_productivity.people = people
                        day_productivity.extra_hours = extra_hours
                    day_productivity.productivity = day_productivity.productivity or 0
                    day_productivity.save()
                except ValueError:
                    messages.error(request, 'Invalid data for DayProductivity')

        messages.success(request, 'Production entry added successfully')
        return redirect('workorder-production')
    else:
        items = ProdItemStd.objects.all()
    context = {
        'title': 'New Production Entry',
        'items': items,
    }
    return render(request, 'workorder/new_production_entry.html', context)

@login_required
def productivity(request):
    # items = ProdItem.objects.all().order_by('-completed_date')
    # Group items by completed_date (date only, ignoring time)
    grouped_items = (
        ProdItem.objects
        .annotate(date=TruncDate('completed_date'))  # Truncate to date
        .order_by('-date')
    )

    # Get unique dates from items
    unique_dates = grouped_items.values_list('date', flat=True).distinct()

    # Paginate dates
    paginator = Paginator(unique_dates, 1)  # One date group per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Get the current date for this page
    current_date = page_obj.object_list[0] if page_obj.object_list else None

    # Filter items by the current date in the page
    items = ProdItem.objects.filter(completed_date__date=current_date) if current_date else []


    # add a property called pph (parts per hour) to each item
    for item in items:
        print('item',item)
        item.pph = round(item.qty_produced / item.produced_time) if item.produced_time != 0 else 0
        item.pphp = round(item.pph/item.people_inline) if item.people_inline != 0 else 0
        item.item.pphp = round(item.item.pph/item.item.people_inline) if item.item.people_inline != 0 else 0
        item.setup_total = round(item.setup_time * item.setup_people, 1) if item.setup_people != 0 else 0
        item.item.setup_total = round(item.item.setup_time * item.item.setup_people, 1) if item.item.setup_people != 0 else 0
        item.earned_hours_piece = 1 / (item.item.pph / item.item.people_inline) if item.item.people_inline and item.item.pph != 0 else 0
        
        # Actual times
        item.setup_time_actual = round(item.setup_time * item.setup_people, 1)
        item.inline_hours_actual = round(item.produced_time * item.people_inline, 1)
        
        # Earned hours
        item.setup_earned_hours = round(item.item.setup_time * item.item.setup_people, 1) if item.setup_time else 0
        item.inline_earned_hours = round(item.qty_produced * item.earned_hours_piece, 1)
        
        # Total earned hours
        item.earned_hours_total = item.inline_earned_hours + item.setup_earned_hours
        
        # Productivity calculations
        item.productivity_inline = round(item.pphp / item.item.pphp * 100, 0) if item.item.pphp != 0 else 0
        item.productivity_setup = round(item.item.setup_total/item.setup_total * 100, 0) if item.setup_total != 0 else None

        # Total productivity
        if item.productivity_setup is not None:
            item.productivity_total = round((item.inline_earned_hours/item.earned_hours_total*item.productivity_inline + item.setup_earned_hours/item.earned_hours_total*item.productivity_setup) , 0) if item.earned_hours_total != 0 else 0
        else:
            item.productivity_total = item.productivity_inline
        
        # Standard hours
        item.std_hours = round(item.qty_produced * item.earned_hours_piece / item.item.people_inline, 1)


    status_kpi_dates = [item.item.sku for item in items][::-1]
    status_kpi_values = [item.productivity_total for item in items][::-1]

    # Get the corresponding DayProductivity object for the current date
    day_productivity = None
    if current_date:
        day_productivity = DayProductivity.objects.filter(date=current_date).first()
        # update the day productivity bvalues like earned hours, productivity and pieces produced
        day_productivity.earned_hours = round(sum([item.earned_hours_total for item in items]), 1)
        day_productivity.productivity_inline = round(sum([item.productivity_total for item in items]) / len(items)) if len(items) != 0 else 0
        day_productivity.total_produced = sum([item.qty_produced for item in items])
        day_productivity.available_hours = day_productivity.people * 7.5 + day_productivity.extra_hours
        day_productivity.productivity = round(day_productivity.earned_hours / day_productivity.available_hours * 100) if day_productivity.available_hours != 0 else 0
        # if item std is kind bottle then add it to total pieces bottle
        day_productivity.total_produced_bottle = sum([item.qty_produced for item in items if item.item.kind == 'bottle'])
        day_productivity.total_produced_foil = sum([item.qty_produced for item in items if item.item.kind == 'foil'])
        day_productivity.total_produced_tube = sum([item.qty_produced for item in items if item.item.kind == 'tube'])
        day_productivity.total_produced_replenishment = sum([item.qty_produced for item in items if item.item.kind == 'replenishment'])
        # calculate bottle productivity by doinw the average of each bottle productivity
        day_productivity.productivity_bottle = round(sum([item.productivity_total for item in items if item.item.kind == 'bottle']) / len([item for item in items if item.item.kind == 'bottle'])) if len([item for item in items if item.item.kind == 'bottle']) != 0 else 0
        # calculate tube productivity by doinw the average of each tube productivity
        day_productivity.productivity_tube = round(sum([item.earned_hours_total for item in items if item.item.kind == 'tube']) / 8*100) if len([item for item in items if item.item.kind == 'tube']) != 0 else 0
        # calculate replenishment productivity by doinw the average of each replenishment productivity
        day_productivity.productivity_replenishment = round(sum([item.productivity_total for item in items if item.item.kind == 'replenishment']) / len([item for item in items if item.item.kind == 'replenishment'])) if len([item for item in items if item.item.kind == 'replenishment']) != 0 else 0
        # calculate foil productivity by summing all foil earned hours and divided by 8
        day_productivity.productivity_foil = round(sum([item.earned_hours_total for item in items if item.item.kind == 'foil']) / 8*100) if len([item for item in items if item.item.kind == 'foil']) != 0 else 0
       
        day_productivity.save()

     
    context = {
        'title': 'Productivity',
        'items': items,
        'page_obj': page_obj,
        'status_kpi_dates': status_kpi_dates,
        'status_kpi_values': status_kpi_values,
        'day_productivity': day_productivity,
    }
    return render(request, 'workorder/productivity.html', context)


@login_required
# this view will show all the item standards in a form so you can update them
def standards(request):
    items = ProdItemStd.objects.all().order_by('-pph')
    if request.method == 'POST':
        for item in items:
            item.sku = request.POST.get(f'sku_{item.id}')
            item.name = request.POST.get(f'name_{item.id}')
            item.kind = request.POST.get(f'kind_{item.id}')
            item.pphp = request.POST.get(f'pphp_{item.id}')
            item.people_inline = request.POST.get(f'people_inline_{item.id}')
            item.setup_time = request.POST.get(f'setup_time_{item.id}')
            item.setup_people = request.POST.get(f'setup_people_{item.id}')
            item.save()
        messages.success(request, 'Item standards updated successfully')
        return redirect('workorder-standards')
    context = {
        'title': 'Standards',
        'items': items,
    }
    return render(request, 'workorder/standards.html', context)

@login_required
# update standard
def update_standard(request, id):
    item = ProdItemStd.objects.get(id=id)
    if request.method == 'POST':
        form = ProdItemStdForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item standard updated successfully')
            return redirect('workorder-standards')
    else:
        form = ProdItemStdForm(instance=item)
    context = {
        'title': 'Update Standard',
        'item': item,
        'form': form,
    }
    return render(request, 'workorder/update_standard.html', context)

@login_required
def update_item(request, id):
    item = ProdItem.objects.get(id=id)
    if request.method == 'POST':
        form = ProdItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item updated successfully')
            return redirect('workorder-productivity')
    else:
        form = ProdItemForm(instance=item)
    context = {
        'title': 'Update Item',
        'item': item,
        'form': form,
    }
    return render(request, 'workorder/update_item.html', context)

@login_required
def update_day(request, id):
    day_productivity = DayProductivity.objects.get(id=id)
    if request.method == 'POST':
        form = DayProductivityForm(request.POST, request.FILES, instance=day_productivity)
        if form.is_valid():
            form.save()
            messages.success(request, 'Day productivity updated successfully')
            return redirect('workorder-productivity')
    else:
        form = DayProductivityForm(instance=day_productivity)
    context = {
        'title': 'Update Day Productivity',
        'day_productivity': day_productivity,
        'form': form,
    }
    return render(request, 'workorder/update_day.html', context)