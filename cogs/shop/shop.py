import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from database import wrapper

class Shop(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
    
    # waiting for further development

    @app_commands.command(name="shop", description="Displays the entire shop!")
    async def view_shop_command(self, interaction : discord.Interaction, guide : bool = False):
        
        interaction.response.send_message("shop")

async def setup(bot):
    await bot.add_cog(bot)