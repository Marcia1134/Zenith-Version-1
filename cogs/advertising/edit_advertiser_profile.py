import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class EditAdvertiserProfile(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="edit_advertising_profile", description="Edit The advertising profile")
    async def edit_profile(self, interaction : discord.Interaction):
        embed = discord.Embed(color=discord.Color.purple(), title="Edit your Profile", description="Click the buttons below to change the aspects of your profile.")

        class EditView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Email", emoji="✉️")
            async def edit_email_button(self, interaction : discord.Interaction, button : discord.Button):
                
                class EmailModal(discord.ui.Modal):

                    def __init__(self, advertiser : wrapper.Advertisers):
                        super().__init__(title="Email Edit", timeout=None)
                        
                        self.email_input = discord.ui.TextInput(label="Email", style=discord.TextStyle.short, placeholder=f"old: {advertiser.email}", max_length=254, required=True)
                        self.add_item(self.email_input)
                    
                    async def on_submit(self, interaction1 : discord.Interaction):
                        # interaction1 must be changed eventually. It was used here for debuging.
                        
                        advertiser : wrapper.Advertisers = wrapper.Advertisers.select().where()(email=str(self.email_input.value), user_id=interaction1.user.id)

                        embed_email_submission = discord.Embed(color=discord.Color.purple(), title="Account Created", timestamp=interaction1.created_at)

                        embed_email_submission.add_field(name="Details", value=f"You have signed up with the email: ```{advertiser.email}```\n\nYour Advertising Code is ```{advertiser.code}```", inline=False)

                        embed_email_submission.add_field(name="Getting Started", value="To get started, learn about the advertiser Dashboard. bring up a dashboard anywhere by using the ```/ad_dashboard``` command! If you want a completely private session, use the Direct Message option! This will allow you to edit your profile, get support if needed, and manage your account status!", inline=False)
                        
                        await interaction1.response.send_message(embed=embed_email_submission)

                    async def on_cancel(self, interaction : discord.Interaction):
                        await interaction.reponse.send_message(f"Please know that you can not continue as an Advertiser without signing up with your email! If you do wish to continue please fill out the infomation.")

                await interaction.response.send_modal()
            
            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Nickname", emoji="✉️")
            async def edit_nickname_button(self, interaction : discord.Interaction, button : discord.Button):
                await interaction.response.send_message(f"Editing the {button.label}...")
            
            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Break", emoji="✉️")
            async def edit_break_button(self, interaction : discord.Interaction, button : discord.Button):
                await interaction.response.send_message(f"Editing the {button.label}...")
            
            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Resign", emoji="✉️")
            async def edit_resign_button(self, interaction : discord.Interaction, button : discord.Button):
                await interaction.response.send_message(f"Editing the {button.label}...")
            
            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Support", emoji="✉️")
            async def edit_support_button(self, interaction : discord.Interaction, button : discord.Button):
                await interaction.response.send_message(f"Editing the {button.label}...")
        
        await interaction.response.send_message(embed=embed, view=EditView())

async def setup(bot : commands.Bot):
    await bot.add_cog(EditAdvertiserProfile(bot))