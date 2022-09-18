import discord
from discord.ext import commands
import asyncio

class Welcome(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.Cog.listener()
	async def on_member_join(self, member):
		channel = discord.utils.get(member.guild.channels, name='general')
		await channel.send(f'{member.mention} has joined the server! :D')

	@commands.Cog.listener()
	async def on_member_remove(self, member):
		channel = discord.utils.get(member.guild.channels, name='general')
		await channel.send(f'{member.mention} has left the server :(')

def setup(bot):
	bot.add_cog(Welcome(bot))
	print('Welcome is loaded')