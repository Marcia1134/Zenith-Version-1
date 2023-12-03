import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper as db

class Guide(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot
    
    @app_commands.command(name="guide", description="Sends the guide")
    async def guide(self, interaction : discord.Interaction):
        '''
        Purpose: Sends the guide

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        embed = discord.Embed(title="Zenith Collective", description="```Welcome to the Zenith Collective!```", color=discord.Color.dark_purple())
        embed.add_field(name="What is the Zenith Collective?", value="```We are a development agancey focused on keeping everything you need for a professional discord server under one roof!```", inline=False)
        embed.add_field(name="How do I get started?", value="```If you are looking for a bit of spare cash you can start with our advertising accounts! Using the '/ad_profile', you can get started with earning some money!```", inline=False)
        embed.add_field(name="How do I get paid?", value="```Your level + 5 is the percentage of whatever you get payed!* This goes up until level 15! Check your level by using the /get_level command!```", inline=False)
        embed.add_field(name="How do I get support?", value="```You can get support by using the '-adhelp' command!```", inline=False)
        embed.add_field(name="Invite Link", value="```https://discord.gg/yEGmrzzj7v```", inline=False)
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("sent!", ephemeral=False, delete_after=1)

async def setup(bot):
    await bot.add_cog(Guide(bot))