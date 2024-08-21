from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
import json
from django.urls import reverse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import requests
from django.shortcuts import render
from django.contrib import messages
from .models import Uploaded_file, Playlist





def index(request):
    return render(request, 'index.html')



#File Upload
def upload(request):
    uploaded_files = []
    if request.method == 'POST' and request.FILES.getlist('documents'):
        files = request.FILES.getlist('documents')
        playlist_name = request.POST.get('playlist_name')

        if len(files) > 3:
            messages.error(request, "You can only upload a maximum of 3 files. Please Try Again :)")
        elif len(files) == 0:
            messages.error(request, "No files were attached. Please Try Again :)")
        else:
            playlist = Playlist.objects.create(name=playlist_name)

            for file in files:
                # Save the file directly to the Uploaded_file model
                Uploaded_file.objects.create(
                    name=file.name,
                    file=file,
                    playlist=playlist
                )

            messages.success(request, f'Playlist "{playlist_name}" created successfully!')

    return render(request, 'upload.html', {'uploaded_files': uploaded_files})



# YouTube API 
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']
CLIENT_SECRETS_FILE = os.path.join(os.path.dirname(__file__), 'client_secret.json')

def load_client_config():
    with open(CLIENT_SECRETS_FILE, 'r') as file:
        client_config = json.load(file)
    return client_config

def youtube_auth(request):
    client_config = load_client_config()
    flow = Flow.from_client_config(client_config, scopes=SCOPES)
    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
    authorization_url, state = flow.authorization_url(access_type='offline', include_granted_scopes='true')
    request.session['state'] = state
    return redirect(authorization_url)

def oauth2callback(request):
    state = request.session['state']
    client_config = load_client_config()
    flow = Flow.from_client_config(client_config, scopes=SCOPES, state=state)
    flow.redirect_uri = request.build_absolute_uri(reverse('oauth2callback'))
    authorization_response = request.build_absolute_uri()
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials
    request.session['credentials'] = credentials_to_dict(credentials)
    return redirect('playlist')

def credentials_to_dict(credentials):
    return {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }


def playlist(request):
    if 'credentials' not in request.session:
        return redirect('youtube_auth')

    credentials = Credentials(**request.session['credentials'])
    youtube = build('youtube', 'v3', credentials=credentials)

    playlists_response = youtube.playlists().list(
        part="snippet",
        mine=True
    ).execute()

    playlists = []

    for playlist in playlists_response.get('items', []):
        playlist_id = playlist['id']
        playlist_name = playlist['snippet']['title']
        playlist_link = f"https://www.youtube.com/playlist?list={playlist_id}"  # Updated 'url' to 'link'

        # Save playlist to database
        YoutubePlaylist.objects.create(
            name=playlist_name,
            link=playlist_link,  # Updated 'url' to 'link'
        )

        # Fetch playlist items if needed
        playlist_items_response = youtube.playlistItems().list(
            part="snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50
        ).execute()

        videos = []
        for item in playlist_items_response.get('items', []):
            video_id = item['contentDetails']['videoId']
            try:
                video_response = youtube.videos().list(
                    part="status",
                    id=video_id
                ).execute()

                if (video_response['items'] and
                        video_response['items'][0]['status']['embeddable'] and
                        video_response['items'][0]['status']['privacyStatus'] == 'public'):
                    videos.append(item)
                else:
                    print(f"Video {video_id} is not embeddable or not public.")
            except Exception as e:
                print(f"Error fetching video {video_id}: {e}")

        if videos:
            playlist['videos'] = videos
            playlists.append(playlist)

    request.session['credentials'] = credentials_to_dict(credentials)

    return render(request, 'playlist.html', {'playlists': playlists})


def logout_view(request):
    # Check if credentials are stored in the session
    if 'credentials' in request.session:
        credentials = Credentials(**request.session['credentials'])
        
        # Revoke the refresh token if available
        if credentials.refresh_token:
            revoke_url = 'https://oauth2.googleapis.com/revoke'
            params = {'token': credentials.refresh_token}
            try:
                response = requests.post(revoke_url, params=params)
                response.raise_for_status()  # Raise an HTTPError for bad responses
                print("Token revoked successfully.")
            except requests.RequestException as e:
                print(f"Error revoking token: {e}")

        # Clear credentials from session
        del request.session['credentials']

    # Clear all session data
    request.session.flush()

    # Redirect to the homepage
    return redirect('index')





##############################################################################################################################
# Spotify# views.py
from django.shortcuts import redirect, render
from django.http import JsonResponse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json
import os
from datetime import datetime, timedelta
from .models import SpotifyPlaylist
from django.utils import timezone
import requests
from .models import YoutubePlaylist
from django.http import HttpResponse
import time



# Load Spotify credentials from the file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'spotify_credentials.json')) as f:
    credentials = json.load(f)

