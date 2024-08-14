"""
URL configuration for Playlist project.

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
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django_cron import CronJobManager
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('upload/', views.upload, name='upload'),
    path('youtube_auth/', views.youtube_auth, name='youtube_auth'),
    path('oauth2callback/', views.oauth2callback, name='oauth2callback'),
    path('playlist/', views.playlist, name='playlist'),
    path('logout/', views.logout_view, name='logout'),
    
    #Spotify Path
    path('spotify/', views.spotify_login, name='spotify'),
    path('callback/', views.callback, name='callback'),
    path('spotify_playlists/', views.spotify_playlists, name='spotify_playlists'),
    path('get_access_token/', views.get_access_token, name='get_access_token'),
    path('logout/', views.spotify_logout, name='spotify_logout'),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.index_title = "Cafe Database"

admin.site.site_header = "Cafe Admin"

#Only for development purposes
#if settings.DEBUG:
   # urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
