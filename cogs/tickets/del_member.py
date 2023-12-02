import discord
from discord.ext import commands
from discord import app_commands

class DelMember(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    async def remove_permissions(self, channel : discord.TextChannel, interaction : discord.Interaction, member : discord.Member):
        '''
        Purpose: Removes permissions from the ticket channel
        Attributes: channel - discord.TextChannel, interaction - discord.Interaction, member - discord.Member
        Returns: None
        '''
        await channel.set_permissions(member, read_messages=False, send_messages=False)

    @app_commands.command(name="del_member", description="Removes a member from a ticket")
    async def del_member(self, interaction : discord.Interaction, member: discord.Member):
        if interaction.channel.name.startswith("ticket-") == False:
            await interaction.response.send_message("This is not a ticket channel!", ephemeral=False)
            return
        '''
        Purpose: Removes a member from the ticket channel
        Attributes: interaction - discord.Interaction, member - discord.Member
        Returns: None
        '''
        await interaction.response.send_message("Removing member...", ephemeral=False)
        ticket_channel = interaction.channel
        await self.remove_permissions(ticket_channel, interaction, member)
        
        await self.bot.snowflake['log'].send(f"Removed {member.mention} from ticket by {interaction.user.mention}")
        await interaction.channel.send(f"Removed {member.mention} from ticket!")

async def setup(bot):
    await bot.add_cog(DelMember(bot))