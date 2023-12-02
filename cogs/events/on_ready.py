import discord
from discord.ext import commands
from json import dump

class OnReady(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    #gets list of channels and retrieves their snowflakes
    def channel_ids_to_snowflakes(self):
        for channel in self.bot.config["channels"]:
            try:
                loaded_channel = self.bot.snowflake[channel] = self.bot.get_channel(self.bot.config["channels"][channel])
            except:
                print(f"Failed to load channel {channel}")
            else:
                if loaded_channel != None:
                    print(f"Loaded channel {channel}")
                else:
                    print(f"Failed to load channel {channel}")

    #gets list of roles and retrieves their snowflakes
    def role_ids_to_snowflakes(self, guild : discord.Guild):
        loaded_roles = []
        failed_roles = []
        for role in self.bot.config["roles"]:
            try:
                self.bot.snowflake[role] = guild.get_role(self.bot.config["roles"][role])
            except:
                print(f"Failed to load role {role}")
                failed_roles.append(role)
            else:
                if  self.bot.snowflake[role] != None:
                    print(f"Loaded role {role}")
                    loaded_roles.append(role)
                else:
                    print(f"Failed to load role {role}")
                    failed_roles.append(role)

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

    @commands.Cog.listener('on_ready')
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name} ({self.bot.user.id})')
        print('------')
        #syncs slash commands
        sync = await self.bot.tree.sync()
        print(f'Synced {len(sync)} Slash Commands')

        self.channel_ids_to_snowflakes()
        self.guild_ids_to_snowflake()
        self.role_ids_to_snowflakes(self.bot.snowflake["guild"])

        #Lets the server know, the bot is online
        await self.bot.snowflake['log'].send(f"Logged in as {self.bot.user.name} ({self.bot.user.id})", delete_after=10)

async def setup(bot):
    await bot.add_cog(OnReady(bot))