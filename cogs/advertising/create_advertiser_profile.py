import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class CreateAdvertiserProfile(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    class EmailModal(discord.ui.Modal):

        def create_advertiser(interaction : discord.Interaction, email : str) -> wrapper.Advertisers:
            '''
            Interaction : discord.Interactiob
            Email : str

            returns database instance
            '''
            return wrapper.Advertisers.create(emails=email, user_id=interaction.user.id)

        def __init__(self):
            super().__init__(title="Email Signup", timeout=None)
            self.email_input = discord.ui.TextInput(label="Email", style=discord.TextStyle.short, placeholder="Example@Email.eg", max_length=254, required=True)
            self.add_item(self.email_input)
        
        async def on_submit(self, interaction : discord.Interaction):
            advertiser : wrapper.Advertisers = self.create_advertiser(interaction=interaction, email=self.email_input.value)
            embed_email_submission = discord.Embed(color=discord.Color.purple, title="Account Created", timestamp=interaction.created_at)
            embed_email_submission.add_field(name="Details", value=f"You have signed up with the email: ```{advertiser.emails}```. \n\nYour Advertising Code is ```{advertiser._meta.ROWID}```", inline=False)
            embed_email_submission.add_field("Getting Started", value="There are a couple handy commands you might wanna memorise!\n\n1. ```/advertiser_help```\n> Brings up this embed!\n2. ```/edit```\n> Allows you to edit some of the things about your Advertiser profile, like your email incase you ever put it in wrong!")

        
        async def on_cancel(self, interaction : discord.Interaction):
            await interaction.reponse.send_message(f"Please know that you can not continue as an Advertiser without signing up with your email! If you do wish to continue please fill out the infomation.")

    @app_commands.command(name="create_advertiser_profile", description="Creates an advertiser profile")
    async def create_advertiser_profile(self, interaction : discord.Interaction):
        '''
        Purpose: Creates an advertiser profile

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
             
        class ViewEmail(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                self.add_item(discord.ui.Button(label='PayPal', style=discord.ButtonStyle.link, url="https://www.paypal.com/welcome/signup/"))

            @discord.ui.button(label="Email", custom_id="email_signup_id")
            async def email_signup(self, interaction : discord.Interaction, button : discord.ui.Button):
                await interaction.response.send_modal(self.EmailModal())

        email_embed = discord.Embed(title="Email Signup")
        email_embed.add_field(name="Email Signup", value="Click the **Email** button to link your paypal to your adverising account!", inline=False)
        email_embed.add_field(name="PayPal Signup", value="Click the **PayPal** button to signup for a PayPal Account!", inline=False)

        await interaction.response.send_message(embed=email_embed, view=ViewEmail())

        await self.bot.snowflake['log'].send(f"Created Advertiser Profile for {interaction.user.name}")
    
async def setup(bot):
    await bot.add_cog(CreateAdvertiserProfile(bot))