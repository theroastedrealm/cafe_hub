from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, View, CreateView, UpdateView, DeleteView
from .models import InventoryItem, Category
from .forms import InventoryItemForm
from cafe_hub.settings import LOW_INVENTORY_THRESHOLD
from django.contrib import messages

class Index(TemplateView):
    template_name = 'inventory/index.html'
    
class Dashboard(View):
    def get(self, request):
        branch = request.user.branch
        items = InventoryItem.objects.filter(branch=branch).order_by('id')
    
        low_inventory = InventoryItem.objects.filter(branch=branch, quantity__lte=LOW_INVENTORY_THRESHOLD)
        
        if low_inventory.count() > 0:
            if low_inventory.count() > 1:
                messages.error(request, f'You have {low_inventory.count()} items with low inventory')
            else:
                messages.error(request, f'You have {low_inventory.count()} item with low inventory')
        
        low_inventory_ids = InventoryItem.objects.filter(branch=branch, quantity__lte=LOW_INVENTORY_THRESHOLD).values_list('id', flat=True)
        
        
        return render(request, 'inventory/dashboard.html', {'items': items, 'low_inventory_ids': low_inventory_ids})


class AddItem(CreateView):
    model = InventoryItem   
    form_class = InventoryItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('dashboard')
    
    # these two methods are used to pass the categories to the form
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context
    
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
    
class DeleteItem(DeleteView):
    model = InventoryItem
    template_name = 'inventory/delete_item.html'
    success_url = reverse_lazy('dashboard')
    content_object_name = 'item'
    
    
    
    