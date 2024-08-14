"""
WSGI config for Playlist project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Playlist.settings')

application = get_wsgi_application()


# Establishing An Upload Page to upload a file of any time 
    # Videos
    # Introduction - Django File Upload Tutorial 
    # Model Forms - Django File Upload Tutorial 
    # Django Full Course - 11 - Upload file/multiple files, save file to the model

# Only accepts an mp3 file 
# Displayed the file name that was uploaded
# Accepts multiple mp3 files which are saved in media folder locally

# Researching on the method of outputting the audio files from the page itself
    # How to store these files in a database and retrieving it from there

# Learning about API's and integration within Django
   # Videos
   # What is an API and how does it work? (In plain English)
   # How to use YouTubes API in a Django project

   


