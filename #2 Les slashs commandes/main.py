### ATTENTION ###
"""
Le fait de spécifier le serveur (=guild) à chaque fois, ne sert à rien!
Il a donc été supprimé...
"""


import discord
from discord import app_commands

from discord.ext import commands

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@bot.event
async def on_ready():
    print("Bot running with:")
    print("Username: ", bot.user.name)
    print("User ID: ", bot.user.id)

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands(s)")
    except Exception as e:
        print(e)

def is_owner():
    def predicate(interaction: discord.Interaction):
        if interaction.user.id == interaction.guild.owner_id:
            return True
    return app_commands.check(predicate)

@bot.tree.command(name='test', description='Cette commande est un test !')
async def test_slash(interaction: discord.Interaction):
    await interaction.response.send_message("TEST!")

@bot.tree.command(name='owner', description='Cette commande est réservé pour le propriétaire du serveur!')
@is_owner()
async def owner_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}!", ephemeral=True)

bot.run("TOKEN")