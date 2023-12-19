import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class Cost(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @app_commands.command(name="cost", description="Use this command to set the cost of a service!")
    async def apply_cost(self, interaction : discord.Interaction, cost : int):
        await interaction.response.defer()
        try:
            ticket_channel = wrapper.Ticket.select().where(wrapper.Ticket.channel_id == interaction.channel_id).get()
            print(ticket_channel.__dict__)
            print(ticket_channel.status)
        except Exception as e:
            await interaction.followup.send("This is not a ticket channel, please use this command in the channel of the service you would like to set the cost of.")
            print(e)
            return
        else:
            try:
                print(ticket_channel.channel_id)
            except Exception as e:
                await interaction.followup.send("This is not a ticket channel, please use this command in the channel of the service you would like to set the cost of.")
                print(e)
                print(ticket_channel)
                return
            else:
                pass

        if ticket_channel.channel_type == 0:
            await interaction.followup.send("This is a support ticket! You do not need to set the cost of this service!")
            return
        if ticket_channel.channel_type == 1:
            await interaction.followup.send("This is a moderation ticket! You do not need to set the cost of this service!")
            return
        if ticket_channel.channel_type == 2:

            if self.bot.snowflake["developer"] in interaction.user.roles:
                pass
            else:
                await interaction.followup.send("You do not have permission to use this command!")
                return

            await interaction.followup.send("Fetching your infomation! Please wait...")

            try:
                bot_instance : wrapper.CustomBot = wrapper.CustomBot.select().where(wrapper.CustomBot.ticket_id == interaction.channel.id).get()
                print(str(bot_instance))
            except:
                await interaction.followup.send('There has been an error, your custom bot infomation was not found!')
            else:
                bot_instance.cost = cost
                bot_instance.save()
                await interaction.followup.send(f"Cost set to ${cost}!")
            return
        if ticket_channel.channel_type == 3:
            await interaction.followup.send("This is a custom bot ticket! You do not need to set the cost of this service!")
            return
        if ticket_channel.channel_type == 4:
            await interaction.followup.send("This is a custom bot ticket! You do not need to set the cost of this service!")
            return

async def setup(bot):
    await bot.add_cog(Cost(bot))