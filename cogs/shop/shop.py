import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord import ButtonStyle
from database import wrapper

class Shop(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
    
    class ShopView(ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @ui.button(label="Custom Discord Bot", style=ButtonStyle.blurple, emoji="🤖")
        async def CDB_button(self, interaction : discord.Interaction, button : discord.Button):
            await interaction.response.send_message(f"{button.label}")

    @app_commands.command(name="shop", description="Displays the entire shop!")
    async def view_shop_command(self, interaction : discord.Interaction, guide : bool = False):
        
        await interaction.response.send_message("shop", view=self.ShopView())

async def setup(bot):
    await bot.add_cog(Shop(bot))