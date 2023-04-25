"""

-- Linux/macOS
python3 -m pip install -U discord.py

-- Windows
py -3 -m pip install -U discord.py

"""



import discord
from discord import app_commands

from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)

@bot.event
async def on_ready():
  print(f"{bot.user.name} s'est bien connecté !")

bot.run("TOKEN")