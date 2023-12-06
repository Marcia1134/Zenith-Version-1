import discord 
from discord.ext import commands
from discord import app_commands
from database import wrapper

class AdDeleteMe(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot : commands.Bot = bot
    
    @commands.command(name="deleteme")
    async def deleteme_command(self, ctx : commands.Context):
        """
        Delets the user from the advertising database
        """
        try:
            advertiser : wrapper.Advertisers =  wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == ctx.author.id).get()
        except:
            await ctx.reply("Oops- we where unable to fetch your infomation!")
            return
        else:
            pass

        await ctx.send(f"We go your info!\nYou are advertiser: {advertiser.code}")

        advertiser.delete().execute()

        await ctx.send("Right, we think you are gone, but just incase, lets just check on more time!")

        try:
            advertiser : wrapper.Advertisers =  wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == ctx.author.id).get()
        except:
            await ctx.reply("It seems your infomation is gone! thanks for staying with us for so long! We hope to see you again soon!")
            return
        else:
            await ctx.reply("well this is slightly awkard... how come you are still around? huh... **contact an admin for some help**..")
            pass

async def setup(bot):
    await bot.add_cog(AdDeleteMe(bot))