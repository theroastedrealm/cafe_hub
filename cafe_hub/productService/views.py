from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from .models import ProductService
from .forms import ProductServiceForm
import os

def product_service_list(request):
    items = ProductService.objects.all()
    return render(request, 'product_service_list.html', {'items': items})

def product_service_add(request):
    if request.method == 'POST':
        form = ProductServiceForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_service_list')
    else:
        form = ProductServiceForm()
    return render(request, 'product_service_form.html', {'form': form})

def product_service_edit(request, pk):
    item = get_object_or_404(ProductService, pk=pk)
    if request.method == 'POST':
        form = ProductServiceForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect('product_service_list')
    else:
        form = ProductServiceForm(instance=item)
    return render(request, 'product_service_form.html', {'form': form})

def product_service_delete(request, pk):
    item = get_object_or_404(ProductService, pk=pk)
    if request.method == 'POST':
        if item.image and hasattr(item.image, 'path'):  # Ensure item.image has a path attribute
            image_path = os.path.join(settings.MEDIA_ROOT, item.image.path)
            if os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    print(f"Deleted image at {image_path}")
                except Exception as e:
                    print(f"Error deleting image at {image_path}: {e}")
            else:
                print(f"Image path does not exist: {image_path}")
        item.delete()
        return redirect('product_service_list')
    return render(request, 'product_service_confirm_delete.html', {'item': item})

def product_service_confirm_delete(request, pk):
    item = get_object_or_404(ProductService, pk=pk)
    return render(request, 'product_service_confirm_delete.html', {'item': item})