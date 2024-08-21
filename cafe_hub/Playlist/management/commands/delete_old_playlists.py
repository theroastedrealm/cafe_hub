from django.core.management.base import BaseCommand
from django.utils import timezone
from Playlist.models import SpotifyPlaylist, YoutubePlaylist, Uploaded_file, Playlist

class Command(BaseCommand):
    help = 'Delete playlists older than 3 hours'

    def handle(self, *args, **kwargs):
        threshold_time = timezone.now() - timezone.timedelta(hours=3)
        SpotifyPlaylist.objects.filter(date_created__lt=threshold_time).delete()
        YoutubePlaylist.objects.filter(date_created__lt=threshold_time).delete()
        Uploaded_file.objects.filter(date_created__lt=threshold_time).delete()
        Playlist.objects.filter(date_created__lt=threshold_time).delete()
        self.stdout.write(self.style.SUCCESS('Successfully deleted playlists older than 3 hours'))
