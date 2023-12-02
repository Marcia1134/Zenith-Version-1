import discord
from discord.ext import commands
from discord import app_commands

class CloseTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    async def delete_ticket_fn(self, channel : discord.TextChannel, interaction : discord.Interaction):
        '''
        Purpose: Deletes the ticket channel
        Attributes: channel - discord.TextChannel, interaction - discord.Interaction
        Returns: None
        '''
        await channel.delete()

    @app_commands.command(name="close_ticket", description="Closes a ticket")
    async def close_ticket(self, interaction : discord.Interaction, member: discord.Member = None):
        if interaction.channel.name.startswith("ticket-") == False:
            await interaction.response.send_message("This is not a ticket channel!", ephemeral=False)
            return
        '''
        Purpose: Closes the ticket channel
        Attributes: interaction - discord.Interaction
        Returns: None
        '''
        await interaction.response.send_message("Closing ticket...", ephemeral=False)
        ticket_channel = interaction.channel
        await self.delete_ticket_fn(ticket_channel, interaction)
        await self.bot.snowflake['log'].send(f"Closed ticket by {interaction.user.mention}")
        if member != None:
            await member.send(f"Your ticket has been closed by {interaction.user.mention}! Thank you for your time. If you require further assistance, please create another request using `!help` here.")

async def setup(bot):
    await bot.add_cog(CloseTicket(bot))