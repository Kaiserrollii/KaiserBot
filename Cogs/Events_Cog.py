import discord 
import datetime 
import asyncio
from discord.ext import commands 


class Events_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Events: Online')

    # Welcome message, autorole, and bot DM when a new user joins the server
    @commands.Cog.listener()
    async def on_member_join(self, member): 
        autorole = discord.utils.get(member.guild.roles, name = 'Hydrated')
        channel = self.bot.get_channel(id = 623770537340174336)
        channel2 = self.bot.get_channel(id = 623772413397696513)

        embed = discord.Embed\
        (title = 'Extremely Helpful Starter Guide Part Ⅰ', 
        colour = discord.Colour(0xefe61),
        url = 'https://www.youtube.com/watch?v=YijhXZx88cI',
        description = f':tada: Welcome, {member.mention}!\
        Please check the **Starter Guide** linked above, as well as [Part Ⅱ](https://revelupsubs.com/level-up-project/) and\
        [Part Ⅲ](https://www.youtube.com/watch?v=kpsuuAAaG48). Afterwards, {channel2.mention} is here to help you get acquainted with the server,\
        and `k.help` will answer all your bot inquiries. :confetti_ball: Have fun, nerd.')
        embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/637561476051238912/650177237211021312/13f908c41de53de2b94ea89c0804b1b0.jpg')
        embed.set_author(name = 'Welcome to Kaisercord!', url = 'https://discord.gg/kjuX5TZ', icon_url = f'{member.avatar_url}')
        embed.set_footer(text = f'Member #{len(list(member.guild.members))} | KaiserBot | Kaisercord', icon_url = f'{member.guild.icon_url}')
        embed.timestamp = datetime.datetime.utcnow()

        await channel.send(embed = embed)
        await member.add_roles(autorole)
        await member.send("Welcome to Kaisercord! I'm KaiserBot: the server's personal bot.\nFor more information about me, head to \
https://kaiserbotwebsite--kaiserrollii.repl.co/")


def setup (bot):
    bot.add_cog(Events_Cog(bot))
