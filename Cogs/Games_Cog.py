import discord
import random 
import datetime 
import asyncio
import requests
import json
import sympy
from sympy import *
from sympy.parsing.sympy_parser import parse_expr
import pandas as pd
import html
import sqlite3 as sql
from discord.ext import commands 


class Games_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Games: Online')

    # Returns something cringey from the randomized list
    # Suggest new responses in #suggestions or via DM
    @commands.command(aliases = ['Cringe', 'yikes', 'Yikes'])
    async def cringe(self, ctx):

        cringe_list = ['soYeON uwU',
                       '"Maybe if you stanned Loona..."',
                       'Twitter',
                       'Weebs',
                       'Akgaes',
                       'Sliding into the Facebook Messenger DMs.',
                       'https://www.youtube.com/watch?v=9eWsyXlR0Qk',
                       'https://cdn.discordapp.com/attachments/623770537340174336/690651875086827610/ee9c152.jpg',
                       'https://cdn.discordapp.com/attachments/623770537340174336/690652718095794246/e26440f.jpg',
                       'https://cdn.discordapp.com/attachments/623770537340174336/690653580855738408/SoyeonDesktop.jpg',
                       'https://cdn.discordapp.com/attachments/630633322686578689/691470739244580954/unknown.png',
                       'https://media.discordapp.net/attachments/629892587603492883/691675221219868712/unknown.png',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448157697343538/image0.jpg',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448158934925363/image1.jpg',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448159253430342/image2.jpg',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448159505088562/image3.jpg',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448159970918416/image4.jpg',
                       'https://cdn.discordapp.com/attachments/665437935088304132/695448160264257566/image5.jpg',
                       'https://media.discordapp.net/attachments/629892587603492883/691776592355262504/unknown.png',
                       'https://cdn.discordapp.com/attachments/623770537340174336/697975848090730556/9c54e90.png',
                       'https://twitter.com/baelkie/status/1173066011265949696',
                       'https://cdn.discordapp.com/attachments/623770537340174336/707742026728341594/IMG_1648.JPG',
                       'https://cdn.discordapp.com/attachments/623770537340174336/707870719714918421/unknown.png',
                       'https://cdn.discordapp.com/attachments/630633322686578689/708470605556613140/afzxwn0il7221.png',
                       'https://cdn.discordapp.com/attachments/630633322686578689/717638617928957972/unknown.png',
                       'https://cdn.discordapp.com/attachments/630633322686578689/717638790335823892/unknown.png',
                       'https://imgur.com/rxfQ3XQ.png']
                    
        await ctx.send(f'{random.choice(cringe_list)}')

    # Consumes a parameter of any type, question
    # Returns advice from the randomized list
    # Suggest new responses in #suggestions or via DM
    @commands.command(aliases = ['Advice', 'question', 'Question'])
    async def advice(self, ctx, *, question):

        answer_list = ['JUST DO IT.',
                    "That's your problem, not mine.", 
                    'Ask your mom.',
                    'Ask someone else.',
                    "I don't know, bruh.", 
                    'No comment.',
                    'The solution is to unplug grandma.',
                    'The solution is to `_bestgif`.',
                    'The answer is obvious, pabo.',
                    'Why are you asking me this? Go stan Irene instead.',
                    'That is a dumb question.',
                    '_whoasked',
                    'Find someone to simp on.',
                    'Ask Dr. Phil',
                    'Ask Gabba']

        await ctx.send (f''':question:**Question:** {question}\n'''
                        f''':pencil:**Good Advice:** {random.choice (answer_list)}''')

    @commands.command(aliases = ['Advice_ex', 'question_ex', 'Question_ex'])
    async def advice_ex(self, ctx):
        await ctx.send('```k.advice Should I stan Loona?\n>>> Why are you asking me this? Go stan Irene instead.```')

    # Consumes a nat, amount
    # Returns a randomized number between 0 and amount
    @commands.command(aliases = ['Dice', 'roll', 'Roll'])
    async def dice(self, ctx, amount):
        if amount.isnumeric() == False or int(amount) == 0:
            await ctx.send('Input a *positive integer*, pabo.')
        if int(amount) > 100:
            await ctx.send(f'You have rolled a :game_die: **{random.randint(1, int(amount))}** :game_die: !!!')
            await ctx.send('What kind of die has that many sides, though? Pretty sus :eyes:.')
        else:
            await ctx.send(f'You have rolled a :game_die: **{random.randint(1, int(amount))}** :game_die: !!!')  

    @commands.command(aliases = ['Dice_ex', 'roll_ex', 'Roll_ex'])
    async def dice_ex(self, ctx):
        await ctx.send('```k.dice 12\n>>> 8```')

    # Consumes multiple parameters of any type, choices
    # Returns a randomized choice from choices
    @commands.command(aliases = ['Choose', 'choice', 'Choice'])
    async def choose(self, ctx, *choices: str):
        for i in choices:
            if i.lower() == 'irene' or i.lower() == 'lrene':
                await ctx.send('Irene.')
                return
        await ctx.send(random.choice(choices))

    @commands.command(aliases = ['Choose_ex', 'choice_ex', 'Choice_ex'])
    async def choose_ex(self, ctx):
        await ctx.send('```k.choose Irene anyone_else\n>>> Irene```')

    # Consumes two parameters of any type, one and two
    # Returns either of the embeds, depending on the randomized compatibility 
    # Suggest new responses in #suggestions or via DM
    @commands.command(aliases = ['Ship', 'compatibility', 'Compatibility'])
    async def ship(self, ctx, one, two):
        compatibility = random.randint(0, 100)

        responses1 = ['Do **not** attempt to DM slide. Instead, consider staying forever alone.',
                      'Wallow in despair by consuming an entire package of Oreos. It will make you feel better.',
                      'Distract yourself by watching Red Velvet compilations on YouTube.',
                      'Remind yourself that it is okay to be single. Bros before hoes, no?',
                      'Instead of doing something silly, such as crying, watch [this](https://youtu.be/JCTYs2UaUBE) instead.',
                      "Don't worry. Assuming you're not a boomer, you still have plenty of time to find someone.\
                      If you are a boomer, though, F.",
                      'Whatever you do, do not go to Facebook Messenger and attempt to slide into the DMs. It will not work, guaranteed.',
                      "Starving children in Africa could've eaten that ship. Be a little more considerate next time, smh.",
                      'NERD.',
                      "It's a lost cause. I'm sorry.",
                      'Wait an adequate amount of time before attempting to crawl out of the friendzone. Keyword: "attempt".',
                      "Idk man, I'm not even a real doctor."]

        responses2 = ['Slide into the DMs **NOW**. After that, begin arranging the wedding.',
                      ':somi::somi::somi::somi::somi::somi::somi::somi::somi::somi::somi:',
                      ':somiiupsidedown::somiiupsidedown::somiiupsidedown::somiiupsidedown:',
                      'hehe',
                      "Now begins the important process of DM sliding. Remember: one wrong move, and you're FRIENDZONED.",
                      "Idk, man. I'm not even a real doctor.",
                      'Excellent work. Report back to HQ immediately for your next task.',
                      "Congratulations! If all goes well, you'll be spending lots of money on Valentine's Day.",
                      'Damn. Respect.',
                      "I didn't think you'd make it this far."]
        
        embed1 = discord.Embed\
        (title = "⭐ **Dr. Phil's Expert Love Advice** ⭐", colour = discord.Colour(0xefe61), 
        description = f'''*Disclaimer: Dr. Phil is not a real doctor.*\n
        𝐂𝐎𝐌𝐏𝐀𝐓𝐈𝐁𝐈𝐋𝐈𝐓𝐘:\n'''
        f'Uh oh. 💔 **{one}** and **{two}** are only {compatibility}% compatible.\n\n'
        '𝐍𝐄𝐗𝐓 𝐒𝐓𝐄𝐏𝐒:\n'
        f'{random.choice(responses1)}')
        embed1.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/665437935088304132/703702638184628325/unknown.png')
        embed1.set_footer(text = f'KaiserBot | {ctx.guild.name}',
        icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed1.timestamp = datetime.datetime.utcnow()

        embed2 = discord.Embed\
        (title = "⭐ **Dr. Phil's Expert Love Advice** ⭐", colour = discord.Colour(0xefe61), 
        description = f'''*Disclaimer: Dr. Phil is not a real doctor.*\n
        𝐂𝐎𝐌𝐏𝐀𝐓𝐈𝐁𝐈𝐋𝐈𝐓𝐘:\n'''
        f'🥳 Looks like **{one}** and **{two}** are {compatibility}% compatible! 💞\n\n'
        '𝐍𝐄𝐗𝐓 𝐒𝐓𝐄𝐏𝐒:\n'
        f'{random.choice(responses2)}')
        embed2.set_thumbnail(url = 'https://cdn.discordapp.com/attachments/665437935088304132/703702638184628325/unknown.png')
        embed2.set_footer(text = f'KaiserBot | {ctx.guild.name}',
        icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed2.timestamp = datetime.datetime.utcnow()

        if compatibility < 60:
            await ctx.send (embed = embed1)
        else:
            await ctx.send(embed = embed2)

    @commands.command(aliases = ['Ship_ex', 'compatibility_ex', 'Compatibility_ex'])
    async def ship_ex(self, ctx):
        await ctx.send('```k.ship Kaiserrollii Simps\n>>> Uh oh. 💔 Kaiserrollii and Simps are only 69% compatible.```')

    # Consumes a str, message
    # Returns the spongebobified version of the message
    @commands.command(aliases = ['Spongebobify', 'copypasta', 'Copypasta'])
    async def spongebobify(self, ctx, *, message = None):
        if message is None:
            recent = await ctx.channel.history(limit = 25).flatten()
            counter = 0
            for i in recent[1:]:
                counter += 1
                if i.attachments == [] and i.embeds == []:
                    message = i.content
                    if len(message) > 2000:
                        await ctx.send('Message is too long!')
                        return
                    break
            if counter == 0:
                await ctx.send('Could not find any text messages to spongebobify.')
                return
        L = []
        for i in message:
            if random.choice([True, False]):
                i = i.upper()
                L.append(i)
            else:
                i = i.lower()
                L.append(i)
        await ctx.send(''.join(L))

    @commands.command(aliases = ['Spongebobify_ex', 'copypasta_ex', 'Copypasta_ex'])
    async def spongebobify_ex(self, ctx):
        await ctx.send('```k.spongebobify I begged Angel, any place but England. And 1 year later we were in Manchester, a shithole\n\n\
>>> I BEGgED ANgel, any PLACe But EnGlANd. AnD 1 yEAR lAter WE weRE in MaNcHESter, A shITHolE```')

    # Consumes a str, message
    # Returns the scuffed spongebobified version of the message
    @commands.command(aliases = ['Spongebobify2', 'scuffed', 'Scuffed'])
    async def spongebobify2(self, ctx, *, message = None):
        if message is None:
            recent = await ctx.channel.history(limit = 25).flatten()
            counter = 0
            for i in recent[1:]:
                counter += 1
                if i.attachments == [] and i.embeds == []:
                    message = i.content
                    if len(message) > 2000:
                        await ctx.send('Message is too long!')
                        return
                    break
            if counter == 0:
                await ctx.send('Could not find any text messages to scuff.')
                return
        L = []
        for i in message:
            if random.choice([True, False]):
                i = i.upper()
                L.append(i)
            L.append(i)
        await ctx.send(''.join(L))

    @commands.command(aliases = ['Spongebobify2_ex', 'scuffed_ex', 'Scuffed_ex'])
    async def spongebobify2_ex(self, ctx):
        await ctx.send('```k.scuffed sai more like cry\n>>> sAAII MMorEE liKKEE cRRYY```')

    # Consumes a str, message, and returns an uwufied version of the specified message
    # if message is not given, will uwufy the latest text message in the current channel
    @commands.command(aliases = ['Uwufy', 'uwufier', 'Uwufier', 'uwu', 'Uwu'])
    async def uwufy(self, ctx, *, message = None):
        if message is None:
            recent = await ctx.channel.history(limit = 25).flatten()
            counter = 0
            for i in recent[1:]:
                counter += 1
                if i.attachments == [] and i.embeds == []:
                    message = i.content
                    if len(message) > 2000:
                        await ctx.send('Message is too long!')
                        return
                    break
            if counter == 0:
                await ctx.send('Could not find any text messages to uwufy.')
                return
        wd = message.replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W')
        punctuation = wd.replace('!', '!!! owo').replace('?', '?!??!?')
        emojis = punctuation.replace('❤️', '<3').replace('♥️', '<3').replace('💕', '<3 <3').replace('😊', '>w<')
        uwu = emojis.replace('no', 'nyo').replace('No', 'Nyo')
        if len(uwu) > 2000:
            await ctx.send('Message is too long!')
        else:
            await ctx.send(uwu)

    @commands.command(aliases = ['Uwufy_ex', 'uwufier_ex', 'Uwufier_ex', 'uwu_ex', 'Uwu_ex'])
    async def uwufy_ex(self, ctx):
        await ctx.send("```k.uwufy gn everyone ❤️ remember to stay hydrated & please make sure youre washing your hands & staying clean of germs\
 ~ 💕 Take care, we're half way through the week! Stay in there but remember I'm always here if you want someone to talk to about anything \
:PepeLove: 😊 Take care and gave a great day/night! ♥️\n\n\
>>> gn evewyone <3 wemembew to stay hydwated & pwease make suwe youwuwe washing youwuw hands & staying cwean of gewms ~ <3 <3 Take cawe, we'we \
hawf way thwough the week!!!!! owo Stay in thewe but wemembew I'm awways hewe if youwu want someone to tawk to about anything :PepeWove: >w<\
Take cawe and gave a gweat day/night!!!!! owo <3\n\n\
k.uwufy \n>>> [Uwufies the most recent text message in the current channel]```")

    # Consumes a str, message
    # Returns a scrambled version of the specified message with a 15% chance of a word getting dropped
    @commands.command(aliases = ['Cloutify', 'scramble', 'Scramble', 'jumble', 'Jumble'])
    async def cloutify(self, ctx, *, message = None):
        if message is None:
            recent = await ctx.channel.history(limit = 25).flatten()
            counter = 0
            for i in recent[1:]:
                counter += 1
                if i.attachments == [] and i.embeds == []:
                    message = i.content
                    if len(message) > 2000:
                        await ctx.send('Message is too long!')
                        return
                    break
            if counter == 0:
                await ctx.send('Could not find any text messages to cloutify.')
                return
        lst = message.strip().split(' ')
        lst = list(filter(lambda x: (random.randint(1, 100) >= 15), lst))
        random.shuffle(lst)
        await ctx.send(' '.join(lst))

    @commands.command(aliases = ['Cloutify_ex', 'scramble_ex', 'Scramble_ex', 'jumble_ex', 'Jumble_ex'])
    async def cloutify_ex(self, ctx):
        await ctx.send('```k.cloutifier Oasis do you have Korean fried chicken where you at\n>>> Oasis does where you at Korean fried Chicken```')

    # Consumes question, which can be any type
    # Returns a magic 8ball answer
    @commands.command(aliases = ['Magic8Ball', 'magic', 'Magic'])
    async def magic8ball(self, ctx, *, question):

        answer_list = ['It is certain.',
                       'Without a doubt.',
                       'You may rely on it.',
                       'Yes definitely.',
                       'It is decidedly so.',
                       'As the great bearer of wisdow, the almightly seeker of truth, *yes*.',
                       'Most likely.',
                       'YES.',
                       'Outlook good.',
                       'Signs point to yes.',
                       "I'm busy right now. Ask me later.",
                       "I would tell you now, but I don't think you can handle it.",
                       'Ask again later.',
                       'Cannot predict now.',
                       'Concentrate and ask again.',
                       "Don’t count on it.",
                       'Outlook not so good.',
                       'My sources say no.',
                       'Very doubtful.',
                       'My reply is no.']

        await ctx.send (f''':question:**Question:** {question}\n'''
                        f''':pencil:**Answer:** {random.choice (answer_list)}''')

    # consumes category, which must be either female, male, or mixed
    # runs a Hunger Games simulation
    @commands.command(aliases = ['Hungergames', 'hunger_games', 'Hunger_games', 'hg', 'Hg'])
    @commands.max_concurrency(1, per = commands.BucketType.channel, wait = False)
    async def hungergames(self, ctx, *, category = None):

        if category == None:
            await ctx.send('You need to pick a category, pabo. Check `k.hungergames_ex` for a full list.')
            return
        if category.lower() in ['female', 'females', 'f', 'girl', 'girls', 'g', 
                                'male', 'males', 'm', 'boy', 'boys', 'b', 
                                'mixed', 'mix', 'mx']:
            pass
        else:
            await ctx.send("That's not a proper category, pabo. Check `k.hungergames_ex` for a full list.")
            return

        reapembed = discord.Embed(title = 'Hunger Games - Reaping', colour = discord.Colour(0xefe61),
        description = "Join - 🏆    Start - ✅    Quit - ❌\n\nCareful - once you join, there's no going back.")
        reapembed.set_thumbnail(url = 'https://imgur.com/09B1zTq.gif')
        reapembed.add_field(name = 'Tributes: ', value = '*None so far...*')
        reapembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        reapembed.timestamp = datetime.datetime.utcnow()

        reapmessage = await ctx.send(embed = reapembed)
        await reapmessage.add_reaction('🏆')
        await reapmessage.add_reaction('✅')
        await reapmessage.add_reaction('❌')

        dtributes = {}
        startgame = False
        while not startgame:
            try: 
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = lambda reaction, 
                user: ((str(reaction.emoji) == '🏆' or\
                      (str(reaction.emoji) == '✅' and user == ctx.author) or\
                      (str(reaction.emoji) == '❌' and user == ctx.author))
                      and reaction.message.id == reapmessage.id))
            except asyncio.TimeoutError:
                await reapmessage.delete()
                await ctx.send('Hunger Games timed out. Be faster next time, pabo.')
                return
            else:
                if str(reaction.emoji) == '🏆':
                    dtributes[user.name] = [user.avatar_url, user.id]
                    if len(list(dtributes.keys())) == 24:
                        startgame = True
                    else:
                        reapembed.set_field_at(0, name = f'Tributes: {len(list(dtributes.keys()))}', 
                        value = ', '.join(list(dtributes.keys())))
                        await reapmessage.edit(embed = reapembed)
                elif str(reaction.emoji) == '✅':
                    startgame = True
                elif str(reaction.emoji) == '❌':
                    await reapmessage.delete()
                    cancelled = await ctx.send('Hunger Games cancelled.')
                    await asyncio.sleep(10)
                    await cancelled.delete()
                    return
        
        await reapmessage.delete()

        arenas = {

        'Swamp': ["The Swamp arena is renowed for being one of the most gruelling. Hot and humid, \
with long stretches of grassy fields, cypress swamps, and mangrove forests, navigating the terrain itself is a \
challenge. Pair that with an abundance of alligators, snakes, and other *surprises*, surviving here will take \
true grit. Oh, and don't forget about the other tributes trying to kill you, of course.", 
        'https://imgur.com/HZyIiDS.png'],

        'Forest': ["Don't underestimate the Forest arena just based on its familiarity. This place holds more surprises \
than you'd expect. Watch where you step, and always keep track of your surroundings — you never know what'll come \
leaping out at you through the bushes. Hopefully you've honed your tree-climbing skills during training. Otherwise... \
well, you'll discover that for yourself.",
        'https://imgur.com/iYRTJNm.png'], 
        
        'Urban': ["Modelled after what used to be known as Washington DC, the Urban arena is flush with decrepit structures, \
abandoned government buildings, and damp sewage tunnels. Hunker down in the catwalk of a spacious warehouse or maneveur \
your way up to the rooftop of one of the numerous skyscrapers to gaze up at the daily death recap. But beware: something \
lurks in the shadows during the day, only to roam free at night.",
        'https://imgur.com/KSyEHKe.png'], 
        
        'Beach': ["You'll be disappointed to hear that the Beach arena doesn't boast an all-you-can-drink bar or two-for-one \
jet-skiing excursions. But perhaps it's not too far off. Build a sand castle on the shore while you wait for \
the daily tsunami wave, explore the rocky shoals with a partner and test out just how lethal the stingray-infested \
waters are, and look forward to what fast approaches after the second wave hits. Fun for the whole family!",
        'https://imgur.com/aUZFTJj.png'], 

        'Tundra': ["By far the most extreme of them all, surviving the Tundra arena is no easy task. The real threat here isn't the \
other tributes — it's the environment. Hopefully you bulked up during training and packed on a few extra pounds; you'll need \
them to tide you over when the temperatures drop far below zero and food begins growing scarce. If it's of any consolation, \
at least everyone else is also freezing to death.",
        'https://imgur.com/wS9JjMQ.png'],

        'Desert': ["Compared to the Tundra arena, the Desert arena places you on the opposite end of the spectrum. You'll be \
forced to trek for hours through gruelling heat and little to no shade, all while an assortment of scorpions, snakes, and spiders \
roam the ground beneath your feet. Watch where you step, and make sure to locate a source of water quickly. Otherwise, you might \
find that your journey in the Games will end sooner than you think.",
        'https://imgur.com/7Plko3o.png']

        }

        gbots = ['Irene', 'Seulgi', 'Wendy', 'Joy', 'Yeri',
                'Jennie', 'Jisoo (BP)', 'Rosé', 'Lisa',
                'Nayeon', 'Jihyo', 'Jeongyeon', 'Mina', 'Momo', 'Sana', 'Dahyun (TWICE)', 'Chaeyoung (TWICE)', 'Tzuyu',
                'Yeji', 'Lia', 'Ryujin', 'Chaeryeong', 'Yuna (ITZY)',
                'Juri', 'Yeonhee', 'Suyun', 'Yunkyoung', 'Sohee', 'Dahyun (RCPC)',
                'Soyeon', 'Minnie', 'Soojin', 'Miyeon', 'Shuhua', 'Yuqi',
                'Saerom', 'Jiwon (f9)', 'Jisun', 'Hayoung (f9)', 'Gyuri', 'Jiheon', 'Seoyeon', 'Chaeyoung (f9)', 'Nakyung',
                'Seungyeon', 'Seunghee (CLC)', 'Elkie', 'Sorn', 'Yujin (CLC)', 'Yeeun', 'Eunbin',
                'Sua', 'Siyeon', 'Handong', 'Gahyeon', 'Yoohyeon', 'Dami', 'Jiu',
                'Haseul', 'Heejin', 'Hyunjin (LOONA)', 'Yeojin', 'Vivi', 'Jinsoul', 'Kim Lip', 'Yves', 'Gowon', 'Olivia Hye', 'Choerry', 'Chuu',
                'Solar', 'Moonbyul', 'Wheein', 'Hwasa',
                'Sowon', 'Yerin', 'Eunha', 'Yuju (GFriend)', 'SinB', 'Umji',
                'E:U', 'Aisha', 'Mia', 'Yiren', 'Onda', 'Sihyeon',
                'Wonyoung', 'Sakura', 'Nako', 'Yuri', 'Eunbi', 'Hyewon', 'Yena', 'Chaeyeon', 'Chaewon', 'Minju', 'Hitomi', 'Yujin (IZ)',
                'Suyeon', 'Elly', 'Yoojung', 'Doyeon', 'Sei', 'Lua', 'Rina', 'Lucy',
                'Hyojung', 'Mimi', 'Yooa', 'Seunghee (OMG)', 'Jiho', 'Binnie', 'Arin',
                'Hyebin', 'Jane', 'Nayun', 'Jooe', 'Ahin', 'Nancy',
                'Haeyoon', 'Yuju (CB)', 'Bora', 'Jiwon (CB)', 'Remi', 'Chaerin', 'May',
                'Baby Soul', 'Jiae', 'Jisoo (Lovelyz)', 'Mijoo', 'Kei', 'Jin (Lovelyz)', 'Sujeong', 'Yein',
                'Seola', 'Bona', 'Exy', 'Soobin (WJSN)', 'Luda', 'Dawon (WJSN)', 'Eunseo', 'Yeoreum', 'Dayoung', 'Yeonjung',
                'Léa', 'Dita', 'Jinny', 'Soodam', 'Denise',
                'Songhee', 'Yiyeon', 'Simyeong', 'Jungwoo (BVNDIT)', 'Seungeun',
                'Solji', 'LE', 'Hani', 'Hyelin', 'Jeonghwa',
                'Victoria', 'Amber', 'Luna', 'Krystal',
                'Jimin (AOA)', 'Yuna (AOA)', 'Hyejeong', 'Seolhyun', 'Chanmi',
                'Chorong', 'Bomi', 'Eunji', 'Naeun', 'Namjoo', 'Hayoung (Apink)',
                'CL', 'Park Bom', 'Dara', 'Minzy',
                'Taeyeon', 'Sunny', 'Tiffany', 'Hyoyeon', 'Yuri', 'Sooyoung', 'Yoona', 'Seohyun',
                'Sunmi', 'Chungha', 'Somi', 'IU', 'Hyuna', 'Heize', 'Eyedi', 'Leebada', 'Boa', 'Ailee', 'Jessi', 'Lee Hi']

        bbots = ['RM', 'Jungkook', 'V', 'Jin', 'J-Hope', 'Suga', 'Jimin (BTS)',
                 'Baekhyun', 'Chen', 'D.O', 'Chanyeol', 'Sehun', 'Xiumin', 'Lay', 'Kai', 'Suho', 'Luhan', 'Kris', 'Tao',
                 'Bang Chan', 'Lee Know', 'Changbin', 'Hyunjin (SKZ)', 'Han', 'Felix', 'Seungmin', 'I.N',
                 'Shownu', 'Minhyuk (MONSTA)', 'Kihyun', 'Hyungwon', 'Jooheon', 'I.M',
                 'Hui', 'Hongseok', 'Shinwon', 'Yeo One', 'Yuto', 'Kino', 'Wooseok', 'Yan An', 'Jinho',
                 'Seonghwa', 'Hongjoong', 'Yunho', 'Yeosang', 'San', 'Mingi', 'Wooyoung', 'Jongho',
                 'Yeonjun', 'Soobin (TXT)', 'Beomgyu', 'Taehyun', 'Huening Kai',
                 'Taeil', 'Johnny', 'Taeyong', 'Yuta', 'Kun', 'Doyoung', 'Ten', 'Jaehyun', 'Winwin', 'Jungwoo (NCT)', 
                 'Lucas', 'Mark', 'Xiao Jun', 'Hendery', 'Renjun', 'Jeno', 'Haechan', 'Jaemin', 'Yang Yang', 'Chenle', 'Jisung',
                 'Eunkwang', 'Minhyuk (BtoB)', 'Changsub', 'Hyunsik', 'Peniel', 'Ilhoon', 'Sungjae',
                 'G-Dragon', 'T.O.P', 'Taeyang (BB)', 'Daesung',
                 'Leeteuk', 'Heechul', 'Yesung', 'Shindong', 'Eunhyuk', 'Siwon', 'Donghae', 'Ryeowook', 'Kyuhyun',
                 'S.Coups', 'Jeonghan', 'Joshua', 'Jun', 'Hoshi', 'Wonwoo', 'Woozi', 'DK', 'Mingyu', 'The8', 'Seungkwan', 'Vernon', 'Dino',
                 'Youngbin', 'Inseong', 'Jaeyoon', 'Dawon (SF9)', 'Zuho', 'Rowoon', 'Taeyang (SF9)', 'Hwiyoung', 'Chani',
                 'Woong', 'Donghyun', 'Woojin', 'Daehwi', 'Youngmin',
                 'Sungjin', 'Jae', 'Young K', 'Wonpil', 'Dowoon',
                 'Jay', 'Song', 'Bobby', 'DK', 'Ju-Ne', 'Chan', 'B.I',
                 'Taemin', 'Onew', 'Key', 'Minho',
                 'Jinu', 'Hoony', 'Mino', 'Yoon',
                 'JR', 'Aron', 'Baekho', 'Minhyun', 'Ren',
                 'Edawn', 'PSY', 'Crush', 'pH-1', 'Giriboy', 'JYP', 'SM', 'YG']
                
        arena = random.choice(list(arenas.keys()))

        if category.lower() in ['female', 'females', 'f', 'girl', 'girls', 'g']:
            bots = gbots
        elif category.lower() in ['male', 'males', 'm', 'boy', 'boys', 'b']:
            bots = bbots
        elif category.lower() in ['mixed', 'mix', 'mx']:
            bots = gbots + bbots

        random.shuffle(bots)
        alltributes =  list(dtributes.keys()) + bots[:24 - len(list(dtributes.keys()))]
        random.shuffle(alltributes)

        dstats = {}
        for i in alltributes:
            dstats[i] = [0, '']

        startembed = discord.Embed(title = f'Hunger Games - Arena: {arena}', colour = discord.Colour(0xefe61), 
        description = arenas[arena][0])
        startembed.set_thumbnail(url = arenas[arena][1])
        d = {}
        n = 1
        for t1, t2 in zip(alltributes[0::2], alltributes[1::2]):
            startembed.add_field(name = f'District {n}:', value = f"{t1}\n{t2}")
            d[f'District {n}'] = [t1, t2]
            n += 1
        startembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        startembed.timestamp = datetime.datetime.utcnow()

        startmessage = await ctx.send(embed = startembed)
        await startmessage.add_reaction('▶️')
        await startmessage.add_reaction('❌')

        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 180, check = lambda reaction, 
            user: (((str(reaction.emoji) == '▶️' and user == ctx.author and user != ctx.bot.user) or\
                  (str(reaction.emoji) == '❌' and user == ctx.author and user != ctx.bot.user)) and\
                   reaction.message.id == startmessage.id))
        except asyncio.TimeoutError:
            await startmessage.delete()
            await ctx.send('Hunger Games timed out. Be faster next time, pabo.')
            return
        else:
            if str(reaction.emoji) == '❌':
                await startmessage.delete()
                cancelled = await ctx.send('Hunger Games cancelled.')
                await asyncio.sleep(10)
                await cancelled.delete()
                return
            elif str(reaction.emoji) == '▶️':
                starting = await ctx.send('*Games beginning in 5...*')
                t = 4
                while t > 0:
                    await asyncio.sleep(1)
                    await starting.edit(content = f'*Games beginning in {t}...*')
                    t -= 1

                await asyncio.sleep(1)
                await starting.delete()
                await startmessage.clear_reactions()
                await asyncio.sleep(1)

                careers = d['District 1'] + d['District 2'] + d['District 4']
                noncareers = list(filter(lambda x: x not in careers, alltributes))
                random.shuffle(careers)
                random.shuffle(noncareers)
                alive = alltributes
                dead = []
                day = 1
                sponsored = 0

                while len(alive) > 2:
                    dead = []
                    description = []

                    if day == 1:
                        percentage = random.randint(33, 50) / 100
                        deadper = round(percentage * len(noncareers))
                        if random.randint(1, 100) > 10:
                            dead = noncareers[:deadper] + [careers[0]]
                            alive = list(filter(lambda x: x not in dead, alive))
                            for i in dead:
                                if random.randint(0, 100) > 75:
                                    killer = random.choice(careers[1:])
                                    dstats[killer][0] += 1
                                    dstats[i][1] = day
                                else:
                                    killer = random.choice(alive)
                                    dstats[killer][0] += 1
                                    dstats[i][1] = day
                        else: 
                            dead = noncareers[:deadper] 
                            alive = list(filter(lambda x: x not in dead, alive))
                            for i in dead:
                                killer = random.choice(alive)
                                dstats[killer][0] += 1
                                dstats[i][1] = day

                        deathrate = '{:.2f}'.format(len(dead)/24)
                        if len(dead) >= 9:
                            description.append(f'Bloodbath rating: **Brutal**\n\
                                                 Death rate: **{deathrate}**\n\n\
                            The audience found this bloodbath to be incredibly entertaining.\n\
                                Plenty of kills made for a solid viewing experience.')
                        elif len(dead) >= 6:
                            description.append(f'Bloodbath rating: **Standard**\n\
                                                 Death rate: **{deathrate}**\n\n\
                            The audience found this bloodbath to be pretty standard.\n\
                                No one stood out in particular.')
                        else:
                            description.append(f'Bloodbath rating: **Boring**\n\
                                                 Death rate: **{deathrate}**\n\n\
                            The audience found this bloodbath to be rather boring.\n\
                                A lower-than-average amount of kills made for a dull viewing experience.')

                    verbs = ['killed', 'slaughtered', 'obliterated', 'murdered', 'destroyed', 'butchered',
                             'decimated', 'wrecked', 'annihilated', 'eradicated', 'exterminated']
                    weapons = ['knife', 'throwing knife', 'machete', 'bow', 'hatchet', 'spear', 'large rock',
                               'single punch', 'well-placed kick', 'solid jab to the throat', 'mace', 'baton',
                               'blowgun', 'blowtorch', 'brick', 'crossbow', 'sickle', 'slingshot', 'sword',
                               'shard of glass', 'rusty axe']
                                
                    if day != 1:
                        random.shuffle(alive)
                        percentage = random.randint(25, 33) / 100
                        deadper = round(percentage * len(alive))
                        dead = alive[:deadper] 
                        alive = list(filter(lambda x: x not in dead, alive))

                        if percentage >= 0.31:
                            description.append(f'Audience rating: **Brutal**\n')
                        elif percentage >= 0.28:
                            description.append(f'Audience rating: **Standard**\n')
                        else:
                            description.append(f'Audience rating: **Boring**\n')
                        
                        for i in dead:
                            if arena == 'Swamp':
                                events = ['was swallowed whole by a python.', 'was eaten by an alligator.',
                                          'fell into piranha-infested waters.', 'was killed by massive leeches.',
                                          'was eaten by a crocodile.', 'was attacked by a giant lizard.',
                                          'was chewed up by a killer turtle.', 'was pecked to death by a heron.',
                                          'fell onto a nest of fire ants.', 'drank dirty water and fell fatally ill.',
                                          'got lost in the reeds and died of fatigue.', 'drowned in a flash flood.']

                            elif arena == 'Forest':
                                events = ['was unable to escape a forest fire.', 'fell out of a tree and was impaled.',
                                          'was attacked by a bear.', 'was mauled by a lynx.',
                                          'was eaten by a giant snake.', 'tripped and suffered a fatal head wound.',
                                          'unknowingly consumed poisonous berries.', 'fell off a cliff.', 
                                          'ate bad mushrooms and went insane.', 'was attacked by a cougar.',
                                          'drowned in a river.', 'was buried in an avalanche.']

                            elif arena == 'Urban':
                                events = ['was attacked by a pack of wolves.', 'fell from the roof of a building.',
                                          'was buried in a collapsing building.', 'got lost in the tunnels and went insane.',
                                          'was pecked to death by crows.', 'fell and was impaled by rebar.',
                                          'bled to death from broken glass.', 'was hunted down by a rabid dog.', 
                                          'fell off a balcony.', 'got trapped in a bunker and went insane.',
                                          'died in a gasoline fire.', 'died while crossing a collapsing bridge.']

                            elif arena == 'Beach':
                                events = ['drowned in the second tsunami wave.', 'was stung by a stingray.',
                                          'was eaten by a shark.', 'drowned while swimming.',
                                          'was killed by a giant lobster.', 'fell victim to a killer turtle.',
                                          'was pulled underwater by a giant squid.', 'was attacked by a school of fish.',
                                          'was swallowed by a whale.', 'was pulled underwater by a rip current.',
                                          'was sucked into a whirlpool.', 'was stung by a jellyfish.']

                            elif arena == 'Tundra':
                                events = ['was pushed off a cliff by a mountain goat.', 'was speared by an ox.',
                                          'was attacked by a killer penguin.', 'was slaughtered by a rabid polar bear.',
                                          'died from extreme hypothermia.', 'starved to death.',
                                          'was buried in an avalanche.', 'froze to death in a blizzard.',
                                          'got lost in a cave and went insane.', 'fell into ice cold water and drowned.',
                                          'suffered extreme frostbite and went insane.', 'was snatched by a giant snowy owl.']

                            elif arena == 'Desert':
                                events = ['died from extreme heat stroke.', 'got sucked into quicksand.',
                                          'was stung by a scorpion.', 'was attacked by a rattlesnake.',
                                          'died of severe dehydration.', 'began hallucinating and went insane.',
                                          'was pecked to death by vultures.', 'was attacked by a hyena.',
                                          'was eaten by a giant lizard.', 'got lost in a dust storm and went insane.',
                                          'was mauled by a group of jackals.', 'was bitten by a venomous spider.']

                            if random.randint(0, 100) <= 30:
                                    description.append(f"{i} {random.choice(events)}")
                            else:
                                killer = random.choice(alive)
                                dstats[killer][0] += 1
                                description.append(f"{killer} {random.choice(verbs)} {i} with a {random.choice(weapons)}.")
                            dstats[i][1] = day
                            

                        if random.randint(0, 100) >= 50 and sponsored < 2 and day <= 5:
                            choice1 = random.choice(alive)
                            choice2 = random.choice(list(filter(lambda x: x != choice1, alive)))

                            plusminus1 = f"{random.randint(1, 100)} {random.choice(['+', '-'])} {random.randint(1, 100)}"
                            plusminus2 = f"{random.randint(1, 100)} {random.choice(['+', '-'])} {random.randint(1, 100)}"
                            eplusminus1 = str(simplify(plusminus1))
                            eplusminus2 = str(simplify(plusminus2))
                            multiply1 = f"{random.randint(2, 12)} * {random.randint(2, 12)}"
                            multiply2 = f"{random.randint(2, 12)} * {random.randint(2, 12)}"
                            emultiply1 = str(simplify(multiply1))
                            emultiply2 = str(simplify(multiply2))
                            exponent1 = f"{random.randint(2, 10)} ** {random.randint(0, 3)}"
                            exponent2 = f"{random.randint(2, 10)} ** {random.randint(0, 3)}"
                            eexponent1 = str(simplify(exponent1))
                            eexponent2 = str(simplify(exponent2))
                            remainder1 = f"{random.randint(50, 100)} % {random.randint(1, 49)}"
                            remainder2 = f"{random.randint(50, 100)} % {random.randint(1, 49)}"
                            eremainder1 = str(simplify(remainder1))
                            eremainder2 = str(simplify(remainder2))

                            sptasks1 = {f"Solve: `{plusminus1}`": eplusminus1,
                                        f"Solve: `{multiply1.replace('*', 'x')}`": emultiply1, 
                                        f"Solve: `{exponent1.replace('**', '^')}`": eexponent1, 
                                        f"Find the remainder: `{remainder1.replace('%', '/')}`": eremainder1}

                            sptasks2 = {f"Solve: `{plusminus2}`": eplusminus2, 
                                        f"Solve: `{multiply2.replace('*', 'x')}`": emultiply2, 
                                        f"Solve: `{exponent2.replace('**', '^')}`": eexponent2,  
                                        f"Find the remainder: `{remainder2.replace('%', '/')}`": eremainder2}

                            randomsptask = random.randint(0, len(sptasks1) - 1)
                            qsptask1 = list(sptasks1.keys())[randomsptask]
                            asptask1 = sptasks1[qsptask1]
                            qsptask2 = list(sptasks2.keys())[randomsptask]
                            asptask2 = sptasks2[qsptask2]

                            while asptask1 == asptask2:
                                if randomsptask == 0:
                                    sptask2 = f"{random.randint(1, 50)} {random.choice(['+', '-'])} {random.randint(1, 50)}"
                                    asptask2 = str(simplify(sptask2))
                                elif randomsptask == 1:
                                    sptask2 = f"{random.randint(2, 12)} * {random.randint(2, 12)}"
                                    asptask2 = str(simplify(sptask2))
                                elif randomsptask == 2:
                                    sptask2 = f"{random.randint(1, 8)} ** {random.randint(1, 8)}"
                                    asptask2 = str(simplify(sptask2))
                                else:
                                    sptask2 = f"{random.randint(50, 100)} % {random.randint(1, 49)}"
                                    asptask2 = str(simplify(sptask2))

                            sponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor', colour = discord.Colour(0xefe61),
                            description = f'Chance to sponsor **{choice1}** or **{choice2}**! First task completed will result in that\
                            tribute being sponsored.')
                            sponsorembed.add_field(name = f'Sponsor {choice1}:', value = qsptask1)
                            sponsorembed.add_field(name = f'Sponsor {choice2}:', value = qsptask2)
                            sponsorembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                            sponsorembed.timestamp = datetime.datetime.utcnow()

                            sponsormessage = await ctx.send(embed = sponsorembed)

                            def checksponsor(sponsoranswer: discord.Message): 
                                return (sponsoranswer.channel == sponsormessage.channel and sponsoranswer.content == asptask1) or\
                                    (sponsoranswer.channel == sponsormessage.channel and sponsoranswer.content == asptask2)
                            try:
                                sponsoranswer = await self.bot.wait_for('message', timeout = 120, check = checksponsor)
                            except asyncio.TimeoutError:
                                await sponsormessage.delete()
                                await ctx.send('Chance to sponsor timed out. Be faster next time, pabo.')
                                await ctx.send(f"The correct answers are: `{asptask1}` and `{asptask2}`.")
                                await asyncio.sleep(3)
                            else:

                                gifts = ['trident', 'machine gun', 'katana', 'silenced pistol', 'flamethrower', 'shotgun', 
                                         'chainsaw', 'rifle', 'sniper rifle', 'stun gun', 'crossbow with explosive arrows',
                                         'shuriken', 'silenced assault rifle', 'crossbow with poisonous arrows', 'grenade launcher']
                                gift = random.choice(gifts)
                                    
                                if sponsoranswer.content == asptask1:
                                    if random.randint(0, 100) <= 10 :
                                        sponsordeath = 'None'
                                        description.append(f"{choice1} attempted to kill {choice2} with a {gift} but was too slow.")
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice1}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\nHowever, {choice2} spots the parachute as it comes down \
                                                and flees before {choice1} can make use of its contents. Better luck next time.")
                                    elif random.randint(0, 100) <= 10:
                                        sponsordeath = choice1
                                        description.append(f"{choice1} accidentally killed him/herself with a {gift}.")
                                        dead.append(choice1)
                                        dstats[choice1][1] = day
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice1}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\n{choice1} snatches the weapon and goes off to pursue \
                                                an unsuspecting {choice2}, {gift} in hand, but in a moment of clumsiness, ends \
                                                    up turning the weapon the wrong way and dying an embarrassing death.")
                                    else:
                                        sponsordeath = choice2
                                        description.append(f"{choice1} slaughtered {choice2} with a {gift}.")
                                        dead.append(choice2)
                                        dstats[choice1][0] += 1
                                        dstats[choice2][1] = day
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice1}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\nOverjoyed, {choice1} takes a few moments getting comfortable \
                                                with the weapon before heading off to intercept {choice2} and make very good use of it.")
                                    
                                elif sponsoranswer.content == asptask2:
                                    if random.randint(0, 100) <= 10 :
                                        sponsordeath = 'None'
                                        description.append(f"{choice2} attempted to kill {choice1} with a {gift} but was too slow.")
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice2}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\nHowever, {choice1} spots the parachute as it comes down \
                                                and flees before {choice2} can make use of its contents. Better luck next time.")
                                    elif random.randint(0, 100) <= 10:
                                        sponsordeath = choice2
                                        description.append(f"{choice2} accidentally killed him/herself with a {gift}.")
                                        dead.append(choice2)
                                        dstats[choice2][1] = day
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice2}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\n{choice2} snatches the weapon and goes off to pursue \
                                                an unsuspecting {choice1}, {gift} in hand, but in a moment of clumsiness, ends \
                                                    up turning the weapon on him/herself and dying an embarrassing death.")
                                    else:
                                        sponsordeath = choice1
                                        description.append(f"{choice2} slaughtered {choice1} with a {gift}.")
                                        dead.append(choice1)
                                        dstats[choice2][0] += 1
                                        dstats[choice1][1] = day
                                        wsponsorembed = discord.Embed(title = f'Hunger Games - {arena} - Sponsor',
                                        colour = discord.Colour(0xefe61),
                                        description = f"**{choice2}** has been sponsored! A parachute floats down from the \
                                            sky to reveal a **{gift}**!\n\nOverjoyed, {choice2} takes a few moments getting comfortable \
                                                with the weapon before heading off to intercept {choice1} and make very good use of it.")

                                alive = list(filter(lambda x: x not in dead, alive))

                                wsponsorembed.add_field(name = 'Sponsor gift:', value = gift.capitalize())
                                wsponsorembed.add_field(name = 'Deaths:', value = sponsordeath)
                                wsponsorembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                                wsponsorembed.timestamp = datetime.datetime.utcnow()

                                sponsored += 1
                                await sponsormessage.delete()
                                wsponsormessage = await ctx.send(embed = wsponsorembed)
                                await wsponsormessage.add_reaction('▶️')
                                await wsponsormessage.add_reaction('❌')
                                
                                try: 
                                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 180, check = lambda reaction, 
                                    user: (((str(reaction.emoji) == '▶️' and user == ctx.author and user != ctx.bot.user) or\
                                          (str(reaction.emoji) == '❌' and user == ctx.author and user != ctx.bot.user)) and\
                                           reaction.message.id == wsponsormessage.id))
                                except asyncio.TimeoutError:
                                    await wsponsormessage.delete()
                                    return
                                else:
                                    if str(reaction.emoji) == '❌':
                                        await wsponsormessage.delete()
                                        await ctx.send('Hunger Games cancelled.')
                                        return
                                    elif str(reaction.emoji) == '▶️':
                                        await wsponsormessage.delete()

                    if len(alive) == 1:
                        alive.append(dead[-1])
                        dead.remove(dead[-1])
                        description = description[:-1]
                    if len(alive) == 0:
                        alive.append(dead[-1])
                        alive.append(dead[-2])
                        dead.remove(dead[-1])
                        dead.remove(dead[-2])
                        description = description[:-2]
                    if not dead:
                        deadvalue = 'None'
                        deadnum = '0'
                    else:
                        deadvalue = '\n'.join(dead)
                        deadnum = len(dead)

                    text = '\n'.join(description)
                    dembed = discord.Embed(title = f'Hunger Games - {arena} - Day {day} Recap', colour = discord.Colour(0xefe61), 
                    description = text) 

                    dembed.add_field(name = f'Alive ({len(alive)}):', value = '\n'.join(alive))
                    dembed.add_field(name = f'Deceased ({deadnum}):', value = deadvalue)
                    dembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    dembed.timestamp = datetime.datetime.utcnow()

                    dmessage = await ctx.send(embed = dembed)
                    await dmessage.add_reaction('▶️')
                    await dmessage.add_reaction('❌')

                    try: 
                        reaction, user = await self.bot.wait_for('reaction_add', timeout = 180, check = lambda reaction, 
                        user: (((str(reaction.emoji) == '▶️' and user == ctx.author and user != ctx.bot.user) or\
                              (str(reaction.emoji) == '❌' and user == ctx.author and user != ctx.bot.user)) and\
                               reaction.message.id == dmessage.id))
                    except asyncio.TimeoutError:
                        await dmessage.delete()
                        await ctx.send('Hunger Games timed out. Be faster next time, pabo.')
                        return
                    else:
                        if str(reaction.emoji) == '❌':
                            await dmessage.delete()
                            cancelled = await ctx.send('Hunger Games cancelled.')
                            await asyncio.sleep(10)
                            await cancelled.delete()
                            return
                        elif str(reaction.emoji) == '▶️':
                            await dmessage.delete()
                            day += 1

                dmatchstyle = discord.Embed(title = f"Hunger Games - {arena} - Gamemaker's Choice", colour = discord.Colour(0xefe61),
                description = 'Choose the deathmatch style!\n\nTrivia: ❓\n\nRNG:   🎲')
                dmatchstyle.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                dmatchstyle.timestamp = datetime.datetime.utcnow()

                stylemessage = await ctx.send(embed = dmatchstyle)
                await stylemessage.add_reaction('❓')
                await stylemessage.add_reaction('🎲')
                pickrng = False

                try: 
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 180, check = lambda reaction, 
                    user: ((str(reaction.emoji) == '❓' and user == ctx.author) or\
                          (str(reaction.emoji) == '🎲' and user == ctx.author)
                           and reaction.message.id == stylemessage.id))
                except asyncio.TimeoutError:
                    await stylemessage.delete()
                    await ctx.send('Hunger Games timed out. Be faster next time, pabo.')
                    return
                else:
                    if str(reaction.emoji) == '🎲':
                        pickrng = True
                        await stylemessage.delete()
                    elif str(reaction.emoji) == '❓':
                        url = 'https://opentdb.com/api.php?amount=2&difficulty=easy&type=multiple'
                        request = requests.get(url)
                        dmtrivia = json.loads(request.text)

                        dmatchtasks = {html.unescape(dmtrivia['results'][0]['question']): 
                                       html.unescape(dmtrivia['results'][0]['correct_answer']),
                                       html.unescape(dmtrivia['results'][1]['question']): 
                                       html.unescape(dmtrivia['results'][1]['correct_answer'])}

                        qdmtask1 = list(dmatchtasks.keys())[0]
                        admtask1 = dmatchtasks[qdmtask1].lower()
                        qdmtask2 = list(dmatchtasks.keys())[1]
                        admtask2 = dmatchtasks[qdmtask2].lower()

                        dmatchembed = discord.Embed(title = f'Hunger Games - {arena} - Deathmatch', colour = discord.Colour(0xefe61),
                        description = 'The first task completed will decide the outcome of the Games!')
                        dmatchembed.add_field(name = f'{alive[0]}:', value = qdmtask1)
                        dmatchembed.add_field(name = f'{alive[1]}:', value = qdmtask2)
                        dmatchembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                        dmatchembed.timestamp = datetime.datetime.utcnow()

                        dmatchmessage = await ctx.send(embed = dmatchembed)
                
                        def checkdmatch(dmatchanswer: discord.Message): 
                            return (dmatchanswer.channel == dmatchmessage.channel and dmatchanswer.content.lower() == admtask1.lower() and 
                                    dmatchanswer.author.id != ctx.bot.user.id) or\
                                   (dmatchanswer.channel == dmatchmessage.channel and dmatchanswer.content.lower() == admtask2.lower() and 
                                    dmatchanswer.author.id != ctx.bot.user.id)
                        try:
                            dmatchanswer = await self.bot.wait_for('message', timeout = 90, check = checkdmatch)
                        except asyncio.TimeoutError:
                            pickrng = True
                            await ctx.send('Deathmatch trivia timed out. Be faster next time, pabo.')
                            await ctx.send(f"The correct answers are: `{admtask1}` and `{admtask2}`.")
                            RNG = await ctx.send('Now picking via RNG...')
                            await asyncio.sleep(2)
                            await RNG.edit(content = 'Now picking via RNG... ✅')
                            await asyncio.sleep(1)
                            await RNG.delete()

                if pickrng:
                    victor = alive[random.choice([0, 1])]
                    dstats[victor][0] += 1
                    if victor == alive[0]:
                        dstats[alive[1]][1] = day
                        runnerup = alive[1]
                    else:
                        dstats[alive[0]][1] = day
                        runnerup = alive[0]
                elif dmatchanswer.content.lower() == admtask1.lower():
                    victor = alive[0]
                    runnerup = alive[1]
                    dstats[victor][0] += 1
                    dstats[alive[1]][1] = day
                elif dmatchanswer.content.lower() == admtask2.lower():
                    victor = alive[1]
                    runnerup = alive[0]
                    dstats[victor][0] += 1
                    dstats[alive[0]][1] = day

                counter = 1
                for i in list(d.values()):
                    if victor == i[0] or victor == i[1]:
                        victordistrict = counter
                        break
                    counter += 1

                victorembed = discord.Embed(title = f'Hunger Games - {arena} - Victor', colour = discord.Colour(0xefe61),
                description = f'Congratulations, **{victor}** from District {victordistrict}!')
                victorembed.add_field(name = 'Kills:', value = dstats[victor][0])
                victorembed.add_field(name = 'Duration:', value = f'{day} days')
                victorembed.add_field(name = 'Runner-up:', value = runnerup)
                victorembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                victorembed.timestamp = datetime.datetime.utcnow()

                victorembed = await ctx.send(embed = victorembed)
                await asyncio.sleep(3)

                victorkills = dstats[victor][0]
                if victorkills >= 5:
                    victorrating = 'Brutally entertaining'
                elif victorkills == 4:
                    victorrating = 'Entertaining'
                elif victorkills == 3:
                    victorrating = 'Mildly entertaining'
                elif victorkills == 2:
                    victorrating = 'Slightly boring'
                else:
                    victorrating = 'Very boring'

                dstats[victor][1] = day

                overviewembed = discord.Embed(title = f'Hunger Games - {arena} - Final Standings', colour = discord.Colour(0xefe61), 
                description = f"**Victor:** {victor} | District {victordistrict}\n**Kill count:** {victorkills}\n\
                **Survival:** {day} days\n**Victor rating:** {victorrating}")

                if victor in list(dtributes.keys()):
                    overviewembed.set_thumbnail(url = dtributes[victor][0])

                    pdb = sql.connect('Profiles.sqlite')
                    cursor = pdb.cursor()
                    cursor.execute(f'SELECT House FROM main WHERE UserID = {dtributes[victor][1]}')
                    house = cursor.fetchone()[0]
                    pdb.commit()
                    cursor.close()
                    pdb.close()

                    hdb = sql.connect('Houses.sqlite')
                    cursor = hdb.cursor()
                    cursor.execute(f'SELECT {house} FROM House_points')
                    updated = cursor.fetchone()[0] + 20
                    insert = (f'UPDATE House_points SET {house} = ?')
                    values = (updated,)
                    cursor.execute(insert, values)

                    cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {dtributes[victor][1]}')
                    INupdated = cursor.fetchone()[0] + 20
                    INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
                    INvalues = (INupdated, dtributes[victor][1])
                    cursor.execute(INinsert, INvalues)

                    hdb.commit()
                    cursor.close()
                    hdb.close()

                    hgdb = sql.connect('HG.sqlite')
                    cursor = hgdb.cursor()
                    cursor.execute('SELECT UserID FROM victors')
                    IDlist = cursor.fetchall()

                    x = False
                    for i in IDlist:
                        if str(dtributes[victor][1]) == i[0]:
                            x = True
                            break
                    if x:
                        cursor.execute(f'SELECT Wins FROM victors WHERE UserID = {dtributes[victor][1]}')
                        hgupdated = cursor.fetchone()[0] + 1
                        hginsert = (f'UPDATE victors SET Wins = ? WHERE UserID = ?')
                        hgvalues = (hgupdated, dtributes[victor][1])
                        cursor.execute(hginsert, hgvalues)
                    else:
                        hginsert = ('INSERT INTO victors(UserID, Wins) VALUES(?, ?)')
                        hgvalues = (ctx.author.id, 1)
                        cursor.execute(hginsert, hgvalues)

                    hgdb.commit()
                    cursor.close()
                    hgdb.close()

                else:
                    overviewembed.set_thumbnail(url = 'https://imgur.com/9Pp2BQm.gif')
                
                for i in d.keys():
                    tribute1 = d[i][0]
                    tribute2 = d[i][1]
                    overviewembed.add_field(name = f'{i}:', 
                    value = f"{tribute1} - {dstats[tribute1][0]} - D{dstats[tribute1][1]}\n\
                              {tribute2} - {dstats[tribute2][0]} - D{dstats[tribute2][1]}")
                overviewembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                overviewembed.timestamp = datetime.datetime.utcnow()

                await ctx.send(embed = overviewembed)

    #checks for max concurrency error
    @hungergames.error
    async def hungergames_error(self, ctx, error):
        if isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send('This command can only run one instance at a time per channel. \
Check back in a few moments, or try a different channel.')

    @commands.command(aliases = ['Hungergames_ex', 'hunger_games_ex', 'Hunger_games_ex', 'hg_ex', 'Hg_ex'])
    async def hungergames_ex(self, ctx):
        d = {'Category': ['Female', 'Male', 'Mixed'], 'Alias': ['f, g', 'm, b', 'mx']}
        index = [1, 2, 3]
        df = pd.DataFrame(data = d, index = index)
        await ctx.send(f'```Due to the nature of this command, it can only run one instance at a time per channel.\n\n\
Full list of categories:\n\n{df}\n\nk.hungergames Mixed\n>>> [Starts up a Hunger Games with both male and female idols]```')

    @commands.command(aliases = ['hg_lb', 'hg_leaderboard', 'hungergames_lb'])
    async def hungergames_leaderboard(self, ctx):
        db = sql.connect('HG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM victors ORDER BY Wins DESC;')
        result = cursor.fetchmany(3)
        cursor.execute(f'SELECT Count(*) FROM victors')
        total = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()

        embed = discord.Embed(title = 'Hunger Games Leaderboard ', colour = discord.Colour(0xefe61))
        embed.set_thumbnail(url = 'https://imgur.com/09B1zTq.gif')

        if total >= 3:
            embed.add_field(name = 'Top Victors:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}\n\
                                                             2. **{self.bot.get_user(int(result[1][0]))}** - {result[1][1]}\n\
                                                             3. **{self.bot.get_user(int(result[2][0]))}** - {result[2][1]}')
        elif total == 2:
            embed.add_field(name = 'Top Victors:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}\n\
                                                             2. **{self.bot.get_user(int(result[1][0]))}** - {result[1][1]}')
        elif total == 1:
            embed.add_field(name = 'Top Victors:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}')
        elif total == 0:
            embed.add_field(name = 'Top Victors:', value = 'None')

        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)


def setup(bot):
    bot.add_cog(Games_Cog(bot))
