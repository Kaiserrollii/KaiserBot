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

    # Welcome message, autorole, and bot DM when a new user joins Kaisercord
    # Hardcoded welcome message for Joycord as well as per request
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
            embed.set_thumbnail(url = f'{member.avatar_url}')
            embed.set_author(name = f'Welcome to {member.guild.name}!', url = 'https://discord.gg/kjuX5TZ', icon_url = f'{member.avatar_url}')
            embed.set_footer(text = f'Member #{len(list(member.guild.members))} | KaiserBot | {member.guild.name}',
            icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            await channel.send(embed = embed)
            await member.add_roles(autorole)
            await member.send(f"Welcome to {member.guild.name}! I'm KaiserBot: the server's personal bot.\nFor more information about me, head to \
    https://kaiserbotwebsite--kaiserrollii.repl.co/")

        elif member.guild.id == 764260384818462731: #joycord id
            autorole = discord.utils.get(member.guild.roles, name = 'Joyful') #joycord autorole
            channel = self.bot.get_channel(id = 764263186747883531) # joycord joy-channel
            welcome_channel = self.bot.get_channel(id = 764268945758617620) #joycord welcome
            roles_channel = self.bot.get_channel(id = 764270079042781195) # joycord roles
            bot_channel = self.bot.get_channel(id = 764261923905994762) # joycord botland

            embed = discord.Embed(title = 'A new member has arrived!', colour = discord.Colour(0x00d741),
            description = f"Welcome to the Joy discord server, {member.mention}!\n\n\
Please check out {welcome_channel.mention} for rules and important information!\n\
You can add special Joy themed roles in {roles_channel.mention}!\n\
If you're here for the card game, please check out {bot_channel.mention}!")
            embed.set_thumbnail(url = f'{member.avatar_url}')
            embed.set_footer(text = f'Member #{len(list(member.guild.members))}!')
            await channel.send(embed = embed)
            await member.add_roles(autorole)

        else:
            return

    # Roles system for Kaisercord
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return
        else:
            if message.author.guild.id == 604539500223397898:
                roleschannel = self.bot.get_channel(id = 623772688711942144)
                if message.channel == roleschannel:
                    if message.content.startswith('+') or message.content.startswith('-'):
                        rolename = message.content[1:]
                        rolelist = list(map(lambda x: str(x), message.author.guild.roles))
                        index = list(reversed(rolelist)).index('🔱 Commanders 🔱') + 1
                        offlimits = list(reversed(rolelist))[:index]
                        memberroles = list(map(lambda x: str(x), message.author.roles))
                        if rolename in rolelist:
                            if rolename in offlimits or rolename == '@everyone':
                                noperms = await roleschannel.send('Nice try.')
                                await asyncio.sleep(3)
                                await message.delete()
                                await noperms.delete()
                            else:
                                role = discord.utils.get(message.author.guild.roles, name = rolename)
                                d = dict(role.permissions)
                                roleperms = list(filter(lambda key: d[key], d))
                                if 'administrator' in roleperms or 'mention_everyone' in roleperms or 'kick_members' in roleperms or\
                                'ban_members' in roleperms or 'manage_channels' in roleperms or 'manage_guild' in roleperms or\
                                'view_audit_log' in roleperms or 'priority_speaker' in roleperms or 'manage_messages' in roleperms or\
                                'mute_members' in roleperms or 'deafen_members' in roleperms or 'move_members' in roleperms or\
                                'manage_nicknames' in roleperms or 'manage_roles' in roleperms or 'manage_webhooks' in roleperms or\
                                'manage_emojis' in roleperms:
                                    if message.author.guild_permissions.ban_members == False:
                                        noperms = await roleschannel.send('Nice try.')
                                        await asyncio.sleep(3)
                                        await message.delete()
                                        await noperms.delete()
                                    else:
                                        if message.content.startswith('+'):
                                            if rolename in memberroles:
                                                existent = await roleschannel.send(f"You can't add a role you already have, pabo. Try something else.")
                                                await asyncio.sleep(3)
                                                await message.delete()
                                                await existent.delete()
                                            else:
                                                await message.author.add_roles(role)
                                                addmessage = await roleschannel.send(f'`{role}` added for {message.author}!')
                                                await asyncio.sleep(3)
                                                await message.delete()
                                                await addmessage.delete()
                                        elif message.content.startswith('-'):
                                            if rolename not in memberroles:
                                                nonexistent = await roleschannel.send(f"You can't remove a role you don't have, pabo. Try something else.")
                                                await asyncio.sleep(3)
                                                await message.delete()
                                                await nonexistent.delete()
                                            else:
                                                await message.author.remove_roles(role)
                                                removemessage = await roleschannel.send(f'`{role}` removed for {message.author}!')
                                                await asyncio.sleep(3)
                                                await message.delete()
                                                await removemessage.delete()
                                else:
                                    if message.content.startswith('+'):
                                        if rolename in memberroles:
                                            existent = await roleschannel.send(f"You can't add a role you already have, pabo. Try something else.")
                                            await asyncio.sleep(3)
                                            await message.delete()
                                            await existent.delete()
                                        else:
                                            await message.author.add_roles(role)
                                            addmessage = await roleschannel.send(f'`{role}` added for {message.author}!')
                                            await asyncio.sleep(3)
                                            await message.delete()
                                            await addmessage.delete()
                                    elif message.content.startswith('-'):
                                        if rolename not in memberroles:
                                            nonexistent = await roleschannel.send(f"You can't remove a role you don't have, pabo. Try something else.")
                                            await asyncio.sleep(3)
                                            await message.delete()
                                            await nonexistent.delete()
                                        else:
                                            await message.author.remove_roles(role)
                                            removemessage = await roleschannel.send(f'`{role}` removed for {message.author}!')
                                            await asyncio.sleep(3)
                                            await message.delete()
                                            await removemessage.delete()
                        else:
                            validmessage = await roleschannel.send(f'`{rolename}` is not a valid role, pabo. Try again, and remember that \
role names are **CASE SENSITIVE**.')
                            await asyncio.sleep(5)
                            await message.delete()
                            await validmessage.delete()
                    else:
                        await message.delete()
                else:
                    return
            else:
                return


def setup (bot):
    bot.add_cog(Events_Cog(bot))
