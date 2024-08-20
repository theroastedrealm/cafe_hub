from django.db import models

class Uploaded_file(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name
    
class SpotifyPlaylist(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.name

class YoutubePlaylist(models.Model):
    name = models.CharField(max_length=255)
    link = models.URLField()

    def __str__(self):
        return self.name