import discord
import asyncio
import datetime
from discord.ext import commands


# Helper function for formatting dictionary -> string
def dict_format(d):
    L = []
    for i in d:
        L.append(i)
        L.append(d[i])
        L.append('\n')
    return ''.join(L)

# Converter class for converting strings to member/channel objects
class Find_Object(commands.Converter):

    async def member_convert(self, ctx, argument):
        converter = commands.MemberConverter()
        member = await converter.convert(ctx, argument)
        return member
    
    async def channel_convert(self, ctx, argument):
        converter = commands.TextChannelConverter()
        channel = await converter.convert(ctx, argument)
        return channel

# Main class for poll functionality
class Poll_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Poll: Online')

    @commands.command(aliases = ['Poll', 'pollii', 'Pollii'])
    async def poll(self, ctx):
        if not ctx.message.author.guild_permissions.ban_members:
            await ctx.send("You don't have the perms. GIT GUD.")
            return

        # Basic wait_for message check
        def check(answer: discord.Message): 
            return answer.channel == ctx.channel and answer.author.id == ctx.author.id

        # Poll setup embed
        base_description = {'Channel: ': '', 'Member: ': '', 'Question: ': ''}
        setup_embed = discord.Embed(title = 'Poll Setup', colour = discord.Colour(0xefe61))
        setup_embed.description = dict_format(base_description)
        setup_embed.set_thumbnail(url = 'https://imgur.com/1u0GZ83.png')
        setup_embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        setup_embed.timestamp = datetime.datetime.utcnow()
        setup_message = await ctx.send(embed = setup_embed)

        # Identify channel for the poll to be sent in
        channel_message = await ctx.send('**Enter the channel to start the poll in:**')
        try:
            channel_wait = await self.bot.wait_for('message', timeout = 60, check = check)
            channel = channel_wait.content
            await channel_wait.delete()
            base_description['Channel: '] = channel
            description = dict_format(base_description)
            setup_embed.description = description
            await setup_message.edit(embed = setup_embed)
            await channel_message.delete()
        except asyncio.TimeoutError:
            await setup_message.delete()
            await channel_message.delete()
            await ctx.send('Timed out.')
            return

        # Identify member asking the poll question
        member_message = await ctx.send('**Enter the member asking the poll question:**')
        try:
            member_wait = await self.bot.wait_for('message', timeout = 60, check = check)
            member = member_wait.content
            await member_wait.delete()
            base_description['Member: '] = member
            description = dict_format(base_description)
            setup_embed.description = description
            await setup_message.edit(embed = setup_embed)
            await member_message.delete()
        except asyncio.TimeoutError:
            await setup_message.delete()
            await member_message.delete()
            await ctx.send('Timed out.')
            return

        # Identify poll question
        question_message = await ctx.send('**Enter the question:**')
        try:
            question_wait = await self.bot.wait_for('message', timeout = 60, check = check)
            question = question_wait.content
            await question_wait.delete()
            base_description['Question: '] = question
            description = dict_format(base_description)
            setup_embed.description = description
            await setup_message.edit(embed = setup_embed)
            await question_message.delete()
        except asyncio.TimeoutError:
            await setup_message.delete()
            await question_message.delete()
            await ctx.send('Timed out.')
            return

        # Ask if user wants to add a thumbnail to the poll
        thumbnail_message = await ctx.send('**Poll image url (optional - "None" for no image):**')
        try:
            thumbnail_wait = await self.bot.wait_for('message', timeout = 60, check = check)
            thumbnail = thumbnail_wait.content
            await thumbnail_wait.delete()
            if thumbnail.lower() == 'none':
                pass
            else:
                setup_embed.set_thumbnail(url = thumbnail)
                await setup_message.edit(embed = setup_embed)
            await thumbnail_message.delete()
        except asyncio.TimeoutError:
            await setup_message.delete()
            await thumbnail_message.delete()
            await ctx.send('Timed out.')
            return

        # Identify amount of options for the poll (<=10)
        amount_message = await ctx.send('**How many options will your poll have:**')
        try:
            amount_wait = await self.bot.wait_for('message', timeout = 60, check = check)
            amount = int(amount_wait.content)

            if amount > 10:
                await ctx.send('Your poll has too many options! Please keep it at 10 or under.')
                await setup_message.delete()
                await amount_message.delete()
                await amount_wait.delete()
                return

            await amount_wait.delete()
            await amount_message.delete()
        except asyncio.TimeoutError:
            await setup_message.delete()
            await amount_message.delete()
            await ctx.send('Timed out.')
            return

        # Gather emote/text pairs for each option
        counter = 0
        options = {}
        while counter < amount:
            counter += 1

            # Get emote for option (must be either default or in one of the bot's guilds)
            emote_message = await ctx.send(f'**Enter the emote for Option {counter}:**')
            try:
                emote_wait = await self.bot.wait_for('message', timeout = 60, check = check)
                emote = emote_wait.content
                await emote_wait.delete()
                await emote_message.delete()
            except asyncio.TimeoutError:
                await setup_message.delete()
                await emote_message.delete()
                await ctx.send('Timed out.')
                return
            
            # Get text for option
            text_message = await ctx.send(f'**Enter the text for Option {counter}:**')
            try:
                text_wait = await self.bot.wait_for('message', timeout = 60, check = check)
                text = text_wait.content
                await text_wait.delete()
                await text_message.delete()
            except asyncio.TimeoutError:
                await setup_message.delete()
                await text_message.delete()
                await ctx.send('Timed out.')
                return

            options[emote] = text
            setup_embed.add_field(name = '\u200b', value = emote + ' ' + text, inline = False)
            await setup_message.edit(embed = setup_embed)

        # Ask user if ready to deploy poll
        ready_message = await ctx.send('Poll setup complete! Deploy?')
        await ready_message.add_reaction('✅')
        await ready_message.add_reaction('❌')

        # Basic wait_for reaction check
        def reaction_check(reaction, user):
            return ((user == ctx.author) and \
                    (str(reaction.emoji) == '✅' or str(reaction.emoji) == '❌') and \
                    (reaction.message.id == ready_message.id))

        # Wait for user reaction
        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 60, check = reaction_check)
        except asyncio.TimeoutError:
            await setup_message.delete()
            await ready_message.delete()
            await ctx.send('Timed out.')
            return
        else:
            # If ready to deploy, send poll embed in given channel
            if str(reaction.emoji) == '✅':
                await ready_message.delete()
                
                # Convert member string to member object
                member = await Find_Object.member_convert(self, ctx, member)

                poll_embed = discord.Embed(title = f"{member.name}'s Question of the Day")
                poll_embed.colour = member.colour
                poll_embed.description = question

                # Set thumbnail if given
                if thumbnail.lower() != 'none':
                    poll_embed.set_thumbnail(url = thumbnail)

                # Add each option pair into a field value
                value = ''
                for i in options.items():
                    value += i[0] + ' ' + i[1] + '\n'

                poll_embed.add_field(name = '\u200b', value = value, inline = False)
                poll_embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                poll_embed.timestamp = datetime.datetime.utcnow()

                # convert channel string to channel object
                channel = await Find_Object.channel_convert(self, ctx, channel)
                poll_message = await channel.send(embed = poll_embed)

                # Add emote reactions to poll embed
                for i in list(options.keys()):
                    await poll_message.add_reaction(i)

                await ctx.send('Deployed!')

            # Otherwise, cancel
            elif str(reaction.emoji) == '❌':
                await ctx.send('Poll cancelled.')
                await asyncio.sleep(10)
                await setup_message.delete()
                await ready_message.delete()
                return

    @commands.command(aliases = ['Poll_ex', 'pollii_ex', 'Pollii_ex'])
    async def poll_ex(self, ctx):
        await ctx.send(f'```k.poll\n>>> [Starts a new poll setup]```')

    
def setup(bot):
    bot.add_cog(Poll_Cog(bot))
