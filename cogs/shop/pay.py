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
            ticket_channel : wrapper.Ticket = wrapper.Ticket.select().where(wrapper.Ticket.channel_id == interaction.channel_id)
        except:
            await interaction.followup.send("This is not a ticket channel, please use this command in the channel of the service you would like to pay for.")
            return
        else:
            pass

        if ticket_channel.type == 0:
            await interaction.followup.send("This is a support ticket! You do not need to pay for this service!")
            return
        if ticket_channel.type == 1:
            await interaction.followup.send("This is a moderation ticket! You do not need to pay for this service!")
            return
        if ticket_channel.type == 2:
            await interaction.followup.send("Fetching your infomation! Please wait...")

            await sleep(randint(a=2, b=7))

            try:
                bot_instance : wrapper.CustomBot = wrapper.CustomBot.select().where(wrapper.CustomBot.ticket_id == interaction.channel.id)
            except:
                await interaction.followup.send('There has been an error, your custom bot infomation was not found!')
            else:
                await interaction.followup.send(f"Your infomation has been found! Your Bot ID is {bot_instance.bot_id}")
            return
            
        if ticket_channel.type == 3:
            interaction.followup.send("This version of Zenith Bot does not support custom servers yet!")
            return
        if ticket_channel.type == 4:
            interaction.followup.send("Payment is not nessary for this service, if it is, a manual payment can be done via a staff member!")