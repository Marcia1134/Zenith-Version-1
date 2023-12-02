import discord
from discord.ext import commands
from cogs.advertising import db_wrapper as db

class AdHelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="adhelp", description="Displays the help message")
    async def adhelp(self, ctx : commands.Context):
        '''
        Purpose: Displays the help message

        Parameters: ctx - discord.Context

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == ctx.author.id).exists()  == False:
            await ctx.send("You have not yet signed up as an Advertiser. You can do that by using the `/ad_profile` command in any channel!")
            return
        embed = discord.Embed(title="Zenith Collective", description=f"Hope this Helps!", color=discord.Color.dark_purple())
        embed.add_field(name="Help and Server Assistance -", value="If you ever need help with anything regarding Advertising, please use the `-adhelp` command here!")
        embed.add_field(name="Advertising Rules -", value="Just make sure you are being respectful, sensible, and proffesional. For example, don't spam! Make sure you are advertising in advertising spaces only. If you are unsure, please use the help command!")
        embed.add_field(name="Advertising Tips -", value="Just some tips! Make sure that you target the right people! Join new servers or servers that are looking for partnerships! Also keep in mind Advertising rules for each server!")
        embed.add_field(name="Generating Referal Codes -", value="You can use `/get_code` on the server to get a referal code!")
        embed.add_field(name="Other Useful Commands - ", value="You can use `/level` to display your current level! \n You can use `/ad_profile_delete` to delete your current profile. \n You can use the '/adhelp' command to see this message again at any point!")
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AdHelpCommand(bot))