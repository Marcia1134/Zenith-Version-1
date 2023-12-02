import discord
from discord.ext import commands
from discord import app_commands

class CreateTicket(commands.Cog):
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

    @app_commands.command(name="create_ticket", description="Creates a ticket")
    async def create_ticket(self, interaction : discord.Interaction, member: discord.Member, reason: str = "No reason provided"):
        
        await interaction.response.send_message("Creating ticket...", ephemeral=False)
        ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{member.global_name}", category=self.bot.snowflake['ticket_category'])
        
        # Sets permissions for the ticket channel
        await self.grant_permissions(ticket_channel, interaction, member)
        
        #Defines embed class
        class embed:
            pass
        
        # Sends appropriate messages
        embed.ticket_realizer = discord.Embed(title="Ticket Created", description=f"Hello {member.mention}, thank you for waiting paticently to be connected with a moderator! Please begin by describing what you need assistance with!", color=0x00ff00)
        embed.ticket_realizer.add_field(name="Reason", value=reason)
        embed.ticket_realizer.set_footer(text="Thank you for your patience!")
        await ticket_channel.send(embed=embed.ticket_realizer)

        await interaction.channel.send(content=f"Created ticket {ticket_channel.mention}")

        embed.member_private = discord.Embed(title="Ticket Created", description=f"A ticket has been created for you! Please make your way there {ticket_channel.mention}", color=0x00ff00)
        embed.member_private.add_field(name="Reason", value=reason)
        embed.member_private.set_footer(text="Thank you for your patience!")
        await member.send(embed=embed.member_private)
        
        embed.member_private_reminder = discord.Embed(title="Ticket Created", description=f"Please do understand that if you are unable to respond to your ticket within 30 minutes, the ticket will be deleted by a moderator!", color=0x00ff00)
        await member.send(embed=embed.member_private_reminder)
        
        # Logs the ticket creation with relvant infomation
        embed.logging_message = discord.Embed(title="Ticket Created", color=0x00ff00)
        embed.logging_message.add_field(name="Ticket Channel", value=f'{ticket_channel.mention}')
        embed.logging_message.add_field(name="Ticket Creator", value=f'{interaction.user.mention}')
        embed.logging_message.add_field(name="Ticket Member", value=f'{member.mention}')
        embed.logging_message.add_field(name="Reason", value=f'```{reason}```')
        embed.logging_message.timestamp = interaction.created_at
        embed.logging_message.set_footer(text=f"If this ticket looks suspisious, please contact an Admin, or lock the ticket channel.")
        await self.bot.snowflake['log'].send(embed=embed.logging_message)
        

async def setup(bot):
    await bot.add_cog(CreateTicket(bot))