import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class AddMember(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="add_member", description="Adds a member to a ticket")
    async def add_member(self, interaction : discord.Interaction, member: discord.Member):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        `member` = int

        ### Returns

        `None`

        ### Description

        Adds a member to a ticket.
        
        Grabs user from `member` parameter, checks if the user is in the ticket, and if not, adds them to the ticket.

        '''
        # Grabs Member Snowflake
        #try:
        #    member = self.bot.get_user(member)
        #except:
        #    await interaction.response.send_message("Invalid member!")
        #    return

        # Checks if Member is None
        if member is None:
            await interaction.response.send_message("Invalid member!")
            return

        # Checks Ticket Status
        ticket : wrapper.Ticket = wrapper.Ticket.get(wrapper.Ticket.channel_id == interaction.channel.id)
        if ticket.status == 1:
            await interaction.response.send_message("This is a closed ticket! It is not possible to add any new members.")
            return
        
        # Checks if the member is already in the ticket
        if member in interaction.channel.members:
            await interaction.response.send_message("This member is already in the ticket!")
            return
        
        ticket_channel : discord.TextChannel = self.bot.get_channel(ticket.channel_id)
        await ticket_channel.set_permissions(member, view_channel=True, send_messages=True)
        
        class MemberAddedEmbed(discord.Embed):
            '''
            ## Zenith Collective

            Embed for when a user is added to a ticket.

            `title` = "Member Added"

            `description` = "{member.mention} has been added to the ticket!"

            `color` = discord.Color.magenta()

            `footer` = "Zenith Collective"

            `timestamp` = interaction.created_at

            `thumbnail` = member.avatar_url
                `or` member.default_avatar_url
            '''
            def __init__(self):
                super().__init__(title="Member Added", description=f"{member.mention} has been added to the ticket!", color=discord.Color.magenta())
                self.set_footer(text="Zenith Collective")
                self.timestamp = interaction.created_at

                # Try to set the thumbnail to the member's avatar, if it fails, set it to the default avatar
                try:
                    self.set_thumbnail(url=member.avatar_url)
                except:
                    try:
                        self.set_thumbnail(url=member.default_avatar_url)
                    except:
                        pass 

        await ticket_channel.send(embed=MemberAddedEmbed())
        await interaction.response.send_message(f"Added {member.mention} to the ticket!")
        await self.bot.snowflake['log'].send(f"Added {member.mention} to ticket {ticket_channel.mention} in {ticket_channel.guild.name}!")

async def setup(bot : commands.Bot):
    await bot.add_cog(AddMember(bot))