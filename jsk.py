import discord
from jishaku.cog import Jishaku
from discord.ext import commands

class Jsk(commands.Bot):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Jishaku(bot))