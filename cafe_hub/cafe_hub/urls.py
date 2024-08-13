"""
URL configuration for cafe_hub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from inventory.views import Dashboard
from main import views
from main.admin_sites import branch_admin_sites,populate_branch_admin_sites

def generate_branch_admin_urls():
    if not branch_admin_sites:
        populate_branch_admin_sites()
    
    urlpatterns = []
    for branch_name, admin_site in branch_admin_sites.items():
        branch_name_safe = branch_name.replace(' ', '-')
        urlpatterns.append(path(f'{branch_name_safe}-admin/', admin_site.urls))
    return urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('accounts/', include('main.urls')),
    #path('', views.branchesView, name='index'),
    path('', include('main.urls')),
    
    path('menu/',include('preOrderApp.urls')),
    path('seating/',include('seating_main.urls')),
    path('inventory/', include('inventory.urls')),
    path('playlist/', include('Playlist.urls')),
    path('products_services/', include('productService.urls')),
    #path('branch/<int:pk>/', views.branch_detail, name='branch_detail'),
    #path('branch/<int:pk>/menu/', Menu.as_view(), name='menu'),
    #path('branch/<int:pk>/inventory/',Dashboard.as_view() , name='inventory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += generate_branch_admin_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