SPOTIFY_CLIENT_ID = credentials['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = credentials['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = credentials['SPOTIFY_REDIRECT_URI']
SPOTIFY_SCOPES = 'user-read-playback-state user-modify-playback-state playlist-read-private'

def spotify_login(request):
    auth_url = (
        f"https://accounts.spotify.com/authorize?response_type=code"
        f"&client_id={SPOTIFY_CLIENT_ID}"
        f"&redirect_uri={SPOTIFY_REDIRECT_URI}"
        f"&scope={SPOTIFY_SCOPES}"
    )
    return redirect(auth_url)


def callback(request):
    code = request.GET.get('code')
    if not code:
        return HttpResponse('Error: No code provided', status=400)

    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': SPOTIFY_REDIRECT_URI,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    refresh_token = token_json.get('refresh_token')
    expires_in = token_json.get('expires_in')

    if not access_token:
        return HttpResponse(f"Error: Unable to retrieve access token. Response: {token_json}", status=400)

    # Store the tokens and expiration time in the session
    request.session['spotify_access_token'] = access_token
    request.session['spotify_refresh_token'] = refresh_token
    request.session['spotify_token_expires_at'] = time.time() + expires_in

    return redirect('spotify_playlists')


def refresh_access_token(request):
    refresh_token = request.session.get('spotify_refresh_token')
    if not refresh_token:
        return False

    token_url = 'https://accounts.spotify.com/api/token'
    token_data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': SPOTIFY_CLIENT_ID,
        'client_secret': SPOTIFY_CLIENT_SECRET,
    }
    token_response = requests.post(token_url, data=token_data)
    token_json = token_response.json()

    access_token = token_json.get('access_token')
    expires_in = token_json.get('expires_in')

    if not access_token:
        return False

    # Update session with new access token and expiration time
    request.session['spotify_access_token'] = access_token
    request.session['spotify_token_expires_at'] = time.time() + expires_in

    return True

def spotify_playlists(request):
    access_token = request.session.get('spotify_access_token')
    token_expires_at = request.session.get('spotify_token_expires_at')

    if token_expires_at and time.time() > token_expires_at:
        refreshed = refresh_access_token(request)
        if not refreshed:
            return redirect('spotify')
        access_token = request.session.get('spotify_access_token')

    if not access_token:
        return redirect('spotify')

    # Fetch fresh playlist data from Spotify's API
    playlist_url = 'https://api.spotify.com/v1/me/playlists'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    playlist_response = requests.get(playlist_url, headers=headers)

    print(f"Status Code: {playlist_response.status_code}")
    print(f"Response Text: {playlist_response.text}")

    if playlist_response.status_code != 200:
        return HttpResponse(f"Error: Spotify API returned status code {playlist_response.status_code}. Response: {playlist_response.text}", status=playlist_response.status_code)

    try:
        playlist_json = playlist_response.json()
    except json.JSONDecodeError as e:
        return HttpResponse(f"Error decoding JSON: {e}", status=500)

    playlists = playlist_json.get('items', [])
    playlist_data = []

    for playlist in playlists:
        playlist_id = playlist['uri'].split(':')[-1]
        playlist_name = playlist['name']
        playlist_url = playlist['external_urls']['spotify']

        # Update the database to reflect any changes
        SpotifyPlaylist.objects.update_or_create(
            link=playlist_url,
            defaults={
                'name': playlist_name,
                'date_created': timezone.now()
            }
        )

        playlist_data.append({
            'name': playlist_name,
            'id': playlist_id,
            'url': playlist_url
        })
    
    context = {'playlists': playlist_data}
    return render(request, 'spotify.html', context)


######Admin Page#######
# views.py
from django.shortcuts import render, redirect
from .forms import PlaylistForm, UploadedFileForm, SpotifyPlaylistForm, YoutubePlaylistForm

def admin_homepage(request):
    if request.method == 'POST':
        playlist_form = PlaylistForm(request.POST)
        uploaded_file_form = UploadedFileForm(request.POST, request.FILES)
        spotify_playlist_form = SpotifyPlaylistForm(request.POST)
        youtube_playlist_form = YoutubePlaylistForm(request.POST)
        
        if playlist_form.is_valid():
            playlist_form.save()
            return redirect('admin_homepage')

        if uploaded_file_form.is_valid():
            uploaded_file_form.save()
            return redirect('admin_homepage')

        if spotify_playlist_form.is_valid():
            spotify_playlist_form.save()
            return redirect('admin_homepage')

        if youtube_playlist_form.is_valid():
            youtube_playlist_form.save()
            return redirect('admin_homepage')

    else:
        playlist_form = PlaylistForm()
        uploaded_file_form = UploadedFileForm()
        spotify_playlist_form = SpotifyPlaylistForm()
        youtube_playlist_form = YoutubePlaylistForm()

    return render(request, 'admin_homepage.html', {
        'playlist_form': playlist_form,
        'uploaded_file_form': uploaded_file_form,
        'spotify_playlist_form': spotify_playlist_form,
        'youtube_playlist_form': youtube_playlist_form
    })
