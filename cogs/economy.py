import discord
from discord.ext import commands
import asyncio
import sqlite3
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)
import utils

def getBal(user: discord.Member):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute(f"SELECT * FROM Balance WHERE member_id = {user.id}")
	result = cursor.fetchone()

	if result:
		return result[1]
	if not result:
		sql = "INSERT INTO Balance(member_id, balance) VALUES(?,?)"
		val = (user.id, 100)
		cursor.execute(sql, val)
		return 100
	
	main.commit()
	cursor.close()
	main.close()

def addBal(user: discord.Member, amount: int):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute(f"SELECT * FROM Balance WHERE member_id = {user.id}")
	result = cursor.fetchone()
	newAmount = result[1] + amount

	if result:
		sql = f"UPDATE Balance SET balance = {newAmount} WHERE member_id = {user.id}"

	cursor.execute(sql)
	main.commit()
	cursor.close()
	main.close()

def remBal(user: discord.Member, amount: int):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute(f"SELECT * FROM Balance WHERE member_id = {user.id}")
	result = cursor.fetchone()
	newAmount = result[1] - amount

	if result:
		sql = f"UPDATE Balance SET balance = {newAmount} WHERE member_id = {user.id}"

	cursor.execute(sql)
	main.commit()
	cursor.close()
	main.close()

def setBal(user: discord.Member, amount: int):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute(f"SELECT * FROM Balance WHERE member_id = {user.id}")
	result = cursor.fetchone()

	if result:
		sql = f"UPDATE Balance SET balance = {amount} WHERE member_id = {user.id}"

	cursor.execute(sql)
	main.commit()
	cursor.close()
	main.close()

def clearData(user: discord.Member):
	main = sqlite3.connect('main.db')
	cursor = main.cursor()
	cursor.execute(f"SELECT * FROM Balance WHERE member_id = {user.id}")
	result = cursor.fetchone()

	if result:
		cursor.execute(f"DELETE FROM Balance WHERE member_id = {user.id}")

	main.commit()
	cursor.close()
	main.close()

