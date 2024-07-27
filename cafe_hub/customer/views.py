
from django.shortcuts import get_object_or_404, render
from django.views import View 
from django.views import generic

from main.models import Branch
from customer.models import MenuItem
# Create your views here.

class Index(View):
    def get(self, request, *args,**kwarfgs):
        return render(request, "customer/index.html")



class Menu(generic.ListView):
    model = MenuItem
    context_object_name = 'menu_list'   
    #queryset = MenuItem.objects.all()
    template_name = 'customer/menu.html'
      


class Order(View): 
    model=MenuItem
    context_object_name='food_list'
    queryset = non_coffee=MenuItem.objects.filter(category__name__contains='Food')
    template_name = 'customer/menu.html'  

    def get(self, request, *args,**kwarfgs):
        non_coffee=MenuItem.objects.filter(category__name__contains='Non-Coffee')
        coffee=MenuItem.objects.filter(category__name__contains='Coffee')
        food=MenuItem.objects.filter(category__name__contains='Food')
    

        context = {
            'non_coffee':non_coffee,
            'coffee':coffee,
            'food':food,
        }

        return render(request, 'customer/menu.html',context)
    
