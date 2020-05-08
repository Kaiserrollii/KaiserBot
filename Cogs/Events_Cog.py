import discord 
import datetime 
import sys 
import sqlite3
from discord.ext import commands 


class Events_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 

    @commands.Cog.listener()
    async def on_ready(self):
        print('Events: Online')

    # Welcome message, autorole, and bot DM when a new user joins Kaisercord
    # Customizable welcome message and autorole when a new user joins any other server
    # Not in use at the moment (for when bot begins joining other servers)
    @commands.Cog.listener()
    async def on_member_join(self, member): 
        if member.guild.id == 604539500223397898:
            autorole = discord.utils.get(member.guild.roles, name = 'Hydrated')
            channel = self.bot.get_channel(id = 623770537340174336)
            channel2 = self.bot.get_channel(id = 623772413397696513)

            embed = discord.Embed(title = 'Extremely Helpful Starter Guide Part Ⅰ', colour = discord.Colour(0xefe61),
            url = 'https://www.youtube.com/watch?v=YijhXZx88cI', description = f':tada: Welcome, {member.mention}!\
            Please check the **Starter Guide** linked above, as well as [Part Ⅱ](https://revelupsubs.com/level-up-project/) and\
            [Part Ⅲ](https://www.youtube.com/watch?v=kpsuuAAaG48). Afterwards, {channel2.mention} is here to help you get acquainted with the server,\
            and `k.help` will answer all your bot inquiries. :confetti_ball: Have fun, nerd.')
            embed.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/637561476051238912/650177237211021312/13f908c41de53de2b94ea89c0804b1b0.jpg')
            embed.set_author(name = f'Welcome to {member.guild.name}!', url = 'https://discord.gg/kjuX5TZ', icon_url = f'{member.avatar_url}')
            embed.set_footer(text = f'Member #{len(list(member.guild.members))} | KaiserBot | {member.guild.name}', icon_url = f'{member.guild.icon_url}')
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed = embed)
            await member.add_roles(autorole)
            await member.send(f"Welcome to {member.guild.name}! I'm KaiserBot: the server's personal bot.\nFor more information about me, head to \
    https://kaiserbotwebsite--kaiserrollii.repl.co/")

        else:
            db = sqlite3.connect('cogs/EventsDB.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT Channel_ID FROM EventsDB WHERE Guild_ID = {member.guild.id}')
            channelID = cursor.fetchone()
            if channelID is None:
                return 
            else:
                cursor.execute(f'SELECT WMessage FROM EventsDB WHERE Guild_ID = {member.guild.id}')
                message = cursor.fetchone()
                user = member.mention
                server = member.guild
                
                embed = discord.Embed(title = 'New Member!', colour = discord.Colour(0xefe61), 
                description = str(message[0]).format(user = user, server = server) + ' `k.help` for more information about KaiserBot.')
                embed.set_author(name = member.name, icon_url = f'{member.avatar_url}')
                embed.set_footer(text = f'Member #{len(list(member.guild.members))} | KaiserBot | {member.guild.name}',
                icon_url = f'{member.guild.icon_url}')
                embed.timestamp = datetime.datetime.utcnow()

                cursor.execute(f'SELECT Autorole FROM EventsDB WHERE GUILD_ID = {member.guild.id}')
                auto = cursor.fetchone()
                autorole = discord.utils.get(member.guild.roles, name = auto[0])
                await member.add_roles(autorole)

                sendchannel = self.bot.get_channel(id = int(channelID[0]))
                await sendchannel.send(embed = embed)

    @commands.command(aliases = ['Set_channel', 'setchannel', 'Setchannel', 'set_c', 'Set_c'])
    async def set_channel(self, ctx, channel: discord.TextChannel):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('cogs/EventsDB.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT Channel_ID FROM EventsDB WHERE Guild_ID = {ctx.guild.id}')
            channelID = cursor.fetchone()
            if channelID is None:
                sql = ('INSERT INTO EventsDB(Guild_ID, Channel_ID) VALUES(?, ?)')
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'Welcome message channel set to {channel.mention}.')
            elif channelID is not None:
                sql = ('UPDATE EventsDB SET Channel_ID = ? WHERE Guild_ID = ?')
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'Welcome message channel updated to {channel.mention}.')
            cursor.execute(sql, val)
            cursor.close()
            db.commit()
            db.close()
        else:
            await ctx.send("You don't have the perms. GIT GUD.")
    
    @commands.command(aliases = ['Set_channel_ex', 'setchannel_ex', 'Setchannel_ex', 'set_c_ex', 'Set_c_ex'])
    async def set_channel_ex(self, ctx):
        await ctx.send('```k.set_channel #the-lounge\n>>> [Welcome message will display in #the-lounge]```')

    @commands.command(aliases = ['Set_welcome', 'setwelcome', 'Setwelcome', 'set_w', 'Set_w'])
    async def set_welcome(self, ctx, *, message):
        if ctx.message.author.guild_permissions.administrator:
            db = sqlite3.connect('cogs/EventsDB.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT WMessage FROM EventsDB WHERE Guild_ID = {ctx.guild.id}')
            welcome = cursor.fetchone()
            if welcome is None:
                sql = ('INSERT INTO EventsDB(Guild_ID, WMessage) VALUES(?, ?)')
                val = (ctx.guild.id, message)
                await ctx.send(f'Welcome message text set to: ```{message}```')
            elif welcome is not None:
                sql = ('UPDATE EventsDB SET WMessage = ? WHERE Guild_ID = ?')
                val = (message, ctx.guild.id)
                await ctx.send(f'Welcome message text updated to: ```{message}```')
            cursor.execute(sql, val)
            cursor.close()
            db.commit()
            db.close()
        else:
            await ctx.send("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Set_welcome_ex', 'setwelcome_ex', 'Setwelcome_ex', 'set_w_ex', 'Set_w_ex'])
    async def set_welcome_ex(self, ctx):
        await ctx.send('```{server}: mentions the server\n{user}: mentions the user\n\nk.set_welcome Please welcome {user}, the newest \
member of {server}!\n>>> [Sets welcome message as "Plase welcome {user}, the newest member of {server}!"]```')

    @commands.command(aliases = ['Set_autorole', 'setautorole', 'Setautorole', 'set_a', 'Set_a'])
    async def set_autorole(self, ctx, *, role):
        if ctx.message.author.guild_permissions.administrator:
            if role in list(map(lambda x: str(x), ctx.guild.roles)):
                db = sqlite3.connect('cogs/EventsDB.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT Autorole FROM EventsDB WHERE Guild_ID = {ctx.guild.id}')
                autorole = cursor.fetchone()
                if autorole is None:
                    sql = ('INSERT INTO EventsDB(Guild_ID, Autorole) VALUES(?, ?)')
                    val = (ctx.guild.id, role)
                    await ctx.send(f'Autorole set to `{role}`.')
                elif autorole is not None:
                    sql = ('UPDATE EventsDB SET Autorole = ? WHERE Guild_ID = ?')
                    val = (role, ctx.guild.id)
                    await ctx.send(f'Autorole updated to `{role}`.')
                cursor.execute(sql, val)
                cursor.close()
                db.commit()
                db.close()
            else:
                await ctx.send("That's not a valid role in this server, pabo. Remember, the role is __**CASE SENSITIVE**__.")
        else:
            await ctx.send("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Set_autorole_ex', 'setautorole_ex', 'Setautorole_ex', 'set_a_ex', 'Set_a_ex'])
    async def set_autorole_ex(self, ctx):
        await ctx.send('```Role name is CASE SENSITIVE.\n\n\
k.set_autorole Hydrated\n>>> [Sets Hydrated as the autorole]```')


def setup (bot):
    bot.add_cog(Events_Cog(bot))
