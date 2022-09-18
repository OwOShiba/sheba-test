from github import Github
import discord
from discord.ext import commands
import utils


g = Github("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")
repo = g.get_repo("OwOShiba/sheba-test")
rgb = discord.Color.from_rgb(0,255,110)

class Github(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.cooldown(1, 25.0)
    async def issue(self, ctx, title : str, *, desc : str):
        """Flags an issue for admins of the bot"""
        
        repo.create_issue(title=f"{title}", body=f"{desc}      Created by {ctx.author}")
        embed = discord.Embed(title='Issue Created', description=f'{title} \n** **  \n{desc}', color=rgb)
        embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=["suggestion"])
    @commands.cooldown(1, 25.0)
    async def suggest(self, ctx, title : str, *, desc : str):
        """Creates a suggestion for the bot that admins to look at"""
        
        repo.create_issue(title=f"{title}", body=f"{desc}      Created by {ctx.author}")
        embed = discord.Embed(title='Suggestion Created', description=f'{title} \n** **  \n{desc}', color=rgb)
        embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Github(bot))
    print("Github is loaded")