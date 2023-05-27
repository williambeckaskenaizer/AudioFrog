from playlist import Playlist
from song import Song
from enum import Enum
from discord.ext import commands
from now_playing import NowPlayingView
import utils
import discord
import yt_dlp
import asyncio
import spotify_helpers
from search import search_for_song

class Player:
    def __init__(self, guild: discord.guild, bot: discord.bot):
        self.playlist = Playlist()
        self.guild = guild
        self.current_song = None
        self.bot = bot
        self.spotify_token = spotify_helpers.get_token()
        self.now_playing_id = None
        self.playing_status = None
        
    
    def set_guild(self, guild):
        self.guild = guild
    
    def add_to_playlist(self, song: Song):
        self.playlist.add_song(song)
        
    def next_song(self, error, ctx: commands.Context):
        next_song = self.playlist.next()

        self.current_song = None

        if next_song is None:
            return

        coro = self.play_song(next_song, ctx=ctx)
        self.bot.loop.create_task(coro)
        
        
    async def playlist_ended(self, ctx: commands.Context):
        now_playing_message = await ctx.fetch_message(self.now_playing_id)
        await now_playing_message.edit(content="**Playlist Ended.**", embed=None, view=None)

    async def play_song(self, song: Song, ctx: commands.Context): #
        if song.link:
            self.current_song = song
        else:
            searched = await search_for_song(song.title, 1)
            searched = searched[0]
            self.current_song = searched
        
        # self.playlist.playhistory.append(self.current_song)
        
        try:
            downloader = yt_dlp.YoutubeDL({'format': 'bestaudio', 'title': True})
            r = downloader.extract_info(self.current_song.link, download=False)
        except:
            await asyncio.wait(1)
            downloader = yt_dlp.YoutubeDL({'title': True})
            r = downloader.extract_info(self.current_song.link, download=False)
        
        
        vc = ctx.voice_client # define our voice client

        if not vc: # check if the bot is not in a voice channel
            vc = await ctx.author.voice.channel.connect()
        # connection = await vc.connect(reconnect=True, timeout=20)
        vc.play(discord.FFmpegAudio(
            r['url'], before_options='-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'), after=lambda e: self.next_song(e, ctx=ctx))
        
        if self.now_playing_id is not None:
            now_playing_message = await ctx.fetch_message(self.now_playing_id)
            await now_playing_message.delete()
        np_embed = utils.build_now_playing(song=self.current_song)
        self.playing_status = "**Now Playing:**"
        message = await ctx.send(content=self.playing_status, embed=np_embed, view=NowPlayingView(ctx=ctx, player=self))
        self.now_playing_id = message.id
        self.playlist.song_queue.popleft()
    
    async def skip_song(self, ctx: commands.Context):
        
        current_guild = utils.get_guild(self.bot, ctx)
        
        if await utils.play_check(ctx) == False:
            return False
        
        
        if current_guild is None:
            await ctx.send("couldn't get server")
        
        if current_guild.voice_client is None or (not current_guild.voice_client.is_paused() and not current_guild.voice_client.is_playing()):
            await ctx.send("Playlist Empty!")
            return False
        
        now_playing_message = await ctx.fetch_message(self.now_playing_id)
        await now_playing_message.edit(content="**Skipping...**")
        self.guild.voice_client.stop()
        return True
    
    async def stop_and_clear(self, ctx: commands.Context):
        if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) is None:
            return False
        self.playlist.next()
        await self.clear_queue()
        self.guild.voice_client.stop()
        now_playing_message = await ctx.fetch_message(self.now_playing_id)
        await now_playing_message.edit(content="**Stopped.**",view=None, embed=None)
        return True
        
    async def clear_queue(self):
        self.playlist.song_queue.clear()
        
    async def pause_song(self, ctx: commands.Context):
        try:    
            voice_channel = self.guild.voice_client
            voice_channel.pause()
            now_playing_message = await ctx.fetch_message(self.now_playing_id)
            await now_playing_message.edit(content="**Paused**")
            self.playing_status = "**Paused.**"
            return True
        except:
            return False
    
    async def resume_song(self, ctx: commands.Context):
        try:
            voice_channel = self.guild.voice_client
            voice_channel.resume()
            now_playing_message = await ctx.fetch_message(self.now_playing_id)
            self.playing_status = "**Now Playing:**"
            await now_playing_message.edit(content=self.playing_status)
            return True
        except:
            return False
        
    async def add_spotify_playlist(self, ctx: commands.Context, playlist):
        # try:
        playlist_id = playlist.split("/")[-1]
        ret_playlist_info = spotify_helpers.get_playlist_info(token=self.spotify_token, playlist=playlist_id)
        if ret_playlist_info:
            ret_playlist_items = spotify_helpers.get_playlist_items(token=self.spotify_token, playlist=playlist_id)
            embed = spotify_helpers.get_playlist_embed(token=self.spotify_token, playlist=ret_playlist_info)
            playlist_names = spotify_helpers.process_playlist(ret_playlist_items)
            for item in playlist_names:
                new_song = Song(title=item, link='', thumbnail='', description='', duration='', uploader='', uploader_img='')
                self.playlist.add_song(new_song)
        return embed

    async def move_now_playing(self, ctx: commands.Context):
        if discord.utils.get(ctx.bot.voice_clients, guild=ctx.guild) is not None and self.current_song is not None:
            new_now_playing = utils.build_now_playing(self.current_song)
            current_now_playing = await ctx.fetch_message(self.now_playing_id)
            await current_now_playing.delete()
            new_np_message = await ctx.send(content=self.playing_status, embed=new_now_playing, view=NowPlayingView(ctx=ctx, player=self))
            self.now_playing_id = new_np_message.id

    async def get_now_playing(self):
        return self.current_song