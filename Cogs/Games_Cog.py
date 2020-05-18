import discord
import random 
import datetime 
import asyncio
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
                       'https://cdn.discordapp.com/attachments/630633322686578689/708470605556613140/afzxwn0il7221.png']
                    
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
        if 'irene' in choices:
            await ctx.send('irene')
        elif 'Irene' in choices:
            await ctx.send('Irene')
        elif 'lrene' in choices:
            await ctx.send('Irene')
        else:
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
                      "Now beings the important process of DM sliding. Remember: one wrong move, and you're FRIENDZONED.",
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
        
        message = await ctx.send('*Calculating compatibility...*')
        await asyncio.sleep(3)
        await message.delete()
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
    async def spongebobify(self, ctx, *, message):
        L = []
        for i in message:
            if random.choice([True, False]):
                i = i.upper()
                L.append(i)
            else:
                L.append(i)
        await ctx.send(''.join(L))

    @commands.command(aliases = ['Spongebobify_ex', 'copypasta_ex', 'Copypasta_ex'])
    async def spongebobify_ex(self, ctx):
        await ctx.send('```k.spongebobify I begged Angel, any place but England. And 1 year later we were in Manchester, a shithole\n\n\
>>> I BEGgED ANgel, any PLACe But EnGlANd. AnD 1 yEAR lAter WE weRE in MaNcHESter, A shITHolE```')

    # Consumes a str, message
    # Returns the scuffed spongebobified version of the message
    @commands.command(aliases = ['Spongebobify2', 'scuffed', 'Scuffed'])
    async def spongebobify2(self, ctx, *, message):
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

    # Consumes a str, message
    # Returns an uwufied version of the specified message
    @commands.command(aliases = ['Uwufy', 'uwufier', 'Uwufier', 'uwu', 'Uwu'])
    async def uwufy(self, ctx, *, message):
        wd = message.replace('r', 'w').replace('R', 'W').replace('l', 'w').replace('L', 'W')
        punctuation = wd.replace('!', '!!!!! owo').replace('?', '?!??!!?')
        emojis = punctuation.replace('❤️', '<3').replace('♥️', '<3').replace('💕', '<3 <3').replace('😊', '>w<')
        no = emojis.replace('no', 'nyo').replace('No', 'Nyo')
        uwu = no.replace('you', 'youwu').replace('You', 'Youwu')
        await ctx.send(uwu)

    @commands.command(aliases = ['Uwufy_ex', 'uwufier_ex', 'Uwufier_ex', 'uwu_ex', 'Uwu_ex'])
    async def uwufy_ex(self, ctx):
        await ctx.send("```k.uwufy gn everyone ❤️ remember to stay hydrated & please make sure youre washing your hands & staying clean of germs\
 ~ 💕 Take care, we're half way through the week! Stay in there but remember I'm always here if you want someone to talk to about anything \
:PepeLove: 😊 Take care and gave a great day/night! ♥️\n\n\
>>> gn evewyone <3 wemembew to stay hydwated & pwease make suwe youwuwe washing youwuw hands & staying cwean of gewms ~ <3 <3 Take cawe, we'we \
hawf way thwough the week!!!!! owo Stay in thewe but wemembew I'm awways hewe if youwu want someone to tawk to about anything :PepeWove: >w<\
Take cawe and gave a gweat day/night!!!!! owo <3```")

    # Consumes a str, message
    # Returns a scrambled version of the specified message with a 15% chance of a word getting dropped
    @commands.command(aliases = ['Cloutify', 'scramble', 'Scramble', 'jumble', 'Jumble'])
    async def cloutify(self, ctx, *, message):
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


def setup(bot):
    bot.add_cog(Games_Cog(bot))
