import discord
from discord.ext import commands
import random as r
from imgurpython import ImgurClient

imgur = ImgurClient("10566f247b8fb31","24ae94e5eb9f6a238c7606c00b52bd565da0e385")

class Imgur(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(name='imgur', pass_context=True)
	@commands.cooldown(1, 5.0)
	async def imgur(self, ctx, *text: str):
		"""Allows the user to search for an image from imgur"""
		rand = r.randint(0, 29)
		if text == ():
			embed=discord.Embed(title=f"""Please enter a search term.""", description=None, color=discord.Color.from_rgb(204,34,0))
			await ctx.send(embed=embed)
		elif text[0] != ():
			items = imgur.gallery_search(" ".join(text[0:len(text)]), advanced=None, sort='viral', window='all',page=0)
			await ctx.send(items[rand].link)

def setup(bot):
	bot.add_cog(Imgur(bot))
	print('Imgur is loaded')