from celery import shared_task
from django.core.management import call_command

def delete_old_playlists():
    call_command('delete_old_playlists')
