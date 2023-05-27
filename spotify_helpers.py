import os
from dotenv import load_dotenv
import base64
from requests import post, get
import json
from discord import Embed
import asyncio

load_dotenv()


SPOTIFY_CLIENT_ID=os.getenv("SPOTIFY_ID")
SPOTIFY_CLIENT_SECRET=os.getenv("SPOTIFY_SECRET")
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'

def get_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")
    
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"grant_type":"client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

# def get_auth_header(token):
#     return {"Authorization":"Bearer " + token}

# https://open.spotify.com/playlist/7fr0AXpXthIMOkXujbrevy?si=a2d63f72586b4721

def get_playlist_info(token, playlist):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    url = f'{SPOTIFY_API_BASE_URL}/playlists/{playlist}'
    headers = {
        "Authorization":"Bearer " + token,
        "Content-Type": "application/json"
    }
    result = get(url, headers=headers)
    return result.json()

def get_playlist_items(token, playlist):
    headers = {
    'Authorization': f'Bearer {token}'
    }
    url = f'{SPOTIFY_API_BASE_URL}/playlists/{playlist}/tracks'
    tracks = []
    response = get(url, headers=headers)
    first_data = response.json()
    first_page = first_data.get('tracks')
    tracks.extend(first_page.get('items'))
    next_url = first_page.get('next')
    while next_url:
        response = get(next_url, headers=headers)
        data = response.json()
        items = data.get('items', [])
        # print(tracks_1.keys())
        tracks.extend(items)
        next_url = data.get('next')
    return tracks
    # url = f"https://api.spotify.com/v1/playlists/{playlist}"
    # headers = {
    #     "Authorization":"Bearer " + token,
    #     "Content-Type": "application/json"
    # }
    # result = get(url, headers=headers)
    # return result.json()
    
def process_playlist(playlist):
    songs = []
    for track_info in playlist:
        track_name = track_info["track"]["name"]
        artists = track_info["track"]["album"]["artists"]
        ret_artists = ""
        for artist in artists:
            ret_artists += f'{artist["name"]} '
        song = f'{track_name} by {ret_artists}'
        songs.append(song)
        
    return songs

def get_user_image(token, user_id):
    url = f"https://api.spotify.com/v1/users/{user_id}"
    headers = {
        "Authorization":"Bearer " + token,
        "Content-Type": "application/json"
    }
    result = get(url, headers=headers)
    image = result.json()["images"][0]["url"]
    return image

def get_playlist_embed(token, playlist):
    playlist_embed = Embed(color=0x1DB954)
    title = playlist["name"]
    thumbnail = playlist["images"][0]["url"]
    author = playlist["owner"]["display_name"]
    author_image = get_user_image(token, playlist["owner"]["id"])
    description = playlist["description"]
    tracks = playlist["tracks"]["total"]
    
    playlist_embed.set_author(name=author, icon_url=author_image)
    playlist_embed.set_thumbnail(url=thumbnail)
    playlist_embed.add_field(name=title, value=description)
    playlist_embed.add_field(name="Tracks", value=tracks, inline=False)
    return playlist_embed