import discord
from discord.ext import commands
from discord import app_commands
from database.wrapper import Ticket as wrapper
from asyncio import sleep

class CloseTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="close_ticket", description="closes a ticket")
    async def close_ticket(self, interaction : discord.Interaction):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        ### Returns

        `None`

        ### Description

        close a ticket.

        Checks if the ticket is already closed, and if not, closes the ticket.
        '''

        

        # Checks Ticket Status
        ticket : wrapper = wrapper.get(wrapper.channel_id == interaction.channel.id)
        if ticket.status == 1:
            await interaction.response.send_message("This ticket is closed! It is not possible to close a closed ticket.")
            return

        await interaction.response.send_message("This might take a second! Please wait while we close the ticket for you!")

        ticket_channel : discord.TextChannel = self.bot.get_channel(ticket.channel_id)
        await ticket_channel.set_permissions(interaction.guild.default_role, send_messages=False)
        for role in interaction.guild.roles:
            if not role.permissions.administrator:
                await ticket_channel.set_permissions(role, send_messages=False, view_channel=False)
                await sleep(0.1)
        await ticket_channel.set_permissions(self.bot.user, send_messages=True)
        await ticket_channel.set_permissions(interaction.guild.me, send_messages=True)
        

        class TicketCloseEmbed(discord.Embed):
            '''
            ## Zenith Collective

            ### Parameters

            `discord.Embed` = Embed

            ### Returns

            `None`

            ### Description

            Embed that is sent when a ticket is closed.
            '''
            def __init__(self):
                super().__init__()
                self.title = "Ticket Close"
                self.description = f"Ticket has been closed by {interaction.user.mention}"
                self.color = discord.Color.magenta()

        await interaction.channel.send(embed=TicketCloseEmbed())

        # Updates Database
        ticket.status = 1
        ticket.save()

async def setup(bot : commands.Bot):
    await bot.add_cog(CloseTicket(bot))