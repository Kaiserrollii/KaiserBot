import discord
import traceback
import sys
import datetime
from discord.ext import commands

class Error_Handler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Error_Handler: Online')

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':
                await ctx.send('I could not find that member. Please try again.')

        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('You are missing a required argument. Please review the necessary parameters.')

        elif isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f'This command is on cooldown. Try again in **{datetime.timedelta(seconds = int(error.retry_after))}**.')

        else:
            print('Ignoring exception in command {}:'.format(ctx.command), file = sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file = sys.stderr)
            await ctx.send('An error has occurred. :pensive:')

def setup(bot):
    bot.add_cog(Error_Handler(bot))