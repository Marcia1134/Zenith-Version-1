import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class RemoveMember(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="remove_member", description="Removes a member from a ticket")
    async def add_member(self, interaction : discord.Interaction, member: int):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        `member` = int

        ### Returns

        `None`

        ### Description

        Removes a member from a ticket.
        
        Grabs user from `member` parameter, checks if the user is in the ticket, Removes them from the ticket.

        '''
        # Grabs Member Snowflake
        try:
            member = self.bot.get_user(member)
        except:
            await interaction.response.send_message("Invalid member!")
            return

        # Checks if Member is None
        if member is None:
            await interaction.response.send_message("Invalid member!")
            return

        # Checks Ticket Status
        ticket : wrapper.Ticket = wrapper.Ticket.get(wrapper.Ticket.channel_id == interaction.channel.id)
        if ticket.status == 1:
            await interaction.response.send_message("This is a closed ticket! It is not possible to remove any old members.")
            return
        
        # Checks if the member is not present in the ticket.
        if member not in interaction.channel.members:
            await interaction.response.send_message("This member does not exist in the ticket! In order to add them, please use the `/add_member` command.")
            return
        
        ticket_channel : discord.TextChannel = self.bot.get_channel(ticket.channel_id)
        await ticket_channel.set_permissions(member, view_channel=False, send_messages=False)
        
        class MemberRemovedEmbed(discord.Embed):
            '''
            ## Zenith Collective

            Embed for when a user is Removed from a ticket.

            `title` = "Member Removed"

            `description` = "{member.mention} has been removed from the ticket!"

            `color` = discord.Color.magenta()

            `footer` = "Zenith Collective"

            `timestamp` = interaction.created_at

            `thumbnail` = member.avatar_url
                `or` member.default_avatar_url
            '''
            def __init__(self):
                super().__init__(title="Member Removed", description=f"{member.mention} has been removed from the ticket!", color=discord.Color.magenta())
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

        await ticket_channel.send(embed=MemberRemovedEmbed)
        await interaction.response.send_message(f"Removed {member.mention} from the ticket!")
        await self.bot.snowflake['log'].send(f"Removed {member.mention} from ticket {ticket_channel.mention} in {ticket_channel.guild.name}!")

async def setup(bot : commands.Bot):
    await bot.add_cog(RemoveMember(bot))