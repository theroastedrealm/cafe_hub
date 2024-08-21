from django.db import models
from django.utils import timezone

class Playlist(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

class Uploaded_file(models.Model):
    name = models.CharField(max_length=255)
    file_link = models.URLField(max_length=500)
    date_created = models.DateTimeField(default=timezone.now)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return self.name




class SpotifyPlaylist(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name



class YoutubePlaylist(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()  # Renamed from url to link
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
