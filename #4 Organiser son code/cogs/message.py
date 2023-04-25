import discord

from discord.ext import commands
from discord import app_commands

class Message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content == "QUOI":
            await message.channel.send('FEUR !')


async def setup(bot):
    await bot.add_cog(Message(bot))