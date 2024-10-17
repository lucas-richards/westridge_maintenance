from django.contrib import admin

# Register your models here.
from .models import  Vendor, Asset, WorkOrder, CheckListItem, WorkOrderRecord, KPI, KPIValue

admin.site.register(Vendor)
admin.site.register(Asset)
admin.site.register(WorkOrder)
admin.site.register(WorkOrderRecord)
admin.site.register(CheckListItem)
admin.site.register(KPI)
admin.site.register(KPIValue)



