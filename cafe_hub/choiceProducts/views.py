from django.shortcuts import redirect, render

from choiceProducts.models import Product

# Create your views here.

def productHomepage(request):
    branch = request.user.branch
    products = Product.objects.filter(branch=branch)
    is_staff = request.user.groups.filter(name__in=['uber-user', 'admin']).exists()
    context = {
        "products": products,
        "is_staff": is_staff,
    }
    return render(request, "admin_page.html", context)

def add_product(request):
    if not request.user.is_staff:
        return redirect('customer_page')

    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        amazon_link = request.POST.get('amazon_link')
        image = request.FILES.get('image')
        branch = request.user.branch
        product=Product.objects.create(name=name, description=description, amazon_link=amazon_link, image=image,branch=branch)
        product.save()
    return redirect('/choiceproducts/')

def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)
    product.delete()
    return redirect('/choiceproducts/')

def product_list(request):
    branch=request.user.branch 
    products = Product.objects.filter(branch=branch)
    return render(request, 'customer_page.html', {'products': products})