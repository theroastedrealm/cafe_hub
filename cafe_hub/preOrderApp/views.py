
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Category, Item, Order
from django.contrib.auth.models import User

@login_required
def admin_page(request):
    if not request.user.is_staff:
        return redirect('menu_page')
    
    branch = request.user.branch
    if request.method == 'POST':
        if 'add_category' in request.POST:
            category_name = request.POST.get('category_name')
            Category.objects.create(name=category_name,branch=branch)
        elif 'add_item' in request.POST:
            item_name = request.POST.get('item_name')
            category_id = request.POST.get('category_id')
            category = Category.objects.get(id=category_id)
            Item.objects.create(name=item_name, category=category,branch=branch)
        elif 'confirm_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            order.status = 'confirmed'
            order.save()
        elif 'completed_order' in request.POST:
            order_id = request.POST.get('order_id')
            order = Order.objects.get(id=order_id)
            order.status = 'completed'
            order.save()
    
    categories = Category.objects.filter(branch=branch)
    orders = Order.objects.filter(branch=branch)
    return render(request, 'customer/admin_page.html', {'categories': categories, 'orders': orders})

@login_required
def menu_page(request):
    branch = request.user.branch

    categories = Category.objects.filter(branch=branch)
    if request.method == 'POST':
        items = request.POST.getlist('items')
        order = Order.objects.create(order_number='ORDER#' + str(Order.objects.count() + 1), customer=request.user,branch=branch)
        order.items.set(items)
        order.save()
        return redirect('order_confirmation', order_id=order.id)

    user_orders = Order.objects.filter(customer=request.user,branch=branch)
    return render(request, 'customer/menu_page.html', {'categories': categories, 'user_orders': user_orders})

@login_required
def order_confirmation(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'customer/order_confirmation.html', {'order': order})