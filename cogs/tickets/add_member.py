import discord
from discord.ext import commands
from discord import app_commands

class AddMember(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    async def grant_permissions(self, channel : discord.TextChannel, interaction : discord.Interaction, member : discord.Member):
        '''
        Purpose: Grants permissions to the ticket channel
        Attributes: channel - discord.TextChannel, interaction - discord.Interaction, member - discord.Member
        Returns: None
        '''
        await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await channel.set_permissions(interaction.guild.default_role, read_messages=False, view_channel=False)
        await channel.set_permissions(self.bot.snowflake['member'], read_messages=False, send_messages=False, view_channel=False)
        await channel.set_permissions(self.bot.snowflake['mod'], read_messages=True, send_messages=True)
        await channel.set_permissions(member, read_messages=True, send_messages=True)

    @app_commands.command(name="add_member", description="Adds a member to a ticket")
    async def add_member(self, interaction : discord.Interaction, member: discord.Member):
        if interaction.channel.name.startswith("ticket-") == False:
            await interaction.response.send_message("This is not a ticket channel!", ephemeral=False)
            return
        '''
        Purpose: Adds a member to the ticket channel
        Attributes: interaction - discord.Interaction, member - discord.Member
        Returns: None
        '''
        await interaction.response.send_message("Adding member...", ephemeral=False)
        ticket_channel = interaction.channel
        await self.grant_permissions(ticket_channel, interaction, member)
        
        await self.bot.snowflake['log'].send(f"Added {member.mention} to ticket by {interaction.user.mention}")
        await interaction.channel.send(f"Added {member.mention} to ticket!")

async def setup(bot):
    await bot.add_cog(AddMember(bot))