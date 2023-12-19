import discord
from discord import app_commands
from discord.ext import commands
from database import wrapper
from asyncio import sleep
from random import randint

class Pay(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="pay", description="Use this command when you are ready to pay!")
    async def pay_command(self, interaction : discord.Interaction):

        await interaction.response.defer()

        try:
            ticket_channel = wrapper.Ticket.select().where(wrapper.Ticket.channel_id == interaction.channel_id).get()
            print(ticket_channel.__dict__)
            print(ticket_channel.status)
        except Exception as e:
            await interaction.followup.send("This is not a ticket channel, please use this command in the channel of the service you would like to pay for.")
            print(e)
            return
        else:
            try:
                print(ticket_channel.channel_id)
            except Exception as e:
                await interaction.followup.send("This is not a ticket channel, please use this command in the channel of the service you would like to pay for.")
                print(e)
                print(ticket_channel)
                return
            else:
                pass

        if ticket_channel.channel_type == 0:
            await interaction.followup.send("This is a support ticket! You do not need to pay for this service!")
            return
        if ticket_channel.channel_type == 1:
            await interaction.followup.send("This is a moderation ticket! You do not need to pay for this service!")
            return
        if ticket_channel.channel_type == 2:
            await interaction.followup.send("Fetching your infomation! Please wait...")

            await sleep(randint(a=2, b=7))

            try:
                bot_instance : wrapper.CustomBot = wrapper.CustomBot.select().where(wrapper.CustomBot.ticket_id == interaction.channel.id).get()
                print(str(bot_instance))
            except:
                await interaction.followup.send('There has been an error, your custom bot infomation was not found!')
            else:
                embed = discord.Embed(title="Bot Information", color=discord.Color.blue())
                embed.add_field(name="Bot ID", value=f"```{bot_instance.bot_id}```")
                embed.add_field(name="Bot Name", value=f"```{bot_instance.bot_name}```")
                embed.add_field(name="Bot Description", value=f"```{bot_instance.bot_description}```", inline=False)
                embed.add_field(name="Bot Cost", value=f"```${bot_instance.cost}```")
                await interaction.followup.send(embed=embed)
            return
            
        if ticket_channel.channel_type == 3:
            interaction.followup.send("This version of Zenith Bot does not support custom servers yet!")
            return
        if ticket_channel.channel_type == 4:
            interaction.followup.send("Payment is not nessary for this service, if it is, a manual payment can be done via a staff member!")
        
async def setup(bot):
    await bot.add_cog(Pay(bot))