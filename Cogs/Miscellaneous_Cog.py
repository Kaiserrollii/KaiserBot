import discord
import asyncio
import datetime
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
        icon_url = f'{ctx.guild.icon_url}')
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
        await ctx.send('https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')

    # Returns an invite link to Kaisercord
    @commands.command(aliases = ['Invite', 'inv', 'Inv'])
    async def invite(self, ctx):
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
            icon_url = f'{ctx.guild.icon_url}')
            embed1.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed1)
        else:

            embed2 = discord.Embed()
            embed2.colour = 0xefe61
            embed2.set_author(name = f"{member.name}'s Avatar", icon_url = f'{member.avatar_url}')
            embed2.set_image(url = member.avatar_url)
            embed2.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = f'{ctx.guild.icon_url}')
            embed2.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed2)

    @commands.command(aliases = ['Avatar_ex', 'av_ex', 'Av_ex', 'dp_ex', 'Dp_ex', 'pfp_ex', 'Pfp_ex'])
    async def avatar_ex(self, ctx):
        await ctx.send("```k.avatar_ex @Kaiserrollii \n>>> [@Kaiserrollii's avatar]```")

    # Returns the bot website
    @commands.command(aliases = ['Website', 'site', 'Site'])
    async def website(self, ctx):
        await ctx.send('https://tinyurl.com/kaiserbotwebsite')

    # Returns the bot patreon page
    @commands.command(aliases = ['Patreon', 'simp', 'Simp'])
    async def patreon(self, ctx):
        await ctx.send('<https://www.patreon.com/kaiserbot>')


def setup(bot):
    bot.add_cog(Miscellaneous_Cog(bot))
