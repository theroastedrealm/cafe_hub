# playlist/tasks.py
from celery import shared_task
from django.core.management import call_command

@shared_task
def delete_old_playlists():
    call_command('delete_old_playlists')
