import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class AdDisplay(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot

    @app_commands.command(name = "ad_display", description = "Displays an advertisement")
    async def ad(self, interaction : discord.Interaction, clean : bool =False):
        
        try:
            advertiser : wrapper.Advertisers = wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == interaction.user.id).get()
        except Exception as e:
            print(e)
            await interaction.response.send_message("You need to create a profile first! Use `/ad_create`!")
            return
        else:
            if advertiser == None:
                await interaction.response.send_message("You need to create a profile first! Use `/ad_create`!")
                return
        
        earning = advertiser.level
        if earning >= 14:
            earning = 20
        else:
            earning += 5
        
    
        embed = discord.Embed(title="Advertising Profile", color=discord.Color.purple())
        embed.add_field(name="Email", value=f'```{advertiser.email}```')
        embed.add_field(name="Code", value=f'```{advertiser.code}```')
        embed.add_field(name="Level", value=f'```{advertiser.level}```')
        embed.add_field(name="Cut", value=f'```{earning}%```')
        embed.add_field(name="Succesful Clients", value=f'```{advertiser.client_count}```')
    
        await interaction.response.send_message(embed=embed)
    
async def setup(bot : commands.Bot):
    await bot.add_cog(AdDisplay(bot))