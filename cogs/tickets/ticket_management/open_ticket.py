import discord
from discord.ext import commands
from discord import app_commands
from database.wrapper import Ticket as wrapper
from asyncio import sleep

class OpenTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="open_ticket", description="opens a ticket")
    async def open_ticket(self, interaction : discord.Interaction):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        ### Returns

        `None`

        ### Description

        close a ticket.

        Checks if the ticket is already open, and if not, opens the ticket.
        '''

        # Checks Ticket Status
        ticket : wrapper = wrapper.get(wrapper.channel_id == interaction.channel.id)
        if ticket.status == 0:
            await interaction.response.send_message("This ticket is opened! It is not possible to open an opened ticket.")
            return

        await interaction.response.send_message("This might take a second! Please wait while we open the ticket for you!")

        ticket_channel : discord.TextChannel = self.bot.get_channel(ticket.channel_id)
        await ticket_channel.set_permissions(interaction.guild.default_role, send_messages=False, view_channel=False)
        for role in interaction.guild.roles:
            if role.permissions.manage_channels:
                await ticket_channel.set_permissions(role, send_messages=True, view_channel=True)
                await sleep(0.1)
        await ticket_channel.set_permissions(self.bot.user, send_messages=True, view_channel=True)

        class TicketOpenEmbed(discord.Embed):
            '''
            ## Zenith Collective

            ### Parameters

            `discord.Embed` = Embed

            ### Returns

            `None`

            ### Description

            Embed that is sent when a ticket is opened.
            '''
            def __init__(self):
                super().__init__()
                self.title = "Ticket Opened"
                self.description = f"Ticket has been Opened by {interaction.user.mention}"
                self.color = discord.Color.purple()

        await interaction.channel.send(embed=TicketOpenEmbed())

        # Updates Database
        ticket.status = 0
        ticket.save()

async def setup(bot : commands.Bot):
    await bot.add_cog(OpenTicket(bot))