import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv
from json import load, dump
from asyncio import run

load_dotenv("keys.env")

bot = commands.Bot(command_prefix="-", intents=discord.Intents.all())
bot.snowflake = {}
with open("config.json", "r") as f:
    bot.config = load(f)
if bot.config["channels"]["log"] == '':
    log_channel_id = input("Please enter the ID of the log channel: ")
    bot.config["channels"]["log"] = int(log_channel_id)
    with open("config.json", "w") as f:
        dump(bot.config, f, indent=4)

async def load_cogs():
    with open(file=bot.config["cog_list_file_path"], mode="r") as cog_list:
        cog_list = load(cog_list)
        cogs_loaded = []
        cogs_failed = []
        for cog in cog_list["cogs"]:
            try:
                await bot.load_extension(cog)
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")
                cogs_failed.append(cog)
            else:
                cogs_loaded.append(cog)
                print(f"Loaded cog {cog}")
        print(f"Loaded Cogs: {len(cogs_loaded)} | Failed Cogs: {len(cogs_failed)}")
        print(f"Failed Cogs: {cogs_failed}")

run(load_cogs())

bot.run(getenv("DISCORD"))