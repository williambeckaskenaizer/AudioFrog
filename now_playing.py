import discord
from discord.ext import commands
from discord.utils import get

class NowPlayingView(discord.ui.View):
    def __init__(self, ctx: commands.Context, player):
        
        super().__init__(timeout=None)
        self.ctx = ctx
        self.player = player
    
    @discord.ui.button(label="Pause", style=discord.ButtonStyle.primary, emoji='⏸️', custom_id='pause-b')
    async def pause_callback(self, button, interaction: discord.Interaction):
        await self.player.pause_song(ctx=self.ctx)
        await interaction.response.defer()
        
    @discord.ui.button(label="Resume", style=discord.ButtonStyle.green, emoji='▶️', custom_id='resume-b')
    async def resume_callback(self, button, interaction: discord.Interaction):
        await self.player.resume_song(ctx=self.ctx)
        await interaction.response.defer()
        
    @discord.ui.button(label="Skip", style=discord.ButtonStyle.secondary, emoji='⏩',  custom_id='skip-b')
    async def skip_callback(self, button, interaction: discord.Interaction):
        await interaction.response.defer()
        await self.player.skip_song(ctx=self.ctx)
        
    @discord.ui.button(label="Shuffle", style=discord.ButtonStyle.secondary, emoji='🔀',  custom_id='shuffle-b')
    async def shuffle_callback(self, button, interaction: discord.Interaction):
        self.player.playlist.shuffle()
        await interaction.response.send_message("**Shuffled!**")
        await self.player.move_now_playing(ctx=self.ctx)
        
    @discord.ui.button(label="Stop", style=discord.ButtonStyle.danger, emoji='⏹️', custom_id='stop-b')
    async def stop_callback(self, button, interaction: discord.Interaction):
        stopped = await self.player.stop_and_clear(ctx=self.ctx)
        if stopped:
            await interaction.response.send_message('Lata 🤙')
            voice = get(interaction.client.voice_clients, guild=interaction.guild)
            if voice.is_connected():
                await voice.disconnect()
        else:
            await interaction.response.send_message('Not currently in voice')
            await interaction.response.defer()
        
    
        
    
