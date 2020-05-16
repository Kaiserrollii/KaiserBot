import discord 
import os
from discord.ext import commands 


fin = open('Saved/Confidential.txt')
lines = list(map(lambda x: x.strip(), fin.readlines()))
fin.close()

Token = lines[0]

bot = commands.Bot(command_prefix = 'k.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Status: Online') 
    activity = discord.Activity(name = 'Interstellar 🔭', type = discord.ActivityType.watching)
    return await bot.change_presence(activity = activity)

@bot.command(aliases = ['Kill', 'end', 'End', 'exit', 'Exit'])
async def kill(ctx):
    if ctx.message.author.id == 496181635952148483:
        await ctx.send('**Status:** Offline\n**Background Tasks:** Offline\n**Data:** Offline\n**Events:** Offline\n**Games:** Offline\
        \n**Images:** Offline\n**Math:** Offline\n**Miscellaneous:** Offline\n**Moderation:** Offline\n')
        await bot.logout()
    else:
        await ctx.send("Sorry, but you're not the bot owner.")

@bot.command(aliases = ['Cog_online', 'cogon'])
async def cog_online(ctx, extension):
    if ctx.message.author.id == 496181635952148483:
        bot.load_extension(f'Cogs.{extension}')
        await ctx.send(f':white_check_mark: **{extension}** loaded.')
    else:
        await ctx.send("Sorry, but you're not the bot owner.")

@bot.command(aliases = ['Cog_offline', 'cogoff'])
async def cog_offline(ctx, extension):
    if ctx.message.author.id == 496181635952148483:
        bot.unload_extension (f'Cogs.{extension}')
        await ctx.send(f':x: **{extension}** unloaded.')
    else:
        await ctx.send("Sorry, but you're not the bot owner.")
        
for filename in os.listdir('./Cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'Cogs.{filename[:-3]}')


bot.run(Token)
