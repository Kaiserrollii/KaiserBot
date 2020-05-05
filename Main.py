import discord 
import os
from discord.ext import commands 


fin = open('Confidential.txt')
line = fin.readline()
fin.close()

Token = line.strip()
bot = commands.Bot(command_prefix = 'k.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Status: Online') 
    activity = discord.Activity(name = 'Interstellar 🔭', type = discord.ActivityType.watching)
    return await bot.change_presence(activity = activity)

# Will be tweaked if bot goes public
@bot.command(aliases = ['Kill', 'end', 'End', 'exit', 'Exit'])
async def kill(ctx):
    if ctx.message.author.guild_permissions.administrator:
        await ctx.send('**Status:** Offline\n**Background Tasks:** Offline\n**Commands:** Offline\n**Events:** Offline\n**Games:** Offline\
        \n**Math:** Offline\n**Miscellaneous:** Offline\n**Moderation:** Offline\n')
        await bot.logout()
    else:
        await ctx.send("You don't have the perms. GIT GUD.")

@bot.command(aliases = ['Cog_online', 'cogon'])
async def cog_online(ctx, extension):
    if ctx.message.author.guild_permissions.administrator:
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f':white_check_mark: **{extension}** loaded.')
    else:
        await ctx.send("You don't have the perms. GIT GUD.")

@bot.command(aliases = ['Cog_offline', 'cogoff'])
async def cog_offline(ctx, extension):
    if ctx.message.author.guild_permissions.administrator:
        bot.unload_extension (f'cogs.{extension}')
        await ctx.send(f':x: **{extension}** unloaded.')
    else:
        await ctx.send("You don't have the perms. GIT GUD.")
        
for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(Token)





