import discord
from discord.ext import commands
from discord import app_commands
from database.wrapper import Ticket as wrapper

class CreateTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="create_ticket", description="Creates a ticket")
    @app_commands.choices(ticket_type = [
        app_commands.Choice(name="Support", value=0),
        app_commands.Choice(name="Moderation", value=1),
        app_commands.Choice(name="Custom Bot", value=2),
        app_commands.Choice(name="Custom Server", value=3),
        app_commands.Choice(name="Other", value=4)
    ])
    async def create_ticket(self, interaction : discord.Interaction, ticket_type : int):
        pass
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        `ticket_type` = int

        ### Returns

        `None`

        ### Description

        Creates a ticket.

        Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
        '''

        async def create_support_ticket(interaction: discord.Interaction):
            '''
            ## Zenith Collective

            ### Parameters

            `interaction` = discord.Interaction

            ### Returns

            `None`

            ### Description

            Creates a support ticket.

            Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
            '''
            support_category = discord.utils.get(interaction.guild.categories, name="Support Tickets")
            if support_category is None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                }

                support_category = await interaction.guild.create_category_channel(name="Support Tickets", overwrites=overwrites)

            ticket_channel = await interaction.guild.create_text_channel(name=f"support-{interaction.user.name}", category=support_category)

            ticket_id = wrapper.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, type=0, status=0)

            await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

            support_embed = discord.Embed(title="Support Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
            support_embed.set_footer(text="Zenith Collective")
            support_embed.set_image(url=self.bot.config['branding']['logo'])
            support_embed.timestamp = interaction.created_at
            support_embed.add_field(name="Ticket Type", value="Support", inline=True)
            support_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
            support_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
            support_embed.add_field(name="Getting Started", value="Please describe your issue in as much detail as possible. A staff member will be with you shortly. Include screenshots/screen recordings or any other media that may help describe your issue.", inline=False)
            support_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)
            
            await ticket_channel.send(embed=support_embed)

            return ticket_channel

        async def create_moderation_ticket(interaction: discord.Interaction):
            '''
            ## Zenith Collective

            ### Parameters

            `interaction` = discord.Interaction

            ### Returns

            `None`

            ### Description

            Creates a moderation ticket.

            Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
            '''
            moderation_category = discord.utils.get(interaction.guild.categories, name="Moderation Tickets")
            if moderation_category is None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                }

                moderation_category = await interaction.guild.create_category_channel(name="Moderation Tickets", overwrites=overwrites)

            ticket_channel = await interaction.guild.create_text_channel(name=f"moderation-{interaction.user.global_name}", category=moderation_category)

            ticket_id = wrapper.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, type=1, status=0)

            await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

            moderation_embed = discord.Embed(title="Moderation Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
            moderation_embed.set_footer(text="Zenith Collective")
            moderation_embed.set_image(url=self.bot.config['branding']['logo'])
            moderation_embed.timestamp = interaction.created_at
            moderation_embed.add_field(name="Ticket Type", value="Moderation", inline=True)
            moderation_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
            moderation_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
            moderation_embed.add_field(name="Getting Started", value="Please describe your issue in as much detail as possible. A staff member will be with you shortly. Include screenshots/screen recordings or any other media that may help describe your issue.", inline=False)
            moderation_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)

            await ticket_channel.send(embed=moderation_embed)

            return ticket_channel

        async def create_custom_bot_ticket(interaction: discord.Interaction):
            '''
            ## Zenith Collective

            ### Parameters

            `interaction` = discord.Interaction

            ### Returns

            `None`

            ### Description

            Creates a custom bot ticket.

            Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
            '''
            custom_bot_category = discord.utils.get(interaction.guild.categories, name="Custom Bot Tickets")
            if custom_bot_category is None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                }

                custom_bot_category = await interaction.guild.create_category_channel(name="Custom Bot Tickets", overwrites=overwrites)

            ticket_channel = await interaction.guild.create_text_channel(name=f"custom-bot-{interaction.user.name}", category=custom_bot_category)

            ticket_id = wrapper.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, type=2, status=0)

            await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

            custom_bot_embed = discord.Embed(title="Custom Bot Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
            custom_bot_embed.set_footer(text="Zenith Collective")
            custom_bot_embed.set_image(url=self.bot.config['branding']['logo'])
            custom_bot_embed.timestamp = interaction.created_at
            custom_bot_embed.add_field(name="Ticket Type", value="Custom Bot", inline=True)
            custom_bot_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
            custom_bot_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
            custom_bot_embed.add_field(name="Getting Started", value="Please describe your issue in as much detail as possible. A staff member will be with you shortly. Include screenshots/screen recordings or any other media that may help describe your issue.", inline=False)
            custom_bot_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)
            
            await ticket_channel.send(embed=custom_bot_embed)

            return ticket_channel

        async def create_custom_server_ticket(interaction: discord.Interaction):
            '''
            ## Zenith Collective

            ### Parameters

            `interaction` = discord.Interaction

            ### Returns

            `None`

            ### Description

            Creates a custom server ticket.

            Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
            '''
            custom_server_category = discord.utils.get(interaction.guild.categories, name="Custom Server Tickets")
            if custom_server_category is None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                }

                custom_server_category = await interaction.guild.create_category_channel(name="Custom Server Tickets", overwrites=overwrites)

            ticket_channel = await interaction.guild.create_text_channel(name=f"custom-server-{interaction.user.name}", category=custom_server_category)

            ticket_id = wrapper.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, type=3, status=0)

            await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

            custom_server_embed = discord.Embed(title="Custom Server Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
            custom_server_embed.set_footer(text="Zenith Collective")
            custom_server_embed.set_image(url=self.bot.config['branding']['logo'])
            custom_server_embed.timestamp = interaction.created_at
            custom_server_embed.add_field(name="Ticket Type", value="Custom Server", inline=True)
            custom_server_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
            custom_server_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
            custom_server_embed.add_field(name="Getting Started", value="Please describe your issue in as much detail as possible. A staff member will be with you shortly. Include screenshots/screen recordings or any other media that may help describe your issue.", inline=False)
            custom_server_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)
            
            await ticket_channel.send(embed=custom_server_embed)

            return ticket_channel

        async def create_other_ticket(interaction: discord.Interaction):
            '''
            ## Zenith Collective

            ### Parameters

            `interaction` = discord.Interaction

            ### Returns

            `None`

            ### Description

            Creates an other ticket.

            Grabs ticket type from `ticket_type` parameter, creates a ticket, and sends a message to the user with the ticket channel.
            '''
            other_category = discord.utils.get(interaction.guild.categories, name="Other Tickets")
            if other_category is None:
                overwrites = {
                    interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                    interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                    self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                }

                other_category = await interaction.guild.create_category_channel(name="Other Tickets", overwrites=overwrites)

            ticket_channel = await interaction.guild.create_text_channel(name=f"other-{interaction.user.name}", category=other_category)

            ticket_id = wrapper.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, type=4, status=0)

            await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

            other_embed = discord.Embed(title="Other Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
            other_embed.set_footer(text="Zenith Collective")
            other_embed.set_image(url=self.bot.config['branding']['logo'])
            other_embed.timestamp = interaction.created_at
            other_embed.add_field(name="Ticket Type", value="Other", inline=True)
            other_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
            other_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
            other_embed.add_field(name="Getting Started", value="Please describe your issue in as much detail as possible. A staff member will be with you shortly. Include screenshots/screen recordings or any other media that may help describe your issue.", inline=False)
            other_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)
            
            await ticket_channel.send(embed=other_embed)

            return ticket_channel

        if ticket_type == 0:
            await interaction.response.send_message("Creating a support ticket...", ephemeral=True)
            channel = await create_support_ticket(interaction)
            await interaction.followup.send(f"Support ticket created! ({channel.mention})", ephemeral=True)
        elif ticket_type == 1:
            await interaction.response.send_message("Creating a moderation ticket...", ephemeral=True)
            channel = await create_moderation_ticket(interaction)
            await interaction.followup.send(f"Moderation ticket created! ({channel.mention})", ephemeral=True)
        elif ticket_type == 2:
            await interaction.response.send_message("Creating a custom bot ticket...", ephemeral=True)
            channel = await create_custom_bot_ticket(interaction)
            await interaction.followup.send(f"Custom bot ticket created! ({channel.mention})", ephemeral=True)
        elif ticket_type == 3:
            await interaction.response.send_message("Creating a custom server ticket...", ephemeral=True)
            channel = await create_custom_server_ticket(interaction)
            await interaction.followup.send(f"Custom server ticket created! ({channel.mention})", ephemeral=True)
        elif ticket_type == 4:
            await interaction.response.send_message("Creating an other ticket...", ephemeral=True)
            channel = await create_other_ticket(interaction)
            await interaction.followup.send(f"Other ticket created! ({channel.mention})", ephemeral=True)
        else:
            await interaction.response.send_message("Invalid ticket type!", ephemeral=True)
            return

async def setup(bot : commands.Bot):
    await bot.add_cog(CreateTicket(bot))