from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='workorder-dashboard'),
    path('assets/', views.assets, name='workorder-assets'),
    path('asset/<int:id>/', views.asset_page, name='workorder-asset-page'), # For rendering the page
    path('asset/<int:id>/json/', views.asset_json, name='workorder-asset-json'), # For returning JSON data
    path('asset/add/', views.add_asset, name='workorder-add-asset'),
    path('asset/edit/<int:id>/', views.edit_asset, name='workorder-edit-asset'),
    path('asset/delete/<int:id>/', views.delete_asset, name='workorder-delete-asset'),
    path('vendors/', views.vendors, name='workorder-vendors'),
    path('vendor/<int:id>/', views.vendor, name='workorder-vendor'),
    path('vendor/add/', views.add_vendor, name='workorder-add-vendor'),
    path('vendor/edit/<int:id>/', views.edit_vendor, name='workorder-edit-vendor'),
    path('vendor/delete/<int:id>/', views.delete_vendor, name='workorder-delete-vendor'),
    path('workorders/', views.workorders, name='workorder-workorders'),
    
    path('workorder/<int:id>/<int:id2>/', views.workorder_record_items, name='workorder-record-items'),
    path('workorder/<int:id>/', views.workorder_page, name='workorder-page'),  # For rendering the page
    path('workorder/<int:id>/json/', views.workorder, name='workorder-json'),  # For returning JSON data
    path('workorder/add/', views.add_workorder, name='workorder-add-workorder'),
    path('workorder/copy/<int:id>/', views.copy_workorder, name='workorder-copy-workorder'),
    path('workorder/edit/<int:id>/', views.edit_workorder, name='workorder-edit-workorder'),
    path('workorder/delete/<int:id>/', views.delete_workorder, name='workorder-delete-workorder'),
    path('asset/<int:id>/workorders/new/', views.asset_workorders_new, name='workorder-asset-workorders-new'),
    path('workorder_records/', views.workorder_records, name='workorder-workorder-records'),
    path('workorder_record/<int:id>/json/', views.workorder_record, name='workorder-workorder-record-json'), # For rendering the page
    path('workorder_record/<int:id>/', views.workorder_record_page, name='workorder-workorder-record'),  # For returning JSON data
    path('workorder_record/add/', views.add_workorder_record, name='workorder-add-workorder-record'),
    path('production/', views.production, name='workorder-production'),
    path('add_production_entry/', views.add_production_entry, name='workorder-add-production-entry'),
    path('productivity/', views.productivity, name='workorder-productivity'),
    path('standards/', views.standards, name='workorder-standards'),
    path('standard/new/', views.add_standard, name='workorder-add-standard'),
    path('standard/<int:id>/', views.update_standard, name='workorder-update-standard'),
    path('item/<int:id>/', views.update_item, name='workorder-update-item'),
    path('day/<int:id>/', views.update_day, name='workorder-update-day'),
    
]
