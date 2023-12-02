import discord
from discord.ext import commands
from discord import app_commands
from cogs.advertising import db_wrapper as db

class GetLevel(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="get_level", description="Gets the level of an advertiser")
    async def get_level(self, interaction : discord.Interaction):
        '''
        Purpose: Gets the level of an advertiser

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == interaction.user.id).exists()  == False:
            await interaction.response.send_message("You have not yet signed up as an Advertiser. You can do that by using the `/ad_profile` command in any channel!")
        else:
            advertiser : db.Advertisers = db.Advertisers.get(user_id=interaction.user.id)
            embed = discord.Embed(title="Zenith Collective", description=f"```You are level {advertiser.level}!```", color=discord.Color.dark_purple())
            await interaction.response.send_message(embed=embed, ephemeral=False)

async def setup(bot):
    await bot.add_cog(GetLevel(bot))