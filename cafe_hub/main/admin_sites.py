from django.apps import apps
from django.dispatch import receiver
from .models import Branch  
from .admin import BranchAdminSite  
from django.db.models.signals import post_migrate
from django.contrib.admin import AdminSite


branch_admin_sites = {}

def populate_branch_admin_sites():
    inventoryModel = apps.get_model('inventory', 'InventoryItem')
    categoryModel = apps.get_model('inventory', 'Category')
    seatingModel = apps.get_model('seating_main', 'Seat')
    customUserModel = apps.get_model('main', 'CustomUser')
    branchModel = apps.get_model('main', 'Branch')

    for branch in branchModel.objects.all():
        branch_admin_site = BranchAdminSite(name=f'{branch.name}_admin')
        branch_admin_site.register(inventoryModel)
        branch_admin_site.register(categoryModel)
        branch_admin_site.register(seatingModel)
        branch_admin_site.register(customUserModel)
        branch_admin_sites[branch.name] = branch_admin_site

