import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from json import load, dump

class ConfigManager(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    @app_commands.command(name="set_channel", description="Sets a channel to a role")
    @app_commands.choices(channel_choices = [
        Choice(name="log", value="log"),
        Choice(name="welcome", value="welcome"),
        Choice(name="support channel", value="ticket_category"),
    ])
    async def set_channel(self, interaction : discord.Interaction, channel_choices: Choice[str]):
        if interaction.user.guild_permissions.manage_channels:
            if channel_choices.value == "ticket_category":
                await interaction.response.send_message("Please mention the category you would like to set as the ticket category", ephemeral=False)
                category = await self.bot.wait_for("message", check=lambda m: m.author == interaction.user and m.channel == interaction.channel)
                self.bot.config["channels"][channel_choices.value] = category.id
                with open("config.json", "w") as f:
                    dump(self.bot.config, f, indent=4)
                return
            with open("config.json", "w") as f:
                self.bot.config["channels"][channel_choices.value] = interaction.channel.id
                dump(self.bot.config, f, indent=4)
            await interaction.response.send_message(f"Set channel {channel_choices.value} to {interaction.channel.mention}")
            await self.bot.snowflake['log'].send(f"Set channel {channel_choices.value} to {interaction.channel.mention} by {interaction.user.mention}")
    
    @app_commands.command(name="set_role", description="Sets a role to a channel")
    @app_commands.choices(role_choices = [
        Choice(name="mod", value="mod"),
        Choice(name="admin", value="admin"),
        Choice(name="mute", value="mute"),
        Choice(name="bot", value="bot"),
        Choice(name="member", value="member"),
    ])
    async def set_role(self, interaction : discord.Interaction, role_choices: Choice[str], role: discord.Role):
        '''
        Purpose: Assigns the role.id of the role value to the config file?

        Parameters: interaction - discord.Interaction, roles_choices - Choice[str], role - discord.Role

        Returns: None
        '''
        if interaction.user.guild_permissions.manage_roles:
            self.bot.config["roles"][role_choices.value] = role.id
            with open("config.json", "w") as f:
                dump(self.bot.config, f, indent=4)
            await interaction.response.send_message(f"Set role {role_choices.value} to {role.mention}")
            

    @app_commands.command(name="reload_cogs", description="Reloads all cogs")
    async def reload_cogs(self, interaction : discord.Interaction):
        '''
        Purpose: reload all cog files for the discord bot.

        Parameters: interaction - discord.Interaction

        Returns: None
        '''
        if interaction.user.guild_permissions.manage_channels:
            with open(file=self.bot.config["cog_list_file_path"], mode="r") as cog_list:
                cog_list = load(cog_list) 
                cogs_loaded = [] 
                cogs_failed = []
                for cog in cog_list["cogs"]:
                    try:
                        await self.bot.reload_extension(cog)
                    except Exception as e:
                        print(f"Failed to load cog {cog}: {e}")
                        cogs_failed.append(cog)
                    else:
                        cogs_loaded.append(cog)
                        print(f"Loaded cog {cog}")
                print(f"Loaded Cogs: {len(cogs_loaded)} | Failed Cogs: {len(cogs_failed)}")
                print(f"Failed Cogs: {cogs_failed}")
                await interaction.response.send_message(f"Loaded Cogs: {len(cogs_loaded)} | Failed Cogs: {len(cogs_failed)}")
    
    @app_commands.command(name="load_cog", description="loads a cog")
    async def load_cog(self, interaction : discord.Interaction, cog_name: str):
        if interaction.user.guild_permissions.manage_channels:
            try:
                await self.bot.load_extension(cog_name)
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")
                await interaction.response.send_message(f"Failed to load cog {cog_name}: {e}")
            else:
                print(f"Loaded cog {cog_name}")
                await interaction.response.send_message(f"Loaded cog {cog_name}")

    @app_commands.command(name="reload_cog", description="reloads a cog")
    async def reload_cog(self, interaction : discord.Interaction, cog_name: str):
        if interaction.user.guild_permissions.manage_channels:
            try:
                await self.bot.reload_extension(cog_name)
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")
                await interaction.response.send_message(f"Failed to load cog {cog_name}: {e}")
            else:
                print(f"Loaded cog {cog_name}")
                await interaction.response.send_message(f"Loaded cog {cog_name}")

    @app_commands.command(name="sync_commands", description="syncs slash commands")
    async def sync_commands(self, interaction : discord.Interaction):
        if interaction.user.guild_permissions.manage_channels:
            sync = await self.bot.tree.sync()
            await interaction.response.send_message(f"Synced {len(sync)} Slash Commands")

    def guild_ids_to_snowflake(self):
        try:
            self.bot.snowflake["guild"] = self.bot.get_guild(self.bot.config["guild"])
        except Exception as e:
            print(f"Failed to load guild" + "[]" + str(e))
        else:
            if self.bot.snowflake["guild"] == None:
                print(f"Failed to load guild")
                return
            print(f"Loaded guild")

    #gets list of channels and retrieves their snowflakes
    def channel_ids_to_snowflakes(self):
        loaded_channels = []
        failed_channels = []
        for channel in self.bot.config["channels"]:
            try:
                loaded_channel = self.bot.snowflake[channel] = self.bot.snowflake['guild'].get_channel(self.bot.config["channels"][channel])
            except Exception as e:
                print(f"Failed to load channel {channel} | {e}")
                failed_channels.append(channel)
            else:
                if loaded_channel != None:
                    print(f"Loaded channel {channel}")
                    loaded_channels.append(channel)
                else:
                    print(f"Failed to load channel {channel} | Channel not found")
                    failed_channels.append(channel)
        return f"{len(loaded_channels)}/{len(self.bot.config['channels'])}"

    #gets list of roles and retrieves their snowflakes
    def role_ids_to_snowflakes(self, guild : discord.Guild):
        loaded_roles = []
        failed_roles = []
        for role in self.bot.config["roles"]:
            try:
                self.bot.snowflake[role] = guild.get_role(self.bot.config["roles"][role])
            except Exception as e:
                print(f"Failed to load role {role} | {e}")
                failed_roles.append(role)
            else:
                if self.bot.snowflake[role] != None:
                    print(f"Loaded role {role}")
                    loaded_roles.append(role)
                else:
                    print(f"Failed to load role {role}")
                    failed_roles.append(role)

        return f"{len(loaded_roles)}/{len(self.bot.config['roles'])}"

    @app_commands.command(name="reload_snowflakes", description="loads snowflakes into memory")
    async def load_snowflakes(self, interaction : discord.Interaction):
        if interaction.user.guild_permissions.manage_channels:
            self.bot.snowflake = {}
            self.guild_ids_to_snowflake()
            channel_success_rate = self.channel_ids_to_snowflakes()
            role_success_rate = self.role_ids_to_snowflakes(guild=interaction.guild)
            await interaction.response.send_message(f"Loaded snowflakes ({channel_success_rate} channels, {role_success_rate} roles)")

async def setup(bot):
    await bot.add_cog(ConfigManager(bot))