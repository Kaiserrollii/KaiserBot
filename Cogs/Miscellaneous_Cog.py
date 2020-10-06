import discord
import asyncio
import datetime
import sqlite3 as sql
import pandas as pd 
import numpy as np
from discord.ext import commands 


class Miscellaneous_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Miscellaneous: Online')

    # Returns a general help page
    @commands.command(aliases = ['Help', 'pabo', 'Pabo'])
    async def help(self, ctx):

        embed = discord.Embed(title = '**KaiserBot Help Page**', colour = discord.Colour(0xefe61), 
        description = f'''*Read carefully, pabo.*
        \n__**Helpful Resources:**__
        :round_pushpin: [Obligatory Irene IG Plug](https://www.instagram.com/renebaebae/)
        :round_pushpin: [How to stan Olive - Ⅰ](https://www.youtube.com/watch?v=UkY8HvgvBJ8)
        :round_pushpin: [How to stan Olive - Ⅱ](https://www.youtube.com/watch?v=s7kxoMYg3l8)
        :round_pushpin: [How to stan Olive - Ⅲ](https://drive.google.com/drive/folders/18seLrChB-7VpqWVh3WQgUlexARIVTwXn)
        :round_pushpin: [Stan Jinsoul - Ⅳ](https://drive.google.com/drive/folders/1folanjOUnAqpWNFSVWKwBCV7TeJsDzcx?usp=sharing)
        ```Additional Resources:```\n'''
        '⤷ [Website](https://kaiserbotwebsite--kaiserrollii.repl.co/)\n\n'
        '⤷ Attach "_ex" to the end of any command with parameters to see an example. For instance, `k.choose_ex`.')

        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/637561476051238912/650462638433632272/5274dbb7a4a02ebb643cab87efde7fe0.png')
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
        icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    # Returns bot's ping
    @commands.command(aliases = ['Ping', 'pong', 'Pong'])
    async def ping(self, ctx):
        await ctx.send(f':round_pushpin: {round(self.bot.latency * 1000)}ms! :round_pushpin:')

    # Returns server icon
    @commands.command(aliases = ['Servericon', 'server_icon', 'Server_icon'])
    async def servericon(self, ctx):
        await ctx.send(ctx.guild.icon_url)

    # Returns bot's profile picture
    @commands.command(aliases = ['Boticon', 'bot_icon', 'Bot_icon'])
    async def boticon(self, ctx):
        await ctx.send('https://imgur.com/CuNlLOP.png')

    # Returns an invite link to Kaisercord
    @commands.command(aliases = ['kaisercord', 'Kaisercord', 'aicord', 'kaicord', 'Kaicord'])
    async def aisercord(self, ctx):
        await ctx.send('https://discord.gg/kjuX5TZ')

    # Consumes a parameter, member, which must be a valid user
    # Returns the profile picture of the specified user
    # If member is not given, defaults to self
    @commands.command(aliases = ['Avatar', 'av', 'Av', 'dp', 'Dp', 'pfp', 'Pfp'])
    async def avatar(self, ctx, *, member : discord.Member = None):
        if member is None:

            embed1 = discord.Embed()
            embed1.colour = 0xefe61
            embed1.set_author(name = f"{ctx.author.name}'s Avatar", icon_url = f'{ctx.author.avatar_url}')
            embed1.set_image(url = ctx.author.avatar_url)
            embed1.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed1.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed1)
        else:

            embed2 = discord.Embed()
            embed2.colour = 0xefe61
            embed2.set_author(name = f"{member.name}'s Avatar", icon_url = f'{member.avatar_url}')
            embed2.set_image(url = member.avatar_url)
            embed2.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed2.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed2)

    @commands.command(aliases = ['Avatar_ex', 'av_ex', 'Av_ex', 'dp_ex', 'Dp_ex', 'pfp_ex', 'Pfp_ex'])
    async def avatar_ex(self, ctx):
        await ctx.send("```k.avatar_ex @Kaiserrollii \n>>> [@Kaiserrollii's avatar]```")

    # Returns the bot website
    @commands.command(aliases = ['Website', 'site', 'Site'])
    async def website(self, ctx):
        await ctx.send('<https://kaiserbotwebsite.kaiserrollii.repl.co/>')

    # Returns the bot patreon page
    @commands.command(aliases = ['Patreon', 'simp', 'Simp'])
    async def patreon(self, ctx):
        await ctx.send('<https://www.patreon.com/kaiserbot>')

    @commands.command(aliases = ['Status', 'todo', 'Todo'])
    async def status(self, ctx):
        db = sql.connect('Status.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM todo ORDER BY Priority ASC;')
        result = cursor.fetchall()
        db.commit()
        cursor.close()
        db.close()

        priorities = list(map(lambda x: f'**{x[0]}** - ', result))
        tasks = list(map(lambda x: x[1], result))
        df = pd.DataFrame(data = {'': tasks}, index = priorities)

        guildcount = len(self.bot.guilds)
        membercount = len(self.bot.users)

        embed = discord.Embed(title = 'KaiserBot - Status', colour = discord.Colour(0xefe61),
        description = f'*Currently serving **{guildcount}** servers and **{membercount}** users.\n\nPriority - Task*\n{df}')
        embed.set_thumbnail(url = 'https://imgur.com/rYLKlN8.gif')
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed = embed)

    @commands.command(aliases = ['Status_add', 'task_add', 'Task_add'])
    async def status_add(self, ctx, priority, *, item):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only Kaiserrollii is allowed to do that, pabo.')
            return

        db = sql.connect('Status.sqlite')
        cursor = db.cursor()
        insert = (f'INSERT INTO todo(Priority, Task) VALUES(?, ?)')
        values = (priority, item)
        cursor.execute(insert, values)
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'Added `{item}` to the task list!')

    @commands.command(aliases = ['Status_add_ex', 'task_add_ex', 'Task_add_ex'])
    async def status_add_ex(self, ctx):
        await ctx.send('```k.status_add 1 Random task\n>>> [Adds "Random task" to the list at priority 1]```')

    @commands.command(aliases = ['Status_remove', 'task_remove', 'Task_remove'])
    async def status_remove(self, ctx, *, item):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only Kaiserrollii is allowed to do that, pabo.')
            return

        db = sql.connect('Status.sqlite')
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM todo WHERE Task Like "{item}"')
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'Removed `{item}` from the task list!')

    @commands.command(aliases = ['Status_remove_ex', 'task_remove_ex', 'Task_remove_ex'])
    async def status_remove_ex(self, ctx):
        await ctx.send('```k.status_remove Random task\n>>> [Removes "Random task" from the list]```')

    @commands.command()
    async def servers(self, ctx):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only Kaiserrollii is allowed to do that, pabo.')
            return
        
        await ctx.send(f'{len(self.bot.guilds)} | {len(self.bot.users)}')
        for i in self.bot.guilds:
            await ctx.send(f'{i.name} | {i.id} | {i.member_count}')

def setup(bot):
    bot.add_cog(Miscellaneous_Cog(bot))
