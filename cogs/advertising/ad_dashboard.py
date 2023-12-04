import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

# Change to AdDashboard
class EditAdvertiserProfile(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    '''
    This document does not follow the normal style of coding! Normally I try to keep functions, classes and etc on the global level of the code and here, there was simply too much going on. It is much easier to store the classes and sub classes in the actual application function. This does reduce readablity and can make things harder to understand with this many embeds but I can't think of a better structure at the moment, will review in the next version!
    '''

    @app_commands.command(name="ad_dashboard", description="Edit The advertising profile")
    async def edit_profile(self, interaction : discord.Interaction):
        embed = discord.Embed(color=discord.Color.purple(), title="Edit your Profile", description="Click the buttons below to change the aspects of your profile.")

        class EditView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)

            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Email", emoji="✉️")
            async def edit_email_button(self, interaction : discord.Interaction, button : discord.Button):
                
                class EmailModal(discord.ui.Modal):

                    def __init__(self):
                        super().__init__(title="Email Edit", timeout=None)
                        self.email_input = discord.ui.TextInput(label="Email", style=discord.TextStyle.short, placeholder=f"old: {advertiser.email}", max_length=254, required=True)
                        self.add_item(self.email_input)
                    
                    async def on_submit(self, interaction1 : discord.Interaction):
                        # interaction1 must be changed eventually. It was used here for debuging.

                        '''
                        This code is really inefficent, try to called the database as few times as possible. This will require a restructing and since the affect is rather small, I will leave it until the next version of the advertising to fix... Just stating this issue is known!
                        '''

                        self.advertiser = wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == interaction.user.id).get()

                        self.advertiser.email = str(self.email_input.value)
                        self.advertiser.save()

                        # refresh advertiser instance
                        self.advertiser = wrapper.Advertisers.get_by_id(self.advertiser.code)

                        # Email change submission Embed
                        embed_email_submission = discord.Embed(color=discord.Color.purple(), title="Account Edited", timestamp=interaction1.created_at)

                        embed_email_submission.add_field(name="Details", value=f"You have changed your email too: ```{self.advertiser.email}```\n\nYour Advertising Code is ```{self.advertiser.code}```", inline=False)

                        await interaction1.response.send_message(embed=embed_email_submission)

                    async def on_cancel(self, interaction : discord.Interaction):
                        await interaction.reponse.send_message(f"Please know that you can not continue as an Advertiser without signing up with your email! If you do wish to continue please fill out the infomation.")

                # Check if user has an account or not
                try:
                    advertiser = wrapper.Advertisers.select().where(wrapper.Advertisers.user_id == interaction.user.id).get()
                except wrapper.Advertisers.DoesNotExist:
                    await interaction.response.send_message("Please use the `/ad_create` command to create an account before using the Advertiser Dashboard!")
                    return
                else:
                    pass

                await interaction.response.send_modal(EmailModal())
            
            @discord.ui.button(style=discord.ButtonStyle.blurple, label="Nickname", emoji="🔄")
            async def edit_nickname_button(self, interaction : discord.Interaction, button : discord.Button):
                
                class NickChangeModal(discord.ui.Modal):
                    def __init__(self):
                        super().__init__(title="Change your Nickname on the Server!", timeout=None)

                        nickname_input = discord.ui.TextInput(label="What do you want to change your username too?", max_length=12, min_length=3, placeholder=str(interaction.user.name))

                        self.add_item(nickname_input)

                    async def on_submit(self, interaction : discord.Interaction):
                        await interaction.user.edit(nick=str(self.nickname_input.value))
                        await interaction.response.send_message(f"Your username has been changed to `{self.nickname_input.value}`!")

                    async def on_cancel(self, interaction : discord.Interaction):
                        await interaction.response.send_message(f"Please know that you can not continue as an Advertiser without signing up with your email! If you do wish to continue please fill out the infomation.")

                await interaction.response.send_modal(NickChangeModal())
            
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