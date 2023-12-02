import discord
from discord.ext import commands
from discord import app_commands
from cogs.advertising import db_wrapper as db

class DeleteAdvertiser(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="ad_profile_delete", description="Deletes an advertiser")
    async def delete_advertiser(self, interaction : discord.Interaction):
        '''
        Purpose: Creates a Advertister Profile using the id of the interaction.user

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == interaction.user.id).exists()  == False:
            await interaction.response.send_message("You have not yet signed up as an Advertiser. You can do that by using the `/ad_profile` command in any channel!")
        else:
            db.Advertisers.delete_by_id(interaction.user.id)
            await interaction.response.send_message(f"Deleted Advertiser Profile for {interaction.user.mention}")
            await interaction.user.send("All your infomation has been removed from our databases! If you would like to sign up again, please use the `/ad_profile` command! Thank you!")
            await self.bot.snowflake['log'].send(f"Deleted Advertiser Profile for {interaction.user.mention}")
    
async def setup(bot):
    await bot.add_cog(DeleteAdvertiser(bot))