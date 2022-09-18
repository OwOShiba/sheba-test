import discord
from discord.ext import commands
from discord.errors import Forbidden


async def send_embed(ctx, embed):
    try:
        await ctx.send(embed=embed)
    except Forbidden:
        try:
            await ctx.send("Hey, seems like I can't send embeds. Please check my permissions :)")
        except Forbidden:
            await ctx.author.send(
                f"Hey, seems like I can't send any message in {ctx.channel.name} on {ctx.guild.name}\n"
                f"Can you inform the server team about this issue? :slight_smile: ", embed=embed)


class About(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    @commands.cooldown(1, 15.0)
    async def about(self, ctx, *input):
        """Displays information about the bot and it's cogs"""
        prefix = "?"
        version =  "1.5"
        owner =  "Shiba"
        owner_name = "Shiba#5586"
        if not input:
            try:
                owner = ctx.guild.get_member(owner).mention

            except AttributeError as e:
                owner = owner

            emb = discord.Embed(title='Commands and modules', color=discord.Color.blue(),
                                description=f'Use `{prefix}about <module>` to gain more information about that module '
                                            f':smiley:\n')

            cogs_desc = ''
            for cog in self.bot.cogs:
                cogs_desc += f'`{cog}`\n'

            emb.add_field(name='Modules', value=cogs_desc, inline=False)

            commands_desc = ''
            for command in self.bot.walk_commands():
                if not command.cog_name and not command.hidden:
                    commands_desc += f'{command.name} - {command.help}\n'

            if commands_desc:
                emb.add_field(name='Not belonging to a module', value=commands_desc, inline=False)

            emb.add_field(name="About", value=f"A bot made by Shiba#5586.")
            emb.set_footer(text=f"Bot is running version {version}")

        elif len(input) == 1:

            for cog in self.bot.cogs:
                if cog.lower() == input[0].lower():

                    emb = discord.Embed(title=f'{cog} - Commands', description=None,
                                        color=discord.Color.green())

                    for command in self.bot.get_cog(cog).get_commands():
                        if not command.hidden:
                            emb.add_field(name=f"`{prefix}{command.name}`", value=command.help, inline=False)
                    break

            else:
                emb = discord.Embed(title="What's that?!",
                                    description=f"I've never heard from a module called `{input[0]}` before :scream:",
                                    color=discord.Color.orange())
        elif len(input) > 1:
            emb = discord.Embed(title="That's too much.",
                                description="Please request only one module at once :sweat_smile:",
                                color=discord.Color.orange())

        else:
            emb = discord.Embed(title="It's a magical place.",
                                description="I don't know how you got here.",
                                color=discord.Color.red())

        await send_embed(ctx, emb)


def setup(bot):
    bot.add_cog(About(bot))
    print("About is loaded")