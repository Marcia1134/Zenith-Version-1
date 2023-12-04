import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper

class EmailModal(discord.ui.Modal):

    def __init__(self):
        super().__init__(title="Email Signup", timeout=None)
        
        self.email_input = discord.ui.TextInput(label="Email", style=discord.TextStyle.short, placeholder="Example@Email.eg", max_length=254, required=True)
        self.add_item(self.email_input)
    
    async def on_submit(self, interaction1 : discord.Interaction):
        # interaction1 must be changed eventually. It was used here for debuging.
        
        advertiser : wrapper.Advertisers = wrapper.Advertisers.create(email=str(self.email_input.value), user_id=interaction1.user.id)

        embed_email_submission = discord.Embed(color=discord.Color.purple(), title="Account Created", timestamp=interaction1.created_at)

        embed_email_submission.add_field(name="Details", value=f"You have signed up with the email: ```{advertiser.email}```\n\nYour Advertising Code is ```{advertiser.code}```", inline=False)

        embed_email_submission.add_field(name="Getting Started", value="To get started, learn about the advertiser Dashboard. bring up a dashboard anywhere by using the ```/ad_dashboard``` command! If you want a completely private session, use the Direct Message option! This will allow you to edit your profile, get support if needed, and manage your account status!", inline=False)
        
        await interaction1.response.send_message(embed=embed_email_submission)

    async def on_cancel(self, interaction : discord.Interaction):
        await interaction.reponse.send_message(f"Please know that you can not continue as an Advertiser without signing up with your email! If you do wish to continue please fill out the infomation.")


class CreateAdvertiserProfile(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

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

            @discord.ui.button(label="Email", custom_id="email_signup_id", style=discord.ButtonStyle.blurple)
            async def email_signup(self, interaction : discord.Interaction, button : discord.ui.Button):
                await interaction.response.send_modal(EmailModal())

        email_embed = discord.Embed(title="Email Signup")
        email_embed.add_field(name="Email Signup", value="Click the **Email** button to link your paypal to your adverising account!", inline=False)
        email_embed.add_field(name="PayPal Signup", value="Click the **PayPal** button to signup for a PayPal Account!", inline=False)

        await interaction.response.send_message(embed=email_embed, view=ViewEmail())

        await self.bot.snowflake['log'].send(f"Created Advertiser Profile for {interaction.user.name}")
    
async def setup(bot):
    await bot.add_cog(CreateAdvertiserProfile(bot))