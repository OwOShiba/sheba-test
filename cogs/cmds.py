import discord
from discord.ext import commands
import asyncio
import sqlite3
import utils

class Cmds(commands.Cog):

	def __init__(self, bot):
		self.bot = bot


	

	@commands.command()
	@commands.cooldown(1, 5.0)
	async def hello(self, ctx):
		"""Says hello to the bot"""
		embed=discord.Embed(title=f"""Hiii ^w^""", description=None, color=discord.Color.from_rgb(0,255,110))
		embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
		await ctx.send(embed=embed)

	@commands.command()
	@commands.cooldown(1, 5.0)
	async def ping(self, ctx):
		"""Replies with \"Pong!\""""
		embed=discord.Embed(title=f"""Pong!""", description=None, color=discord.Color.from_rgb(0,255,110))
		embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
		await ctx.send(embed=embed)

	@commands.command()
	@commands.cooldown(1, 5.0)
	async def sendmsg(self, ctx, *, args=None):
		"""Makes the bot send the specified message"""
		embed=discord.Embed(title=f"""{args}""", description=None, color=discord.Color.from_rgb(0,255,110))
		embed.set_author(name="ShebaTest", icon_url=self.bot.user.avatar_url)
		await ctx.send(embed=embed)
		

def setup(bot):
	bot.add_cog(Cmds(bot))
	print('Commands have loaded')