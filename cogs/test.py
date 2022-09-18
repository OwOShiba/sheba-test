import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import asyncio
from datetime import datetime

class Test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(Test(bot))
    print('Test is loaded')