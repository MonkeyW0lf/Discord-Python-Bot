import discord
from discord import app_commands
from discord.ext import commands

import os

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():

    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            if filename[:-3] not in ["view"]:
                await bot.load_extension(f"cogs.{filename[:-3]}")
                print("Cogs bien charge !")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)


bot.run("TOKEN")    