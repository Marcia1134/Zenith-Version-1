import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
from discord import ButtonStyle
from database import wrapper

class Shop(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot : commands.Bot = bot
    
    class ShopView(ui.View):
        def __init__(self, bot):
            self.bot : commands.Bot = bot
            super().__init__(timeout=None)

        @ui.button(label="Custom Discord Bot", style=ButtonStyle.blurple, emoji="🤖")
        async def CDB_button(self, interaction : discord.Interaction, button : discord.Button):
            
            class CustomBotModal(ui.Modal):
                def __init__(self):
                    super().__init__(timeout=None, title="Custom Discord Bot")
                    self.bot_name_input = ui.TextInput(label="The name of your custom bot", placeholder="nameless bot", max_length=16, min_length=3)
                    self.bot_description_input = ui.TextInput(label="A short description of your bot;", placeholder="Just a summary of the bot and it's functions/features", style=discord.TextStyle.long, min_length=50, max_length=500)
                    self.bot_notes_input = ui.TextInput(label="Anything else important you need us to know?", placeholder="Any important notes?", required=False, max_length=450)
                    self.bot_advertiser_code = ui.TextInput(label="Advertiser Code", placeholder="Place your advertsier code here", max_length=6, min_length=1)
                    
                    self.add_item(self.bot_name_input)
                    self.add_item(self.bot_description_input)
                    self.add_item(self.bot_notes_input)
                    self.add_item(self.bot_advertiser_code)
                
                async def on_submit(self, interaction : discord.Interaction):
                    
                    await interaction.response.send_message("Attempting to create channel!")

                    support_category = discord.utils.get(interaction.guild.categories, name="Custom Bot Tickets")
                    if support_category is None:
                        overwrites = {
                            interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False, send_messages=False),
                            interaction.guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True),
                            self.bot.snowflake['mod'] : discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
                        }

                        support_category = await interaction.guild.create_category_channel(name="Custom Bot Tickets", overwrites=overwrites)

                    bot_instance : wrapper.CustomBot = wrapper.CustomBot.select().where(wrapper.CustomBot.bot_name == self.bot_name_input.value).execute()

                    ticket_channel = await interaction.guild.create_text_channel(name=f"custom-bot-{interaction.user.name}", category=support_category)

                    ticket_id = wrapper.Ticket.create(guild_id=interaction.guild.id, channel_id=ticket_channel.id, channel_type=2, status=0)

                    await ticket_channel.edit(name=f"{ticket_channel.name}-{ticket_id}")

                    support_embed = discord.Embed(title="Custom Bot Ticket", description=f"Ticket created by {interaction.user.mention}!", color=discord.Color.magenta())
                    support_embed.set_footer(text="Zenith Collective")
                    support_embed.timestamp = interaction.created_at
                    support_embed.add_field(name="Ticket Type", value="Custom Bot", inline=True)
                    support_embed.add_field(name="Ticket ID", value=ticket_channel.id, inline=True)
                    support_embed.add_field(name="Ticket Channel", value=ticket_channel.mention, inline=True)
                    try:
                        advertiser : wrapper.Advertisers = wrapper.Advertisers.select().where(wrapper.Advertisers.code == self.bot_advertiser_code.value).get()
                    except:
                        await interaction.followup.send(f"The advertiser code of {self.bot_advertiser_code.value} is not a valid code! Please try again: \n\nBot Description: ```{self.bot_description_input.value}```\nNotes: ```{self.bot_notes_input.value}``` ")
                        await ticket_channel.delete()
                        wrapper.Ticket.delete_by_id(ticket_id)
                        return
                    else:
                        support_embed.add_field(name="Advertiser", value=f"Email: ```{advertiser.email}```\nLevel: ```{advertiser.level}```", inline=False)
                        pass
                    bot_instance_id = wrapper.CustomBot.create(user_id = interaction.user.id,
                                             bot_name = self.bot_name_input.value,
                                             bot_description = self.bot_description_input.value,
                                             ticket_id = ticket_channel.id,
                                             code = self.bot_advertiser_code.value)
                    
                    support_embed.add_field(name="Bot ID", value=f"```{bot_instance_id}```", inline=True)
                    support_embed.add_field(name="Bot Name", value=f"```{self.bot_name_input.value}```", inline=True)
                    support_embed.add_field(name="Bot Description", value=f"```{self.bot_description_input.value}```", inline=False)
                    if self.bot_notes_input != None:
                        if self.bot_notes_input != "":
                            support_embed.add_field(name="Description Notes", value=f"```{self.bot_notes_input.value}```", inline=False)
                    
                    support_embed.add_field(name="Closing Ticket", value="To close this ticket, please use the `/close_ticket` command.", inline=False)

                    await ticket_channel.send(embed=support_embed)

                    return ticket_channel
            
            await  interaction.response.send_modal(CustomBotModal())

    @app_commands.command(name="shop", description="Displays the entire shop!")
    async def view_shop_command(self, interaction : discord.Interaction):
        
        embed = discord.Embed(color=discord.Color.purple(), title="Zenith Collective Shop")
        embed.add_field(name="Custom Discord Bot", value="```Custom Discord Bot, fill out the details of your bot and get a developer to assist you by coding a bot of your request.```\n\n```Price Range: 10USD - 60USD```")
        embed.add_field(name="Web Automation", value="```Anything from automating email creating, to automattically uploading or downloading youtube videos.```\n\n```Price Range: 25-80 USD```")

        await interaction.response.send_message(embed=embed, view=self.ShopView(self.bot))

async def setup(bot):
    await bot.add_cog(Shop(bot))