from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from main.admin_sites import branch_admin_sites, populate_branch_admin_sites

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
    # path('', views.branchesView, name='index'),
    path('', include('main.urls')),
    path('menu/', include('preOrderApp.urls')),
    path('seating/', include('seating_main.urls')),
    path('inventory/', include('inventory.urls')),
    path('playlist/', include('Playlist.urls')),
    path('products_services/', include('productService.urls')),
    path('specials/', include('specials.urls')),
    path('choiceproducts/', include('choiceProducts.urls')),
    path('cafePosts/', include('cafePosts.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += generate_branch_admin_urls()

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)