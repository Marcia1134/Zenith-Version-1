import discord
from discord.ext import commands
from discord import app_commands
from cogs.advertising import db_wrapper as db

class AnnoucementModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Create an Announcement!")
        self.atitle = discord.ui.TextInput(label="Enter your title here!", min_length=10, max_length=100)
        self.announcement = discord.ui.TextInput(label="Enter your announcement here!", min_length=10, max_length=1000, style=discord.TextStyle.paragraph)
        self.add_item(self.atitle)
        self.add_item(self.announcement)
        

    async def on_submit(self, interaction : discord.Interaction):

        await interaction.response.send_message("Created Announcement!", ephemeral=False, delete_after=1)

        await interaction.channel.send(embed=discord.Embed(title=self.atitle.value, description=f"```{self.announcement.value}```", color=discord.Color.purple()))

        



class CreateAnnoucement(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="create_announcement", description="Creates an announcement")
    async def create_announcement(self, interaction : discord.Interaction):
        '''
        Purpose: Creates an announcement

        Parameters: interaction - discord.Interaction

        Returns: None
        '''     
        await interaction.response.send_modal(AnnoucementModal())
        await self.bot.snowflake['log'].send(f"Created Announcement for {interaction.user.mention}")

async def setup(bot):
    await bot.add_cog(CreateAnnoucement(bot))