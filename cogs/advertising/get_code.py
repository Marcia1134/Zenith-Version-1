import discord
from discord.ext import commands
from discord import app_commands
from cogs.advertising import db_wrapper as db
from random import randint

class CreateCode(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="get_code", description="Creates a code")
    async def create_code(self, interaction : discord.Interaction):
        '''
        Purpose: Creates a code

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == interaction.user.id).exists()  == False:
            await interaction.response.send_message("You have not yet signed up as an Advertiser. You can do that by using the `/ad_profile` command in any channel!")
            return
        
        codes = db.Advertisers.select(db.Advertisers.code)
        code = randint(100000, 999999)
        while codes.where(db.Advertisers.code == code).exists():
            code = randint(100000, 999999)
        db.Advertisers.update(code=code).where(db.Advertisers.user_id == interaction.user.id).execute()
        await interaction.response.send_message(f"Created Code for {interaction.user.mention}\n\n{code}", ephemeral=False)
        await self.bot.snowflake['log'].send(f"Created Code for {interaction.user.mention}")

async def setup(bot):
    await bot.add_cog(CreateCode(bot))