import discord
from discord.ext import commands
from discord import app_commands
from cogs.advertising import db_wrapper as db


class CustomBotModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(timeout=None, title="Create a Custom Bot!")
        self.code = discord.ui.TextInput(label="Enter your advertiser's code here:", min_length=6, max_length=6)
        self.desc = discord.ui.TextInput(label="Describe your bot here!", min_length=10, max_length=1000, style=discord.TextStyle.paragraph)
        self.add_item(self.code)
        self.add_item(self.desc)
        

    async def on_submit(self, interaction : discord.Interaction):

        ticket_channel = await interaction.guild.create_text_channel(name=f"ticket-{interaction.user.global_name}", category=self.bot.snowflake['ticket_category'])
        
        # Sets permissions for the ticket channel
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        await ticket_channel.set_permissions(interaction.guild.default_role, read_messages=False, view_channel=False)
        await ticket_channel.set_permissions(self.bot.snowflake['member'], read_messages=False, send_messages=False, view_channel=False)
        await ticket_channel.set_permissions(self.bot.snowflake['mod'], read_messages=True, send_messages=True)
        
        embed_ticket_realizer = discord.Embed(title="Ticket Created", description=f"Hello {interaction.user.mention}, thank you for waiting paticently to be connected with a moderator! Please begin by describing what you need assistance with!", color=0x00ff00)
        embed_ticket_realizer.add_field(name="Product Description", value=self.desc.value)
        embed_ticket_realizer.set_footer(text="Thank you for your patience!")
        await ticket_channel.send(embed=embed_ticket_realizer)

        await interaction.channel.send(content=f"Created ticket {ticket_channel.mention}")
        

class CustomBot(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(label="Custom Bot", style=discord.ButtonStyle.green, emoji="🤖")
    async def custom_bot(self, interaction : discord.Interaction, button : discord.ui.Button):
        await interaction.response.send_message("Custom Bot", ephemeral=False, delete_after=1)
        await interaction.channel.send(embed=discord.Embed(title="Custom Bot", description="```Custom Bot```", color=discord.Color.dark_purple()))
        await self.bot.snowflake['log'].send(f"Created Custom Bot request for {interaction.user.mention}")

class Shop(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Gets the shop")
    async def send_shop(self, interaction : discord.Interaction):
        '''
        Purpose: Gets the shop

        Parameters: interaction - discord.Interaction

        Returns: None
        '''

        embed = discord.Embed(title="Zenith Collective", description=f"```The Zenith Collective Shop```", color=discord.Color.dark_purple())
        embed.add_field(name="Custom Bots", value="Just click the button below to get started with getting your own custom bot!", inline=False)
        embed.add_field(name="More Comming Soon !!", value="More products will be added soon!", inline=False)

        await interaction.response.send_message("shop sent!", ephemeral=False, delete_after=1)
        await interaction.channel.send(embed=embed)
        