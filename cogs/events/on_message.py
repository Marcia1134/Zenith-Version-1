import discord
from discord.ext import commands
from discord import app_commands
from json import load, dump

class OnMessage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener('on_message')
    async def on_message(self, message : discord.Message):
        if message.author.bot:
            return
        if message.channel.id == self.bot.config["channels"]["log"]:
            await message.delete()
            await message.channel.send("Please Reserve this channel for Bot Logs!", delete_after=10)

async def setup(bot):
    await bot.add_cog(OnMessage(bot))