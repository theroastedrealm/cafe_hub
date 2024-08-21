from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from datetime import timedelta
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from .models import InventoryItem, Category
from .forms import InventoryItemForm
from cafe_hub.settings import LOW_INVENTORY_THRESHOLD
from django.contrib import messages
from django.contrib import admin
from django.conf import settings

class Index(TemplateView):
    template_name = 'inventory/index.html'
    
class Dashboard(View):
    def get(self, request):
        if not request.user.is_staff:
            return redirect('menu_page')
        branch = request.user.branch
        items = InventoryItem.objects.filter(branch=branch).order_by('id')
    
        low_inventory = InventoryItem.objects.filter(branch=branch, quantity__lte=settings.LOW_INVENTORY_THRESHOLD)
        
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'You have {low_inventory.count()} items with low inventory')
            else:
                messages.error(request, f'You have {low_inventory.count()} item with low inventory')
        
        low_inventory_ids = InventoryItem.objects.filter(branch=branch, quantity__lte=settings.LOW_INVENTORY_THRESHOLD).values_list('id', flat=True)
        
        return render(request, 'inventory/dashboard.html', {
            'items': items,
            'low_inventory_ids': low_inventory_ids,
            'LOW_INVENTORY_THRESHOLD': settings.LOW_INVENTORY_THRESHOLD
        })

class AddItem(CreateView):
    model = InventoryItem   
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    # these two methods are used to pass the categories to the form
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        if not self.request.user.is_superuser:
            form.instance.branch = self.request.user.branch 
        return super().form_valid(form)
    
class EditItem(UpdateView):
    model = InventoryItem
    form_class = InventoryItemForm 
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')

    def get_queryset(self):
        branch = self.request.user.branch
        return InventoryItem.objects.filter(branch=branch)
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
class DeleteItem(DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    content_object_name = 'item'

    def get_queryset(self):
        branch = self.request.user.branch
        return InventoryItem.objects.filter(branch=branch)
    
    
    
    