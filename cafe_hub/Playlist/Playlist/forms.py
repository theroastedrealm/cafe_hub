from django import forms  

class UploadFileForm(forms.Form):
    file = forms.FileField()


from django import forms
from .models import Playlist, Uploaded_file, SpotifyPlaylist, YoutubePlaylist

class PlaylistForm(forms.ModelForm):
    class Meta:
        model = Playlist
        fields = ['name', 'date_created']

class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = Uploaded_file
        fields = ['name', 'file_link', 'date_created', 'playlist']

class SpotifyPlaylistForm(forms.ModelForm):
    class Meta:
        model = SpotifyPlaylist
        fields = ['name', 'link', 'date_created']

class YoutubePlaylistForm(forms.ModelForm):
    class Meta:
        model = YoutubePlaylist
        fields = ['name', 'link', 'date_created']

