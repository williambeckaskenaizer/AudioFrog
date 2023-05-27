import discord
from discord.ext import commands
from discord.utils import get
import os
from dotenv import load_dotenv
from music_player import Player
from search import search_for_song
from utils import connect_to_voice
from utils import build_song_embed
from utils import build_now_playing
from utils import build_playlist_embed
from now_playing import NowPlayingView
import yt_dlp

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents().all()
client = discord.Client(intents=intents)
bot = discord.Bot()
player = Player(guild=806314638895611904, bot=bot)

@bot.event
async def on_ready():
    bot.add_view(NowPlayingView(ctx=discord.context, player=player))
    os.system('cls' if os.name == 'nt' else 'clear')
    f = open('lucio.txt', 'r')
    contents = f.read()
    print(contents)
    print('                         Give yourself to the rhythm!            ')
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening, name="the healing beat"))

@bot.slash_command(name="addsong", description="Add a song to the playlist (Youtube URL)")
async def add_song(ctx: commands.Context, url):
    found_song = await search_for_song(url, 1)
    if found_song:
        found_song = found_song[0]
        player.add_to_playlist(found_song)
        embed = build_song_embed(found_song)
        embed.add_field(name='Postition:', value=player.playlist.__len__())
        await ctx.respond(f"**Added**", embed=embed)
        # await player.move_now_playing(ctx=ctx)
        
@bot.slash_command(name="ysearch", description="search youtube for a song!")
async def y_search(ctx: commands.Context, search):
    results = await search_for_song(search, 10)
    await ctx.respond(f"Found {len(results)} songs")
    
    
@bot.slash_command(name="playlist", description="View playlist")
async def view_playlist(ctx: commands.Context):
    curr_playlist = player.playlist.get_songs()
    titles = []
    # for song in curr_playlist:
    #     titles.append(song.title)
    embed = build_playlist_embed(curr_playlist)
    await ctx.respond(embed=embed)
    # await player.move_now_playing(ctx=ctx)

@bot.slash_command(name="play", description="Play current song in playlist")
async def play(ctx: commands.Context):
    await ctx.defer()
    player.guild = ctx.guild
    # await connect_to_voice(ctx=ctx, guild=ctx.guild, channel_name=ctx.channel)
    
    if len(player.playlist.get_songs()) == 0:
        await ctx.followup.send("**Playlist Empty!**")
    else:
        await ctx.followup.send("**Let's break it down!**")
        await player.play_song(player.playlist.get_songs()[0], ctx)
    
@bot.slash_command(name="skip", description="Next...")
async def pause(ctx: commands.Context):
    skipped = await player.skip_song(ctx=ctx)
    if skipped:
        await ctx.respond("Skipped.")
    else:
        await ctx.respond("Nothing is playing!")

@bot.slash_command(name="stop", description="Stop playing, clear the queue, leave voice.")
async def stop(ctx: commands.Context):
    stopped = await player.stop_and_clear(ctx)
    if stopped:
        await ctx.respond('Lata 🤙')
        voice = get(bot.voice_clients, guild=ctx.guild)
        if voice.is_connected():
            await voice.disconnect()
    else:
        await ctx.respond('Not currently in voice')
        
@bot.slash_command(name="pause", description="Pause whatever's playing")
async def pause(ctx: commands.Context):
    paused = await player.pause_song(ctx=ctx)
    if paused:
        await ctx.respond("On it boss👍")
    else:
        await ctx.respond("Is there something playing???")

@bot.slash_command(name="resume", description="Pick up where you left off (when you paused)")
async def resume(ctx: commands.Context):
    resumed = await player.resume_song(ctx=ctx)
    if resumed:
        await ctx.respond("Away we go!")
    else:
        await ctx.respond("Was there anything paused?")
        
@bot.slash_command(name="nowplaying", description="Displays the current song")
async def now_playing(ctx: commands.Context):
    now_playing = build_now_playing(player.current_song)
    await ctx.respond("**Now Playing:**", embed=now_playing)

@bot.slash_command(name="addspotifyplaylist", description="Add an entire spotify playlist to the queue")
async def add_spotify_playlist(ctx: commands.Context, playlist_link):
    await ctx.response.defer()
    embed = await player.add_spotify_playlist(ctx=ctx, playlist=playlist_link)
    await ctx.respond("***WOOOOO, Jackpot!***", embed=embed)
    
@bot.slash_command(name="shuffle", description="Randomize song queue order")
async def shuffle_songs(ctx: commands.Context):
    player.playlist.shuffle()
    await ctx.respond("**Shuffled!**")

bot.run(TOKEN)