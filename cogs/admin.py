import discord
from discord.ext import commands
import asyncio
import utils

class Admin(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def addAdmin(self, ctx, member : discord.Member):
        """Adds an admin to the bot's permissions"""
        if utils.checkOwner(ctx.author) == True:
            if utils.checkAdmin(member) == True:
                embed=discord.Embed(title=f"""{member.mention} is already an admin!""", description=None, color=discord.Color.from_rgb(204,34,0))
                embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
                await ctx.send(embed=embed)
            else:
                utils.newAdmin(member)
                embed=discord.Embed(title=f"""Appointed new admin of the bot: {member.mention}""", description=None, color=discord.Color.from_rgb(0,255,110))
                embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
            await ctx.send(embed=embed)

    @commands.command()
    async def delAdmin(self, ctx, member : discord.Member):
        """Adds an admin to the bot's permissions"""
        if utils.checkOwner(ctx.author) == True:
            if utils.checkAdmin(member) == False:
                embed=discord.Embed(title=f"""{member.mention} is not an admin!""", description=None, color=discord.Color.from_rgb(204,34,0))
                embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
                await ctx.send(embed=embed)
            else:
                utils.delAdmin(member)
                embed=discord.Embed(title=f"""Removed admin of the bot from: {member.mention}""", description=None, color=discord.Color.from_rgb(0,255,110))
                embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title=f"""Sorry, you don't have permission for this.""", description=None, color=discord.Color.from_rgb(204,34,0))
            await ctx.send(embed=embed)
    
    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.cooldown(1, 10.0)
    async def kick(self, ctx, member : discord.Member, *, reason=None):
        """Kicks a member"""
        if ctx.author == member:
            await ctx.send("Please don't kick yourself :(")
        else:
            await member.kick(reason=reason)
            embed=discord.Embed(title=f"""{member.mention} has been kicked.""", description=None, color=discord.Color.from_rgb(0,255,110))
            embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 10.0)
    async def ban(self, ctx, member : discord.Member, *, reason=None):
        """Bans a member"""
        if ctx.author == member:
            await ctx.send("Please don't kick yourself :(")
        else:
            await member.send(f"You have been banned from {ctx.guild.name}")
            embed=discord.Embed(title=f"""{member.mention} has been banned.""", description=None, color=discord.Color.from_rgb(0,255,110))
            embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 10.0)
    async def unban(self, ctx, *, member):
        """Unbans a member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                embed=discord.Embed(title=f"""Unbanned {user.name}#{user.discriminator}""", description=None, color=discord.Color.from_rgb(0,255,110))
                embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
                await ctx.send(embed=embed)
                return

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 10.0)
    async def clear(self, ctx, amount : int):
        
        """Deletes a certain amount of messages from a channel"""
        await ctx.channel.purge(limit=amount)
        embed=discord.Embed(title=f"""Deleted {amount} of messages.""", description=None, color=discord.Color.from_rgb(0,255,110))
        embed.set_footer(icon_url=f'{ctx.author.avatar_url}', text=f'{ctx.author} - {utils.getTime()}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Admin(bot))
    print('Admin has loaded')