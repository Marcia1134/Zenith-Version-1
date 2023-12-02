import discord
from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="gethelp", description="Displays the help message")
    async def help(self, ctx : commands.Context, *args):
        if ctx.channel.type == discord.ChannelType.private:
            embed = discord.Embed(title="Zenith Collective", description="We have sent a message to the mod team letting them know you need help! Please wait for assistance.", color=discord.Color.dark_purple())
            await ctx.send(embed=embed)
            embed = discord.Embed(title="Zenith Collective Support", description=f"{ctx.author.mention} needs support! Pinging all {self.bot.snowflake['mod'].mention}", color=discord.Color.orange())
            embed.add_field(name="Message:", value=f"```{str(args)}```", inline=False)
            embed.add_field(name="Creating a Ticket: ", value="```Use the /create_ticket command to create a support ticket with the mentioned user```", inline=False)
            await self.bot.snowflake['log'].send(embed=embed)
        else:
            await ctx.send("This command is not usable on a server! Please use this command in a DM with the bot instead!")

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))