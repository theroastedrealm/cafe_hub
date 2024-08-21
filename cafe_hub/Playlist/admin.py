from django.contrib import admin
from django.utils.html import format_html
from .models import SpotifyPlaylist, YoutubePlaylist
from .models import Playlist, Uploaded_file

class UploadedFileInline(admin.TabularInline):
    model = Uploaded_file
    search_fields = ('name', 'playlist__name')
    extra = 1  

class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_created')
    search_fields = ('name',)

    inlines = [UploadedFileInline]  

class Uploaded_file_Admin(admin.ModelAdmin):
    list_display = ('name', 'file_link', 'date_created', 'playlist')
    list_filter = ('playlist',)  

admin.site.register(Playlist, PlaylistAdmin)
admin.site.register(Uploaded_file, Uploaded_file_Admin)



class SpotifyPlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'link_html', 'date_created')
    search_fields = ('name',)

    def link_html(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)

    link_html.short_description = 'Link'

admin.site.register(SpotifyPlaylist, SpotifyPlaylistAdmin)



class YouTubePlaylistAdmin(admin.ModelAdmin):
    list_display = ('name', 'playlist_link', 'date_created')
    search_fields = ('name',)

    def playlist_link(self, obj):
        return format_html('<a href="{}" target="_blank">{}</a>', obj.link, obj.link)
    playlist_link.short_description = 'Playlist Link'  # Updated to reflect the new field name

admin.site.register(YoutubePlaylist, YouTubePlaylistAdmin)