import discord
from discord import app_commands
from discord.ext import commands
import sys
import asyncio
import utils
import traceback
import os

os.environ['MY_TOKEN'] = "NzU3MzQ5MjQxNDQ1NDE3MTMw.GSMBr6.TiKmAI-9Aukb8x-KlLCXQzooxT2tbGgM99wXQk"

intents = discord.Intents.all()
intents.members = True
client = discord.Client(command_prefix='?', case_insensitive=True, intents=intents)
bot = commands.Bot(command_prefix='?', case_insensitive=True, intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
  await bot.change_presence(status=discord.Status.online, activity=discord.Game('Hello! Use ?help for more assistance.'))
  await tree.sync(guild=discord.Object(id=755813698920120320))
  print("Bot is ready")

  initial_extensions = ['cogs.react',
              'cogs.error',
              'cogs.welcome',
              'cogs.cmds',
              'cogs.imgur',
              'cogs.economy',
              'cogs.test',
              'cogs.about',
              'cogs.admin',
              'cogs.github']

  if __name__ == '__main__':
    for extension in initial_extensions:
      try:
        await bot.load_extension(extension)
      except Exception as e:
        print(f'Failed to load extension {extension}', file=sys.stderr)
        traceback.print_exc()
      

@bot.command()
@commands.cooldown(1, 5.0)
async def reload(ctx, cog: str):
  """Reloads certain cogs of the bot"""
  if utils.checkAdmin(ctx.author) == True:
    cogname = cog.capitalize()
    coglower = cog.lower()
    if cogname == "All":
      for extension in initial_extensions:
        try:
          await bot.unload_extension(f"{extension}")
          await bot.load_extension(f"{extension}")
        except Exception as e:
          await ctx.send(e)
      embed=discord.Embed(title=f"""All cogs have been reloaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
      await ctx.send(embed=embed)    
    elif f"cogs.{coglower}" in initial_extensions:
      try:
        await bot.unload_extension(f"cogs.{cog}")
        await bot.load_extension(f"cogs.{cog}")
        embed=discord.Embed(title=f"""The cog {cogname} was reloaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
        await ctx.send(embed=embed)
      except Exception as e:
        await ctx.send(e)
    else:
      embed=discord.Embed(title=f"""Please specify a valid cog, they can be viewed with `?help`""", description=None, color=discord.Color.from_rgb(204,34,0))
      await ctx.send(embed=embed)
  else:
    embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 5.0)
async def load(ctx, cog: str):
  """Loads certain cogs of the bot"""
  if utils.checkAdmin(ctx.author) == True:
    cogname = cog.capitalize()
    coglower = cog.lower()
    if cogname == "All":
      for extension in initial_extensions:
        try:
          await bot.load_extension(f"{extension}")
        except Exception as e:
          await ctx.send(e)
      embed=discord.Embed(title=f"""All cogs have been loaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
      await ctx.send(embed=embed)   
    elif f"cogs.{coglower}" in initial_extensions:
      try:
        await bot.load_extension(f"cogs.{cog}")
        embed=discord.Embed(title=f"""The cog {cogname} was loaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
        await ctx.send(embed=embed)
      except Exception as e:
        await ctx.send(e)
    else:
      embed=discord.Embed(title=f"""Please specify a valid cog, they can be viewed with `?help`""", description=None, color=discord.Color.from_rgb(204,34,0))
      await ctx.send(embed=embed)
  else:
    embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 5.0)
async def unload(ctx, cog: str):
  """Unloads certain cogs of the bot"""
  if utils.checkAdmin(ctx.author) == True:
    cogname = cog.capitalize()
    coglower = cog.lower()
    if cogname == "All":
      for extension in initial_extensions:
        try:
          await bot.unload_extension(f"{extension}")
        except Exception as e:
          await ctx.send(e)
      embed=discord.Embed(title=f"""All cogs have been unloaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
      await ctx.send(embed=embed)   
    elif f"cogs.{coglower}" in initial_extensions:
      try:
        await bot.unload_extension(f"cogs.{cog}")
        embed=discord.Embed(title=f"""The cog {cogname} was unloaded.""", description=None, color=discord.Color.from_rgb(0,255,110))
        await ctx.send(embed=embed)
      except Exception as e:
        await ctx.send(e)
    else:
      embed=discord.Embed(title=f"""Please specify a valid cog, they can be viewed with `?help`""", description=None, color=discord.Color.from_rgb(204,34,0))
      await ctx.send(embed=embed)
  else:
    embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
    await ctx.send(embed=embed)
  
@tree.command(name="hello", description = "say hi to bot", guild=discord.Object(id=755813698920120320))
async def hello(interaction):
  await interaction.response.send_message("Hello!")

bot.run(os.environ.get('MY_TOKEN'))
