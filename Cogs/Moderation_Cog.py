import discord  
import asyncio
import datetime
from discord.ext import commands 


class Moderation_Cog (commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready (self):
        print('Moderation: Online')

    # Consumes a nat, number
    # Deletes [number] amount of messages in the current channel
    @commands.command(aliases = ['Cleanse', 'purge', 'Purge', 'clean', 'Clean'])
    async def cleanse(self, ctx, number):
        if ctx.message.author.guild_permissions.manage_messages:
            number = int(round(float(number)))
            if number < 0:
                await ctx.send('Enter a positive integer, pabo.')
            elif number == 0:
                await ctx.send('Delete 0 messages? :ok_hand: boomer.')
            elif number > 100:
                await ctx.send("Enter a positive integer less than or equal to 100, pabo. Don't make me ask you again.")
            else:
                deleted = await ctx.message.channel.purge(limit = (number + 1))
                message = await ctx.send(f':wastebasket: {len(deleted) - 1} messages deleted by {ctx.message.author.name}.')
                await asyncio.sleep(7)
                await message.delete()
        else:
            await ctx.send("You don't have the perms. GIT GUD.") 

    @commands.command(aliases = ['Cleanse_ex', 'purge_ex', 'Purge_ex', 'clean_ex', 'Clean_ex'])
    async def cleanse_ex(self, ctx):
        await ctx.send('```k.cleanse 10\n>>> [Deletes 10 messages]```')

    # Consumes a nat, duration, and anyof('sec', 'min', 'h'), unit
    # Sets the slowmode in the current channel to the specified duration in the specified unit 
    @commands.command(aliases = ['Slowmode', 'slow', 'Slow', 'sm', 'SM'])
    async def slowmode(self, ctx, duration, unit = None):
        channel = ctx.message.channel
        if ctx.message.author.guild_permissions.manage_messages:
            if unit == None:
                if duration.lower() == 'off' or duration.lower() == 'stop':
                    await channel.edit(slowmode_delay = 0)
                    await ctx.send(f'Slowmode turned off in {channel.mention}.')
                else:
                    await ctx.send('You need to specify a unit, pabo. Choose between `seconds` / `sec`, `minutes` / `min`, or `hours` / `h`.')
            elif int(duration) <= 0:
                await ctx.send('Slowmode duration should be a positive integer, pabo. Try again.')
            elif unit.lower() == 'sec' or unit.lower() == 'seconds' or unit.lower() == 'second':
                if int(duration) > 21600:
                    await ctx.send('21600 seconds is the maximum slowmode duration (in seconds), pabo. Try something smaller.')
                else:
                    await channel.edit(slowmode_delay = duration)
                    await ctx.send(f'Slowmode set to **{duration} second(s)** in {channel.mention}.')
            elif unit.lower() == 'min' or unit.lower() == 'minutes' or unit.lower() == 'minute':
                if int(duration) > 360:
                    await ctx.send('360 minutes is the maximum slowmode duration (in minutes), pabo. Try something smaller.')
                else:
                    await channel.edit(slowmode_delay = (int(duration) * 60))
                    await ctx.send(f'Slowmode set to **{duration} minute(s)** in {channel.mention}.')
            elif unit.lower() == 'h' or unit.lower() == 'hours' or unit.lower() == 'hour':
                if int(duration) > 6:
                    await ctx.send('6 hours is the maximum slowmode duration (in hours), pabo. Try something smaller.')
                else:
                    await channel.edit(slowmode_delay = (int(duration) * 3600))
                    await ctx.send(f'Slowmode set to **{duration} hour(s)** in {channel.mention}.')
            else:
                await ctx.send('Units should be `seconds` / `sec`, `minutes` / `min`, or `hours` / `h`, pabo. Try again.')
        else:
            await ctx.send ("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Slowmode_ex', 'slow_ex', 'Slow_ex', 'sm_ex', 'SM_ex'])
    async def slowmode_ex(self, ctx):
        await ctx.send('```k.slowmode 30 sec\n>>> [Sets slowmode to 30 seconds]\n\nk.slowmode off\n>>> [Turns slowmode off]```')

    # Consumes a parameter, member, which must be a valid user
    # Mutes the specified member
    @commands.command (aliases = ['Mute', 'shh', 'Shh'])
    async def mute(self, ctx, member : discord.Member = None):
        muted_role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if ctx.message.author.guild_permissions.ban_members:
            if not member:
                await ctx.send('Specify a user to mute, pabo.')
            else:
                if muted_role in member.roles:
                    await ctx.send('This user is already muted. Try someone else, pabo.')
                else:
                    await member.add_roles(muted_role)
                    await ctx.send(f':mute: {member} has been muted in the server.')
        else:
            await ctx.send ("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Mute_ex', 'shh_ex', 'Shh_ex'])
    async def mute_ex(self, ctx):
        await ctx.send('```k.mute @Kaiserrollii\n>>> [Mutes Kaiserrollii]\n\nk.mute 496181635952148483\n>>> [Mutes 496181635952148483]```')

    # Consumes a parameter, member, which must be a valid user
    # Unmutes the specified member
    @commands.command (aliases = ['Unmute', 'reverseshh', 'Reverseshh', 'reverse_shh', 'Reverse_shh'])
    async def unmute(self, ctx, member : discord.Member = None):
        muted_role = discord.utils.get(ctx.guild.roles, name = 'Muted')
        if ctx.message.author.guild_permissions.ban_members:
            if not member:
                await ctx.send('Specify a user to unmute, pabo.')
            else:
                if muted_role not in member.roles:
                    await ctx.send('This user is already unmuted. Try someone else, pabo.')
                else:
                    await member.remove_roles(muted_role)
                    await ctx.send(f':speaker: {member} has been unmuted in the server.')
        else:
            await ctx.send ("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Unmute_ex', 'reverseshh_ex', 'Reverseshh_ex', 'reverse_shh_ex', 'Reverse_shh_ex'])
    async def unmute_ex(self, ctx):
        await ctx.send('```k.unmute @Kaiserrollii\n>>> [Unmutes Kaiserrollii]\n\nk.unmute 496181635952148483\n>>> [Unmutes 496181635952148483]```')

    # Consumes a parameter, member, which must be a valid user
    # Returns a kick confirmation embed which times out after 60 seconds
    @commands.command(aliases = ['Kick', 'sadbye', 'Sadbye'])
    async def kick(self, ctx, member : discord.Member, *, reason = None):
        await ctx.send('Fixing some issues with the ban and kick commands. Disabled for the time being. Sorry!')
    #     embed = discord.Embed()
    #     if ctx.message.author.guild_permissions.ban_members:
    #         if member.guild_permissions.ban_members:
    #             await ctx.send("Nice try. You can't kick fellow moderators, pabo.")
    #         else:
    #             embed.colour = 0xefe61
    #             embed.set_thumbnail(url = 
    #             'https://cdn.discordapp.com/attachments/665437935088304132/702985712877961266/681305365446787323.png')
    #             embed.set_author(name = 'Kick Confirmation', icon_url = f'{member.avatar_url}')
    #             embed.title = f'Please confirm kick for {member}.'
    #             embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
    #             icon_url = 'https://i.imgur.com/CuNlLOP.png')
    #             embed.timestamp = datetime.datetime.utcnow()
    #             message = await ctx.send(embed = embed)
    #             await message.add_reaction('✅')
    #             await message.add_reaction('❌')
    #             try: 
    #                 reaction, user = await self.bot.wait_for('reaction_add', timeout = 60, check = lambda reaction, 
    #                 user: str(reaction.emoji) == '✅' and user == ctx.author or str(reaction.emoji) == '❌' and user == ctx.author)
    #             except asyncio.TimeoutError:
    #                 await message.clear_reactions()
    #                 embed.set_author(name = 'Kick Confirmation', icon_url = f'{member.avatar_url}')
    #                 embed.title = f'Attempt to kick {member} has timed out. Slowpoke.'
    #                 embed.set_thumbnail(url = 
    #                 'https://cdn.discordapp.com/attachments/665437935088304132/702991071382339755/494529930864885760.png')
    #                 await message.edit(embed = embed)
    #             else:
    #                 if str(reaction.emoji) == '✅':
    #                     await message.clear_reactions()
    #                     embed.title = f'{member} has been kicked. :wave:'
    #                     embed.description = f'Reason: {reason}'
    #                     await message.edit(embed = embed)
    #                     await member.kick(reason = reason)
    #                 elif str(reaction.emoji) == '❌':
    #                     await message.clear_reactions()
    #                     embed.set_author(name = 'Kick Confirmation', icon_url = f'{member.avatar_url}')
    #                     embed.title = 'Kick cancelled.'
    #                     embed.description = 'Maybe next time.'
    #                     await message.edit(embed = embed)
    #                 else:
    #                     await ctx.send('You need to react with either ✅ or ❌, pabo.')
    #     else:
    #         await ctx.send("You don't have the perms. GIT GUD.")

    # @commands.command(aliases = ['Kick_ex', 'sadbye_ex', 'Sadbye_ex'])
    # async def kick_ex(self, ctx):
    #     await ctx.send('```k.kick @Kaiserrollii\n>>> [Kick confirmation menu]\n\nk.kick 496181635952148483\n>>> [Kick confirmation menu]```')

    # Consumes a parameter, member, which must be a valid user
    # Returns a ban confirmation embed which times out after 60 seconds
    @commands.command(aliases = ['Ban', 'CRIMINAL', 'criminal', 'Criminal'])
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await ctx.send('Fixing some issues with the ban and kick commands. Disabled for the time being. Sorry!')
    #     embed = discord.Embed()
    #     if ctx.message.author.guild_permissions.ban_members:
    #         if member.guild_permissions.ban_members:
    #             await ctx.send("Nice try. You can't ban fellow moderators, pabo.")
    #         else:
    #             embed.colour = 0xefe61
    #             embed.set_thumbnail(url = 
    #             'https://cdn.discordapp.com/attachments/665437935088304132/702985712877961266/681305365446787323.png')
    #             embed.set_author(name = '⇽  C R I M I N A L', icon_url = f'{member.avatar_url}')
    #             embed.title = f'Please confirm ban for {member}.'
    #             embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
    #             icon_url = 'https://i.imgur.com/CuNlLOP.png')
    #             embed.timestamp = datetime.datetime.utcnow()
    #             message = await ctx.send(embed = embed)
    #             await message.add_reaction('✅')
    #             await message.add_reaction('❌')
    #             try: 
    #                 reaction, user = await self.bot.wait_for('reaction_add', timeout = 60, check = lambda reaction, 
    #                 user: str(reaction.emoji) == '✅' and user == ctx.author or str(reaction.emoji) == '❌' and user == ctx.author)
    #             except asyncio.TimeoutError:
    #                 await message.clear_reactions()
    #                 embed.set_author(name = '⇽  Still  a  C R I M I N A L', icon_url = f'{member.avatar_url}')
    #                 embed.title = f'Attempt to ban {member} has timed out. Slowpoke.'
    #                 embed.set_thumbnail(url = 
    #                 'https://cdn.discordapp.com/attachments/665437935088304132/702991071382339755/494529930864885760.png')
    #                 await message.edit(embed = embed)
    #             else:
    #                 if str(reaction.emoji) == '✅':
    #                     await message.clear_reactions()
    #                     embed.title = f'{member} has been banned. :wave:'
    #                     embed.description = f'Reason: {reason}'
    #                     await message.edit(embed = embed)
    #                     await member.ban(reason = reason)
    #                 elif str(reaction.emoji) == '❌':
    #                     await message.clear_reactions()
    #                     embed.set_author(name = '⇽  Still  a  C R I M I N A L', icon_url = f'{member.avatar_url}')
    #                     embed.title = 'Ban cancelled.'
    #                     embed.description = 'Maybe next time.'
    #                     await message.edit(embed = embed)
    #                 else:
    #                     await ctx.send('You need to react with either ✅ or ❌, pabo.')
    #     else:
    #         await ctx.send("You don't have the perms. GIT GUD.")

    # @commands.command(aliases = ['Ban_ex', 'CRIMINAL_ex', 'criminal_ex', 'Criminal_ex'])
    # async def ban_ex(self, ctx):
    #     await ctx.send('```k.ban @Kaiserrollii\n>>> [Ban confirmation menu]\n\nk.ban 496181635952148483\n>>> [Ban confirmation menu]```')

    # Consumes a parameter, member, which consists of username + tag
    # Unbans the specified member
    @commands.command (aliases = ['reverseCRIMINAL', 'ReverseCRIMINAL', 'reversecriminal'])
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        if ctx.message.author.guild_permissions.administrator:
            for ban_entry in banned_users:
                user = ban_entry.user
                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f':white_check_mark: {member} has been unbanned from the server.')
        else:
            await ctx.send ("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['reverseCRIMINAL_ex', 'ReverseCRIMINAL_ex', 'reversecriminal_ex'])
    async def unban_ex(self, ctx):
        await ctx.send('```k.unban Kaiserrollii#6698\n>>> [Unbans Kaiserrollii#6698]```')

    # Consumes channel, which must be a valid channel, and a str, message
    # Sends the specified message in the specified channel
    @commands.command(aliases = ['Say', 'send', 'Send'])
    async def say(self, ctx, channel: discord.TextChannel, *, message):
        if ctx.message.author.guild_permissions.administrator:
            await channel.send(message)
        else:
            await ctx.send("You don't have the perms. GIT GUD.")

    @commands.command(aliases = ['Say_ex', 'send_ex', 'Send_ex'])
    async def say_ex(self, ctx):
        await ctx.send('```k.say #the-lounge stfu\n>>> [Sends "stfu" in #the-lounge]```')


def setup (bot):
    bot.add_cog(Moderation_Cog(bot))
