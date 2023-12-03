import discord
from discord.ext import commands
from discord import app_commands
from database import wrapper as db

class AdProfile(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    class AddEmailModal(discord.ui.Modal):
        def __init__(self):
            super().__init__(timeout=None, title="Set Your PayPal Email Address")
            self.email_input = discord.ui.TextInput(label="Enter your PayPal Email Address", min_length=1, max_length=100)
            self.add_item(self.email_input)

        async def on_submit(self, interaction: discord.Interaction):
            await interaction.response.send_message(f"Your PayPal Email Address has been set to {self.email_input.value}, if this is wrong, you can change it at any time using `/ad_edit`")
            db.Advertisers.update(emails=self.email_input.value).where(db.Advertisers.user_id == interaction.user.id).execute()
            embed = discord.Embed(title="Zenith Collective", description=f"Welcome to the Advertising Team, {interaction.user.display_name}!", color=discord.Color.dark_purple())
            embed.add_field(name="Help and Server Assistance -", value="If you ever need help with anything regarding Advertising, please use the `-adhelp` command here!")
            embed.add_field(name="Advertising Rules -", value="Just make sure you are being respectful, sensible, and proffesional. For example, don't spam! Make sure you are advertising in advertising spaces only. If you are unsure, please use the help command!")
            embed.add_field(name="Advertising Tips -", value="Just some tips! Make sure that you target the right people! Join new servers or servers that are looking for partnerships! Also keep in mind Advertising rules for each server!")
            embed.add_field(name="Generating Referal Codes -", value="You can use `/get_code` on the server to get a referal code!")
            embed.add_field(name="Other Useful Commands - ", value="You can use `/level` to display your current level! \n You can use `/ad_profile_delete` to delete your current profile. \n You can use the '/adhelp' command to see this message again at any point!")
            await interaction.user.send(embed=embed)
            await self.stop()

            

    class EmailButton(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="Set Email Address", custom_id="set_email", style=discord.ButtonStyle.primary)
        async def set_email(self, interaction : discord.Interaction, button : discord.ui.Button):
            await interaction.response.send_modal(AdProfile.AddEmailModal())


    @app_commands.command(name="ad_profile", description="Creates an advertiser")
    async def ad_profile(self, interaction : discord.Interaction):
        '''
        Purpose: Creates a Advertister Profile using the id of the interaction.user

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if db.Advertisers.select().where(db.Advertisers.user_id == interaction.user.id).exists()  == True:
            await interaction.response.send_message(f"You have already signed up as an Advertiser. If you want to delete your account use `/ad_profile_delete`", ephemeral=False)
        else:
            await interaction.response.send_message(f"You have begun the Sign Up Process, just one more step to go! Check your DMs to continue the proccess!", ephemeral=False)
            embed = discord.Embed(title="Zenith Collective", description=f"Welcome to the Advertising Team, {interaction.user.display_name}!", color=discord.Color.dark_purple())
            embed.set_thumbnail
            embed.add_field(name="PayPal", value="Please enter your PayPal email address", inline=False)
            embed.add_field(name="Why we ask.", value="Here at Zenith we want to get you our money as fast as possible and as easily as possible. For this reason we will send your commission cut direct to your PayPal account. ***It's really important you use the correct email address that is linked to your paypal for this reason...***", inline=False)
            embed.add_field(name="How to find your PayPal email address.", value="You can find your PayPal email address by going to your PayPal account and clicking on the settings icon. Then click on the 'Account Settings' tab and you will see your email address under the 'Email' section.", inline=False)
            embed.add_field(name="Responsibility", value="You have been warned! If your commission cut gets sent to the wrong address, I am afraid there is really not a lot we can do. This is up to you to make sure tose details are maintained!", inline=False)
            embed.add_field(name="Changing your Email Address", value="If you need to change your email address, please use the `/ad_edit` command with your new Email Address.\n\nFor example: ```/ad_edit [Example@Email.com]```", inline=False)
            await interaction.user.send(embed=embed, view=AdProfile.EmailButton())
            await self.bot.snowflake['log'].send(f"Started Advertiser Profile for {interaction.user.mention}")
            db.Advertisers.create(user_id=interaction.user.id, emails='', code="0")

async def setup(bot):
    await bot.add_cog(AdProfile(bot))