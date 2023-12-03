import discord
from discord.ext import commands
from discord import app_commands
import datetime
import os

class FreezeTicket(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="freeze_ticket", description="freezes a ticket")
    async def freeze_ticket(self, interaction: discord.Interaction):
        '''
        ## Zenith Collective

        ### Parameters

        `interaction` = discord.Interaction

        ### Returns

        `None`

        ### Description

        Freeze a ticket.

        Checks if the ticket is already frozen, and if not, freezes the ticket.
        '''

        await interaction.response.send_message("This might take a second! Please wait while we freeze the ticket to a file for you!")

        # Create a file to store the messages
        file_path = f"transripts/transcript-{interaction.channel.id}.txt"

        # Check if the file already exists
        if os.path.exists(file_path):
            os.remove(file_path)

        # Create the file
        with open(file_path, "a") as file:
            # Iterate through all messages in the channel
            async for message in interaction.channel.history(limit=None):
                # Check if the message has content and is not a media file
                if message.content and not message.attachments:
                    # Write the message details to the file
                    file.write(f"{message.created_at} - {message.author}: {message.content}\n")
        
        # Send the file as an attachment
        await interaction.channel.send("here is the transcript!", file=discord.File(file_path))
        
async def setup(bot : commands.Bot):
    await bot.add_cog(FreezeTicket(bot))