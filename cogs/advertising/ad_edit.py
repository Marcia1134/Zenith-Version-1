import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper as db

class AdEdit(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="ad_edit", description="Edits an ad")
    async def ad_edit(self, interaction : discord.Interaction, email : str):
        '''
        Purpose: Edits an ad

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == interaction.user.id).exists()  == False:
            await interaction.response.send_message("You have not yet signed up as an Advertiser. You can do that by using the `/ad_profile` command in any channel!")
            return
        else:
            advertiser : db.Advertisers = db.Advertisers.get(user_id=interaction.user.id)
            db.Advertisers.update(emails=email).where(db.Advertisers.user_id == interaction.user.id).execute()
            interaction.response.send_message(f"Edited email to {email}", ephemeral=False)
            await self.bot.snowflake['log'].send(f"Created Ad for {interaction.user.mention}")
    
async def setup(bot):
    await bot.add_cog(AdEdit(bot))