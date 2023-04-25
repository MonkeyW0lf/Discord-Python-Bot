import discord
from discord import app_commands
from discord.ext import commands


import random
from datetime import datetime
import datetime


import calendar
import time
ts = calendar.timegm(time.gmtime())

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="$", intents=intents)


client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


funFact = ["𝘔𝘖𝘕𝘒𝘌𝘠 𝘍𝘙𝘌𝘕𝘊𝘏"]


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


@bot.tree.command(name='ban', description="Bannir un membre")
@is_owner()
@app_commands.describe(
    user='Le membre à bannir.',
    reason='La raison du ban.',
)
async def ban_slash(interaction: discord.Interaction, user: discord.Member, reason: str = None):

    if reason is None:
        reason = "Aucune raison n'a été donnée"

    guild = bot.get_guild(1093998201608081438)
    channel = guild.get_channel(992516724446470234)

    await guild.ban(user, reason=reason)

    embed = discord.Embed(title="__**Banissement**__",
                          description="Un modérateur a ban un membre !", color=0xff0000)
    embed.add_field(name="Information Utilisateur :",
                    value=f"➔ `Utilisateur` : {user.mention}\n➔ `Nom` : {user.name}#{user.discriminator}\n➔ `ID` : {user.id}\n➔ `Bot` : {user.bot}", inline=False)
    embed.add_field(name="Information Banissement :",
                    value=f"➔ `Date` : <t:{ts}:R>\n➔ `Modérateur Responsable` : {interaction.user.mention}\n➔ `Raison` :\n```{reason}```", inline=False)
    embed.set_footer(text=random.choice(funFact))
    embed.timestamp = datetime.datetime.now()

    await interaction.response.send_message(embed=embed, ephemeral=True)
    await channel.send(embed=embed)


@ban_slash.error
async def say_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("Tu n'as pas les permissions !", ephemeral=True)


@bot.tree.command(name='clear', description="Supprimer des messages")
@is_owner()
@app_commands.describe(
    amount='Le nombre de messages à supprimer.',
)
async def clear_slash(interaction: discord.Interaction, amount: int, channel: discord.TextChannel = None):

    guild = bot.get_guild(1093998201608081438)
    channel1 = guild.get_channel(998667695857864864)

    if channel is None:
        channel = interaction.channel

    embed = discord.Embed(title="__**Messages Supprimés**__",
                          description="Un modérateur a supprimé des messages !", color=0x07f246)
    embed.add_field(name="Information Modérateur :",
                    value=f"➔ `Utilisateur` : {interaction.user.mention}\n➔ `Nom` : {interaction.user.name}#{interaction.user.discriminator}\n➔ `ID` : {interaction.user.id}\n➔ `Bot` : {interaction.user.bot}", inline=False)
    embed.add_field(name="Information Messages :",
                    value=f"➔ `Date` : <t:{ts}:R>\n➔ `Salon` : {channel.mention}\n➔ `Nombre` :\n```{amount}```", inline=False)
    embed.set_footer(text=random.choice(funFact))
    embed.timestamp = datetime.datetime.now()

    await interaction.response.send_message(embed=embed, ephemeral=True)
    await channel1.send(embed=embed)
    await channel.purge(limit=amount)


@clear_slash.error
async def say_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("Tu n'as pas les permissions !", ephemeral=True)


@bot.tree.command(name='unban', description="Unban un membre")
@is_owner()
@app_commands.describe(
    user='Le membre à unban.',
)
async def unban_slash(interaction: discord.Interaction, user: str):
    guild = bot.get_guild(1093998201608081438)
    channel = guild.get_channel(992516724446470234)

    mod = interaction.user.mention
    reason = " ".join(reason)
    userName, userId = user.split("#")
    bannedUsers = interaction.guild.bans()
    async for i in bannedUsers:
        if i.user.name == userName and i.user.discriminator == userId:

            embed = discord.Embed(title="__**Membre Débanni**__",
                                  description="Un modérateur a débanni un membre !", color=0x07f246)
            embed.add_field(name="Information Utilisateur :",
                            value=f"➔ `Nom` : {user}", inline=False)
            embed.add_field(name="Information Messages :",
                            value=f"➔ `Date` : <t:{ts}:R>\n➔ `Modérateur Responsable` : {mod}", inline=False)
            embed.set_footer(text=random.choice(funFact))
            embed.timestamp = datetime.datetime.now()
            await interaction.guild.unban(i.user)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            await channel.send(embed=embed)
            return
    # Ici on sait que lutilisateur na pas ete trouvé
    await interaction.response.send_message(f"L'utilisateur {user} n'est pas dans la liste des bans")

@unban_slash.error
async def say_error(interaction: discord.Interaction, error):
    await interaction.response.send_message("Tu n'as pas les permissions !", ephemeral=True)

bot.run("TOKEN")    