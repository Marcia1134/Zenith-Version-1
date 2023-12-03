import discord
from discord.ext import commands
from discord import app_commands
from database.wrapper import Ticket as wrapper

class DeleteTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="delete_ticket", description="Deletes a ticket")
    async def delete_ticket(self, interaction : discord.Interaction):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        ### Returns

        `None`

        ### Description

        Deletes a ticket.

        Checks if the ticket is already deleted, and if not, deletes the ticket.
        '''

        # Checks if it is a ticket
        if interaction.channel.id not in [ticket.channel_id for ticket in wrapper.select()]:
            await interaction.response.send_message("This is not a ticket!")
            return

        # Checks Ticket Status
        ticket : wrapper = wrapper.get(wrapper.channel_id == interaction.channel.id)
        if ticket.status == 0:
            await interaction.response.send_message("A ticket must first be closed before you can delete it!")
            return

        await interaction.response.send_message("This might take a second! Please wait while we delete the ticket for you!")

        ticket.delete_instance()
        await interaction.channel.delete()

        return
    
async def setup(bot : commands.Bot):
    await bot.add_cog(DeleteTicket(bot))