class Economy(commands.Cog):
	def __init__(self, bot):
		self.bot = bot


	@commands.command(aliases = ["bal"])
	@commands.cooldown(1, 5.0)
	async def balance(self, ctx, member : discord.Member = None):
		"""Displays your own or another member's balance"""
		if member == None:
			member = ctx.author
			getBal(member)
		else:
			getBal(member)
		main = sqlite3.connect('main.db')
		cursor = main.cursor()
		cursor.execute(f"SELECT * FROM Balance WHERE member_id = {member.id}")
		result = cursor.fetchone()
		if result is not None:
			if member == None:
				embed=discord.Embed(title=f"""{ctx.author.display_name}'s Balance""", description=f"**{result[1]}** Coins", color=discord.Color.from_rgb(0,255,110))
				embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
				await ctx.send(embed=embed)
			else:
				embed=discord.Embed(title=f"""{member.display_name}'s Balance""", description=f"**{result[1]}** Coins", color=discord.Color.from_rgb(0,255,110))
				embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
				await ctx.send(embed=embed)
		else:
			await ctx.send("Error")
		
	@commands.command(aliases = ["givemoney", "addmoney", "addbal"])
	@commands.cooldown(1, 5.0)
	async def give(self, ctx, member : discord.Member, amount : int):
		"""Adds the specified amount to a member's balance"""
		if utils.checkAdmin(ctx.author) == True:
			getBal(member)
			addBal(member, amount)
				
			main = sqlite3.connect('main.db')
			cursor = main.cursor()
			cursor.execute(f"SELECT * FROM Balance WHERE member_id = {member.id}")
			result = cursor.fetchone()
			if result is not None:
				embed=discord.Embed(title=f"""Updated Balance""", description=f"Added **{amount}** Coins to {member.mention}'s balance. \nNew balance: **{result[1]}**", color=discord.Color.from_rgb(0,255,110))
				embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
				await ctx.send(embed=embed)
			else:
				await ctx.send("Error")
		else:
			embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
			await ctx.send(embed=embed)

	@commands.command()
	@commands.cooldown(1, 5.0)
	async def pay(self, ctx, member : discord.Member, amount : int):
		"""Adds the specified amount to a member's balance"""
		mainbal = getBal(ctx.author)
		otherbal = getBal(member)

		if mainbal >= amount:
			addBal(member, amount)
			remBal(ctx.author, amount)
			embed=discord.Embed(title=f"""Updated Balance""", description=f"{ctx.author.mention} gave **{amount}** Coins to {member.mention}. \n{ctx.author.display_name}'s new balance: {getBal(ctx.author)} Coins", color=discord.Color.from_rgb(0,255,110))
			embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
			await ctx.send(embed=embed)
		else:
			embed=discord.Embed(title=f"""Sorry, you don't have enough money.""", description=None, color=discord.Color.from_rgb(204,34,0))
			await ctx.send(embed=embed)

	@commands.command(aliases = ["setmoney"])
	@commands.cooldown(1, 5.0)
	async def setBal(self, ctx, member : discord.Member, amount : int):
		"""Sets the balance of a specified member"""
		if utils.checkAdmin(ctx.author) == True:
			getBal(member)
			setBal(member, amount)

			main = sqlite3.connect('main.db')
			cursor = main.cursor()
			cursor.execute(f"SELECT * FROM Balance WHERE member_id = {member.id}")
			result = cursor.fetchone()
			if result is not None:
				if member == None:
					embed=discord.Embed(title=f"""Updated Balance""", description=f"Set {ctx.author.mention}'s balance to: **{result[1]}** Coins", color=discord.Color.from_rgb(0,255,110))
					embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
					await ctx.send(embed=embed)
				else:
					embed=discord.Embed(title=f"""Updated Balance""", description=f"Set {member.mention}'s balance to: **{result[1]}** Coins", color=discord.Color.from_rgb(0,255,110))
					embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
					await ctx.send(embed=embed)
			else:
				await ctx.send("Error")
		else:
			embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
			await ctx.send(embed=embed)

	@commands.command(aliases = ["submoney", "subtractmoney", "removemoney", "removebal", "subbal"])
	@commands.cooldown(1, 5.0)
	async def remove(self, ctx, member : discord.Member, amount : int):
		"""Removes the specified amount from a member's balance"""
		if utils.checkAdmin(ctx.author) == True:
			getBal(member)
			remBal(member, amount)

			main = sqlite3.connect('main.db')
			cursor = main.cursor()
			cursor.execute(f"SELECT * FROM Balance WHERE member_id = {member.id}")
			result = cursor.fetchone()
			if result is not None:
				if member == None:
					embed=discord.Embed(title=f"""Updated Balance""", description=f"Subtracted **{amount}** Coins from {ctx.author.mention}'s balance. \nNew balance: **{result[1]}**", color=discord.Color.from_rgb(0,255,110))
					embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
					await ctx.send(embed=embed)
				else:
					embed=discord.Embed(title=f"""Updated Balance""", description=f"Subtracted **{amount}** Coins from {member.mention}'s balance. \nNew balance: **{result[1]}**", color=discord.Color.from_rgb(0,255,110))
					embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
					await ctx.send(embed=embed)
			else:
				await ctx.send("Error")
		else:
			embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
			await ctx.send(embed=embed)

	@commands.command(aliases = ["clearbal", "resetbal", "cleardata"])
	@commands.cooldown(1, 40.0)
	async def resetData(self, ctx):
		"""Resets your data with the currency system"""
		member = ctx.author
		getBal(member)

		main = sqlite3.connect('main.db')
		cursor = main.cursor()
		cursor.execute(f"SELECT * FROM Balance WHERE member_id = {member.id}")
		result = cursor.fetchone()
		if result is not None:
			embed=discord.Embed(title=f"""Reset Data""", description=f"Are you sure you wish to reset your balance? This will time out in 30 seconds.", color=discord.Color.from_rgb(0,255,110))
			embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
			msg = await ctx.send(embed=embed, components=[
					# Button(style=ButtonStyle.green, label="YES"),
					# Button(style=ButtonStyle.red, label="NO")
					Select(
					placeholder="Please select yes or no",
					max_values=2,
					options=[
						SelectOption(label="YES", value="YES"),
						SelectOption(label="NO", value="NO"),
					],)], delete_after=30.0)
			while True:
				interaction = await self.bot.wait_for("select_option")
				if interaction.user.id == member.id:
					if interaction.message.id == msg.id:
						if interaction.component[0].label == "YES":
							clearData(member)
							embed=discord.Embed(title=f"""Reset Data""", description=f"Cleared {member.mention}'s data.", color=discord.Color.from_rgb(0,255,110))
							embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
							await ctx.send(embed=embed)
						elif interaction.component[0].label == "NO":
							embed=discord.Embed(title=f"""Reset Data""", description="Action aborted.", color=discord.Color.from_rgb(204,34,0))
							embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
							await ctx.send(embed=embed)
						await msg.delete()
						
		else:
			await ctx.send("Error")

	@commands.command(aliases=["top5", "lb", "baltop"])
	@commands.cooldown(1, 5.0)
	async def leaderboard(self, ctx):
		"""Displays the top 5 users with the highest balance"""
		main = sqlite3.connect('main.db')
		cursor = main.cursor()
		cursor.execute(f"SELECT member_id FROM Balance ORDER BY balance DESC")
		result = cursor.fetchall()

		cursor.close()
		main.close()

		array = []
		for i in result:
			main = sqlite3.connect('main.db')
			cursor = main.cursor()
			cursor.execute(f"SELECT * FROM Balance WHERE member_id = {i[0]}")
			result1 = cursor.fetchone()
			member = await self.bot.fetch_user(i[0])
			membername = member.display_name
			memberbal = result1[1]
			array.append(f"**{membername}** - {memberbal}")
		if len(array) < 5:
				for a in range(5 - len(array)):
					array.append('** **')

		embed = discord.Embed(title = "**Leaderboard**", description = None, color = discord.Color.from_rgb(0,255,110))
		
		j = 1
		f = 0
		for a in array:
			embed.add_field(name=f"#{j}", value=f"{array[f]} \n** **", inline=False)
			j=j+1
			f=f+1
		await ctx.send(embed=embed)

    

def setup(bot):
	bot.add_cog(Economy(bot))
	print('Economy is loaded')