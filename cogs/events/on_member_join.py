import discord
from discord.ext import commands

class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_member_join')
    async def on_member_join(self, member : discord.Member):
        embed = discord.Embed(title="Zenith Collective", description=f"Welcome to the server {member.mention}!", color=discord.Color.dark_purple())
        if member.avatar.url == None:
            embed.set_thumbnail(url=member.default_avatar.url)
        else:
            embed.set_thumbnail(url=member.avatar.url)
        await self.bot.snowflake['welcome'].send(embed=embed)
        await member.add_roles(self.bot.snowflake['member'])
        embed = discord.Embed(title="Zenith Collective", description=f"Welcome to the Zenith Collective Server {member.display_name}!", color=discord.Color.dark_purple())
        embed.add_field(name="Help and Server Assistance -", value="If you need any assistance with the server please send a message containing: `!help` and what you need assistance with (for general assistance, you may leave it blank)\nExample: `!help I need help with the server rules`")
        await member.send(embed=embed)
        embed = discord.Embed(title="Zenith Collective", description=f"How to enable an advertising code!", color=discord.Color.dark_purple())
        embed.add_field(name="If you have recieved a code;", value="If you have recieved a code, please use the `/login` command to get started!")
        embed.add_field(name="If you have not recieved a code;", value="In order to make a purchase through Zenith Collective you first need a code. To get a code from the server, please use the `/servercode` command!")
        await member.send(embed=embed)

async def setup(bot):
    await bot.add_cog(OnMemberJoin(bot))