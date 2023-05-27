from song import Song
from discord import Embed
from discord.ext import commands

guild_to_settings = {}

def build_song_embed(song: Song):
    song_embed = Embed(color=0xe899ff, title=song.title)
    song_embed.set_thumbnail(url=song.thumbnail)
    return song_embed

def build_now_playing(song: Song):
    now_playing_embed = Embed(color=0xe899ff)
    now_playing_embed.add_field(name=song.title, value=song.description, inline=False)
    now_playing_embed.set_thumbnail(url=song.thumbnail)
    now_playing_embed.add_field(name='Duration', value=song.duration)
    now_playing_embed.set_author(name=song.uploader, icon_url=song.uploader_img)
    return now_playing_embed
    
def build_playlist_embed(songs: list[Song]):
    playlist_embed = Embed(color=0x85c952)
    playlist_embed.set_author(name=f'{len(songs)} songs in queue', icon_url='https://icon-library.com/images/playlist-icon/playlist-icon-12.jpg')
    for pos, song in enumerate(songs):
        playlist_embed.add_field(name=f'{pos + 1}. {song.title}', value='', inline=False)
    return playlist_embed

async def connect_to_voice(guild, channel_name, ctx, switch=False, default=True):
    for channel in guild.voice_channels:
        if str(channel.name).strip() == str(channel_name).strip():
            if switch:
                try:
                    await guild.voice_client.disconnect()
                except:
                    await ctx.send("Not connect :()")

            await channel.connect()
            return

    if default:
        try:
            await guild.voice_channels[0].connect()
        except:
            print("already in channel.")
    else:
        await ctx.send("Couldn't find channel??")
        
def get_guild(bot, command):
    if command.guild is not None:
        return command.guild
    for guild in bot.guilds:
        for channel in guild.voice_channels:
            if command.author in channel.members:
                return guild
    return None

async def play_check(ctx):

    author_voice = ctx.author.voice
    bot_vc = ctx.guild.voice_client.channel
    if author_voice == None:
        await ctx.send("NOT IN VC")
        return False
    elif ctx.author.voice.channel != bot_vc:
        await ctx.send("NOT IN VC")
        return False

    
