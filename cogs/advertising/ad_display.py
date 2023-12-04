import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class AdDisplay(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot

    @app_commands.command(name = "ad_display", description = "Displays an advertisement")
    async def ad(self, interaction : discord.Interaction):
        try:
            advertiser : wrapper.Advertisers = wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == interaction.user.id).get()
        except Exception as e:
            print(e)
            await interaction.response.send_message("You need to create a profile first! Use `/ad_create`!")
        else:
            if advertiser == None:
                await interaction.response.send_message("You need to create a profile first! Use `/ad_create`!")
        earning = advertiser.level
        if earning >= 14:
            earning = 20
        else:
            earning += 5
        embed = discord.Embed(title = "Advertisement Profile", description = f"Your Advertising Code is; `{advertiser.code}`\nYou are now level `{advertiser.level}`!\nWith `{advertiser.client_count}` clients under your belt you are earning up to `{earning}%` per client!\nWhenever you do earn we send it to `{advertiser.email}`", color = discord.Color.blue())
        
        await interaction.response.send_message(embed=embed)
    
async def setup(bot : commands.Bot):
    await bot.add_cog(AdDisplay(bot))