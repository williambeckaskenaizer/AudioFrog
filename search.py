import discord
import yt_dlp
from youtubesearchpython import VideosSearch
from song import Song


'''
Need a Playlist class
need that playlist class to take Songs
'''

async def search_for_song(song, limit):
    videosSearch = VideosSearch(song, limit=limit)
    res = videosSearch.result()
    found_songs = []
    if res:
        for result in res['result']:
            found_song = Song(title=result['title'], link=result['link'], thumbnail=result['thumbnails'][0]['url'], duration=result['duration'], uploader=result['channel']['name'], uploader_img=result['channel']['thumbnails'][0]['url'], description=result['descriptionSnippet'][0]['text'] if result['descriptionSnippet'] else "no description available")
            found_songs.append(found_song)
        return found_songs