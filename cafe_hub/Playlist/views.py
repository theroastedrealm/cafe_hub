from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
import os
import json
from django.urls import reverse
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
import requests


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

#File Upload
def upload(request):
    uploaded_files = []
    if request.method == 'POST' and request.FILES.getlist('documents'):
        files = request.FILES.getlist('documents')
        file_save = FileSystemStorage()
        for file in files:
            file_save.save(file.name, file)
            uploaded_files.append(file.name)
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
    # Check if the user is authenticated (i.e., has Google credentials)
    if 'credentials' not in request.session:
        return redirect('youtube_auth')  # Redirect to Google OAuth flow if not authenticated

    credentials = Credentials(**request.session['credentials'])
    youtube = build('youtube', 'v3', credentials=credentials)

    # Get playlists
    playlists_response = youtube.playlists().list(
        part="snippet",
        mine=True
    ).execute()

    playlists = []

    # Get videos from all the playlists available
    for playlist in playlists_response.get('items', []):
        playlist_id = playlist['id']
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

                # Check if the video is embeddable and public
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

    # Store credentials in session
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






# Spotify
# views.py
from django.shortcuts import redirect, render
from django.http import JsonResponse
import spotify
from spotify.oauth2 import SpotifyOAuth
import json
import os
from datetime import datetime, timedelta

# Load credentials from JSON file
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(BASE_DIR, 'spotify_credentials.json')) as f:
    credentials = json.load(f)

SPOTIFY_CLIENT_ID = credentials['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = credentials['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = credentials['SPOTIFY_REDIRECT_URI']
# Define Spotify scopes as a constant
SPOTIFY_SCOPES = 'user-read-playback-state user-modify-playback-state playlist-read-private'



def spotify_login(request):
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES
    )
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

def callback(request):
    sp_oauth = SpotifyOAuth(
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        redirect_uri=SPOTIFY_REDIRECT_URI,
        scope=SPOTIFY_SCOPES
    )
    code = request.GET.get('code')
    token_info = sp_oauth.get_access_token(code)
    request.session['token_info'] = token_info
    return redirect('spotify_playlists')

def spotify_playlists(request):
    token_info = request.session.get('token_info')
    if not token_info or is_token_expired(token_info):
        return redirect('spotify')
    
    sp = spotify.Spotify(auth=token_info['access_token'])
    playlists_data = sp.current_user_playlists()
    
    playlists = []
    for playlist in playlists_data['items']:
        tracks = sp.playlist_tracks(playlist['id'])
        track_uris = [track['track']['uri'] for track in tracks['items']]
        playlists.append({
            'id': playlist['id'],
            'name': playlist['name'],
            'external_urls': playlist['external_urls'],
            'tracks': track_uris
        })
    
    return render(request, 'spotify.html', {'playlists': playlists, 'access_token': token_info['access_token']})


def is_token_expired(token_info):
    # Check if the token has expired
    expiration_time = datetime.fromtimestamp(token_info['expires_at'])
    return datetime.now() > expiration_time

def refresh_access_token(sp_oauth, refresh_token):
    token_info = sp_oauth.refresh_access_token(refresh_token)
    return token_info

def get_access_token(request):
    token_info = request.session.get('token_info')
    return JsonResponse({'access_token': token_info['access_token']})
