import discord
import random
from discord.ext import commands 
from discord.ext.commands.cooldowns import BucketType
import datetime
import asyncio
import string
import sqlite3 as sql

def profile_check(user_id):
    db = sql.connect('Profiles.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT UserID FROM users WHERE UserID = {str(user_id)}')
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result

def house_check(user_id):
    db = sql.connect('Profiles.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT House FROM users WHERE UserID = {str(user_id)}')
    result = cursor.fetchone()[0]
    db.commit()
    cursor.close()
    db.close()
    if result == 'Set your house using `k.get_sorted`.' or result is None:
        return False
    return True

def item_check(item):
    db = sql.connect('RPG.sqlite')
    cursor = db.cursor()
    cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{item}"')
    result = cursor.fetchone()
    db.commit()
    cursor.close()
    db.close()
    return result


class System(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('System: Online')

    @commands.command(aliases = ['Profile_set', 'pro_set', 'Pro_set'])
    async def profile_set(self, ctx):
        if profile_check(ctx.author.id):
            await ctx.send("You've already set up a profile, pabo.")
            return

        db = sql.connect('HG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT Wins FROM victors WHERE UserID = {ctx.author.id}')
        wins = cursor.fetchone()
        if not wins:
            hg = 0
        else:
            hg = wins[0]

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        insert = ('INSERT INTO users(UserID, Handshakes, Bio, House, HG_wins) VALUES(?, ?, ?, ?, ?)')
        values = (ctx.author.id, 0, 'Set up your profile bio using `k.profile_bio`.', 'Set your house using `k.get_sorted`.', hg)
        cursor.execute(insert, values)
        db.commit()
        cursor.close()
        db.close()
        await ctx.send('👍 `k.profile` to view.')

    @commands.command(aliases = ['Profile', 'pro', 'Pro'])
    async def profile(self, ctx, member: discord.Member = None):
        if member is None:
            user = ctx.author
        else:
            user = member

        if not profile_check(user.id):
            if user == ctx.author:
                await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            else:
                await ctx.send("This user doesn't have a profile, pabo. Try again with someone else.")
            return

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE UserID = {user.id}')
        result = cursor.fetchall()[0]
        house = result[3]
        bio = result[2]
        handshakes = result[1]
        wins = result[4]
        db.commit()
        cursor.close()
        db.close()

        if not house_check(user.id):
            points = 'Set your house using `k.get_sorted`.'
            xp = 'Set your house using `k.get_sorted`.'
        else:
            db = sql.connect('Houses.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {user.id}')
            points = cursor.fetchone()[0]
            db.commit()
            cursor.close()
            db.close()

            db = sql.connect('RPG.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT XP FROM users WHERE UserID = {user.id}')
            xp = cursor.fetchone()[0]
            db.commit()
            cursor.close()
            db.close()
        
        embed = discord.Embed(colour = discord.Colour(0xefe61), description = bio)
        embed.set_author(name = f"{user.name}'s Profile", icon_url = f'{user.avatar_url}')
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name = 'House:', value = house)
        embed.add_field(name = 'Points Earned:', value = points)
        embed.add_field(name = 'XP:', value = xp)
        embed.add_field(name = 'Handshakes:', value = handshakes)
        embed.add_field(name = 'HG Wins:', value = wins)
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
        icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Profile_bio', 'pro_bio', 'Pro_bio'])
    async def profile_bio(self, ctx, *, message = None):
        if not profile_check(ctx.author.id):
            await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            return

        if message is None:
            await ctx.send("You can't leave your bio blank, pabo.")
            return
        if len(message) > 200:
            await ctx.send("Your bio is too long, pabo. Make sure it's 200 characters or under.")
            return

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT Bio FROM users WHERE UserID = {ctx.author.id}')
        insert = ('UPDATE users SET Bio = ? WHERE UserID = ?')
        values = (message, ctx.author.id)
        
        cursor.execute(insert, values)
        db.commit()
        cursor.close()
        db.close()
        await ctx.send(f'Profile bio updated to `{message}`.')

    @commands.command(aliases = ['Profile_bio_ex', 'pro_bio_ex', 'Pro_bio_ex'])
    async def profile_bio_ex(self, ctx):
        await ctx.send('```k.profile_bio Irene best.\n>>> [Sets "Irene best." as your profile bio]```')

    @commands.command(aliases = ['Handshake', 'rep', 'Rep'])
    @commands.cooldown(1, 86400, commands.BucketType.user) 
    async def handshake(self, ctx, member: discord.User = None):
        if member is None:
            self.bot.get_command('handshake').reset_cooldown(ctx)
            await ctx.send("You can't shake hands with no one, pabo. Specify a member.")
        elif member.id == ctx.author.id:
            self.bot.get_command('handshake').reset_cooldown(ctx)
            await ctx.send("You can't shake hands with yourself, pabo. Specify a different member.")
        else:
            if not profile_check(member.id):
                self.bot.get_command('handshake').reset_cooldown(ctx)
                await ctx.send("You can't shake hands with someone who doesn't have a profile, pabo.")
                return

            db = sql.connect('Profiles.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT Handshakes FROM users WHERE UserID = {member.id}')
            updated = cursor.fetchone()[0] + 1
            insert = ('UPDATE users SET Handshakes = ? WHERE UserID = ?')
            values = (updated, member.id)

            cursor.execute(insert, values)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f':handshake: Shook hands with {member}.')

    @commands.command(aliases = ['Handshake_ex', 'rep_ex', 'Rep_ex'])
    async def handshake_ex(self, ctx):
        await ctx.send('```k.handshake @Kaiserrollii\n>>> :handshake: Shook hands with @Kaiserrollii.```')

    @commands.command(aliases = ['Get_sorted', 'sorting_quiz', 'Sorting_quiz'])
    async def get_sorted(self, ctx):
        if not profile_check(ctx.author.id):
            await ctx.send("You can't get sorted without a profile, pabo. Create one with `k.profile_set`.")
            return

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT House FROM users WHERE UserID = {ctx.author.id}')
        result = cursor.fetchone()
        if result[0] == 'Set your house using `k.get_sorted`.' or result[0] is None:
            
            startembed = discord.Embed(title = 'The Sorting Bot Quiz', colour = discord.Colour(0xefe61),
            description = "Start - ✅    Quit - ❌\n\nCareful - once you get sorted, you cannot change houses.")
            startembed.set_thumbnail(url = 'https://imgur.com/vCSdbvP.png')
            startembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            startembed.timestamp = datetime.datetime.utcnow()

            startmessage = await ctx.send(embed = startembed)
            await startmessage.add_reaction('✅')
            await startmessage.add_reaction('❌')

            startquiz = False
            while not startquiz:
                try: 
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = lambda reaction, 
                    user: ((str(reaction.emoji) == '✅' and user == ctx.author) or\
                           (str(reaction.emoji) == '❌' and user == ctx.author)
                          and reaction.message.id == startmessage.id))
                except asyncio.TimeoutError:
                    await startmessage.delete()
                    await ctx.send('Sorting Quiz timed out. Be faster next time, pabo.')
                    return
                else:
                    if str(reaction.emoji) == '✅':
                        startquiz = True
                    elif str(reaction.emoji) == '❌':
                        await startmessage.delete()
                        cancelled = await ctx.send('Sorting Quiz cancelled.')
                        await asyncio.sleep(10)
                        await cancelled.delete()
                        return

            await startmessage.delete()

            houses = {'Pink': 0, 'Yellow': 0, 'Blue': 0, 'Green': 0, 'Purple': 0}

            questions = {

'What would you like to be remembered as?': 
['https://imgur.com/aiKD3vV.png', 
['1: Levelheaded', '2: Easygoing', '3: Generous', '4: Self-assured', '5: Influential']], 

'The zombie apocalypse has just begun. What is the first thing you do?': 
['https://imgur.com/E6eL6yo.png', 
['1: Take inventory.', '2: Find a weapon.', '3: Find local law enforcement.', 
'4: Leave the area.', '5: Contact friends and family.']], 

'You are granted one superpower of your choice. What do you choose?': 
['https://imgur.com/NHeWgeu.png',
['1: Invisibility', '2: Super strength', '3: Time travel', '4: Immortality', '5: Teleportation']], 

"Those who don't know you well describe you as **x**, but in actuality, you are **y**.": 
['https://imgur.com/jyFQwJo.png',
['1: Aloof | playful and witty', '2: Scatter-brained | absorbed in the task at hand', 
'3: Overachieving | fearful of disappointing others', '4: Confident | sensitive and emotional', 
'5: Outgoing | uncomfortable being alone']], 

# Icons made by https://www.flaticon.com/authors/geotatah from https://www.flaticon.com/
'When you find a new interest, you:': 
['https://imgur.com/0UO5C8E.png',
['1: Become obsessed and dedicate all your time towards it.', '2: Strive to perfect it.', 
'3: Maintain a healthy balance between it and your other responsibilities.', 
'4: Entertain it for a short while before moving on to something else.', 
'5: Connect with others who share your interest.']], 

'On a quest to face your worst fear, you come across a set of five closed doors, each containing something \
to help guide you along your journey. You may open only one. Which do you choose?': 
['https://imgur.com/T2fiDKt.png',
['1: The leftmost door. Inside it is an old mage who provides you with useful information about your task.', 
'2: Second-to-the-left. In it is a powerful weapon you can use to defend yourself.', 
'3: The rightmost door. It houses a map of the surrounding area with key locations marked.', 
'4: The door in the middle. It contains a well-trained horse that can outrun anything that decides to chase you.', 
'5: Second-to-the-right. In it is a ghostly figure who, although unable to help in combat, can act as a companion and guide.']], 

# Icons made by http://www.freepik.com/ from https://www.flaticon.com/
'You catch a close friend of yours cheating during a final exam. You are the only one to witness it. After the exam is over, do you:': 
['https://imgur.com/4ygucv9.png',
["1: Remain silent about it, but begin to distance youself. You won't ever forget about what your friend did.", 
"2: Speak to your friend privately, making it clear that you disapprove, but going about it in a passive manner. \
Ultimately, you won't let it ruin your friendship.", 
'3: Send the professor an email detailing what you witnessed. There is a chance your friend will find out that you \
were the one who snitched, but you are willing to take that risk.', 
"4: Pretend it never happened, and forget about it. It isn't your business, and tons of people cheat anyway.", 
"5: Say nothing. You don't condone cheating, but since it's your friend, you'll let it go."]]

                             }

            question_list = list(questions.keys())
            random.shuffle(question_list)

            qcounter = 0
            for i in list(range(len(question_list))):
                qcounter += 1

                qembed = discord.Embed(title = f'The Sorting Bot Quiz - Question {qcounter}', colour = discord.Colour(0xefe61),
                description = question_list[i])

                acounter = 0
                answer_list = questions[question_list[i]][1]
                random.shuffle(answer_list)
                nums = list(map(lambda x: x[0], answer_list))

                for j in answer_list:
                    acounter += 1
                    qembed.add_field(name = '\u200b', value = f'**{acounter}.** {j[3:]}', inline = False)

                qembed.set_thumbnail(url = questions[question_list[i]][0])
                qembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                qembed.timestamp = datetime.datetime.utcnow()

                qmessage = await ctx.send(embed = qembed)
                await qmessage.add_reaction('1️⃣')
                await qmessage.add_reaction('2️⃣')
                await qmessage.add_reaction('3️⃣')
                await qmessage.add_reaction('4️⃣')
                await qmessage.add_reaction('5️⃣')
                await qmessage.add_reaction('❌')

                def check(reaction, user):
                    return (user == ctx.message.author and \
                    (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or \
                     str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or \
                     str(reaction.emoji) == '5️⃣' or str(reaction.emoji) == '❌') and \
                     reaction.message.id == qmessage.id)
                    
                try: 
                    reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = check) 
                except asyncio.TimeoutError:
                        await qmessage.delete()
                        await ctx.send('Sorting Quiz timed out. Be faster next time, pabo.')
                        return
                else:
                    if str(reaction.emoji) == '1️⃣':
                        houses[list(houses.keys())[int(nums[0]) - 1]] += 1
                    elif str(reaction.emoji) == '2️⃣':
                        houses[list(houses.keys())[int(nums[1]) - 1]] += 1
                    elif str(reaction.emoji) == '3️⃣':
                        houses[list(houses.keys())[int(nums[2]) - 1]] += 1
                    elif str(reaction.emoji) == '4️⃣':
                        houses[list(houses.keys())[int(nums[3]) - 1]] += 1
                    elif str(reaction.emoji) == '5️⃣':
                        houses[list(houses.keys())[int(nums[4]) - 1]] += 1
                    elif str(reaction.emoji) == '❌':
                        await qmessage.delete()
                        cancelled = await ctx.send('Sorting Quiz cancelled.')
                        await asyncio.sleep(10)
                        await cancelled.delete()
                        return

                await qmessage.delete()

            maximum = max(list(houses.values()))        
            result = [key for key, val in houses.items() if val == maximum]
            if len(result) > 1:
                ans = random.choice(result)
            else:
                ans = result[0]

            houseembed = discord.Embed(colour = discord.Colour(0xefe61))
            houseembed.set_author(name = f'You have been sorted into {ans.upper()} house! 🎉', 
            icon_url = f'{ctx.author.avatar_url}')

            housesdb = sql.connect('Houses.sqlite')
            hcursor = housesdb.cursor()
            hinsert = (f'INSERT INTO {ans}(UserID, IN_points) VALUES(?, ?)')
            hvalues = (ctx.author.id, 0)
            hcursor.execute(hinsert, hvalues)
            housesdb.commit()
            hcursor.close()
            housesdb.close()

            if ans == 'Pink':
                colour = 0xe985d5
                description = 'Pink is the house of winners. You have a competitive nature and a penchant for good RNG. \
People fear you, not just because you look cold and unapproachable, but because you can and will defeat them.'
                thumbnail = 'https://i.imgur.com/iA4AFBC.gif'
            elif ans == 'Yellow':
                colour = 0xfbe732
                description = 'Yellow is the house of kind souls. People often overlook you for your calm and demure nature, \
but deep down, you know you could beat them all if you set your mind to it.'
                thumbnail = 'https://imgur.com/MRRoloN.gif'
            elif ans == 'Blue':
                colour = 0x40a5f3
                description = "Blue is the house of achievers. It's not enough to just be book-smart; you must also be generous, \
amicable, and all-around a good person. You like making others laugh, even if it's at your own expense."
                thumbnail = 'https://imgur.com/sn1JDKX.gif'
            elif ans == 'Green':
                colour = 0x34b657
                description = "Green is the house of the cool kids. You ooze confidence, and people know you as being unashamedly \
and unapologetically you. But despite your image, when you're with close friends, you tend to let your sensitive side show."
                thumbnail = 'https://imgur.com/C4csOSB.gif'
            elif ans == 'Purple':
                colour = 0x923df9
                description = 'Purple is the house of social butterflies. You make friends wherever you go, and you prefer being \
with others rather than being alone. Social situations are where you thrive.'
                thumbnail = 'https://imgur.com/iSE4njP.gif'

            houseembed.colour = discord.Colour(colour)
            houseembed.description = description + f'\n\n`k.house {ans}` for more information about your house.'
            houseembed.set_thumbnail(url = thumbnail)
            houseembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            houseembed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = houseembed)

            cursor.execute(f'SELECT House FROM users WHERE UserID = {ctx.author.id}')
            insert = ('UPDATE users SET House = ? WHERE UserID = ?')
            values = (ans, ctx.author.id)
            cursor.execute(insert, values)

            db.commit()
            cursor.close()
            db.close()

            db = sql.connect('RPG.sqlite')
            cursor = db.cursor()
            insert = ('INSERT INTO users(UserID, XP, Rubies, HP, Weapon, Armor, Hpotions, Companion, Job) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)')
            values = (ctx.author.id, 0, 25, 100, 'None', 'None', 0, 'None', 'None')
            cursor.execute(insert, values)
            db.commit()
            cursor.close()
            db.close()

        else:
            await ctx.send('You have already been sorted into a house, pabo. No switching allowed.')

    @commands.command(aliases = ['Profile_rpg', 'rpg_profile', 'inventory', 'Inventory', 'inv', 'Inv'])
    async def profile_rpg(self, ctx, member: discord.Member = None):
        if member is None:
            user = ctx.author
        else:
            user = member

        if not profile_check(user.id):
            if user == ctx.author:
                await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            else:
                await ctx.send("This user doesn't have an RPG profile, pabo. Try again with someone else.")
            return
        if not house_check(user.id):
            if user == ctx.author:
                await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            else:
                await ctx.send("This user doesn't have a house, pabo. Try again with someone else.")
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE UserID = {user.id}')
        result = cursor.fetchall()
        weapon = result[0][4]
        armor = result[0][5]
        companion = result[0][7]

        attack = 0
        defense = 0
        if weapon != 'None':
            cursor.execute(f'SELECT Attack FROM market WHERE Name LIKE "{weapon}"')
            attack = cursor.fetchone()[0]
        if armor != 'None':
            cursor.execute(f'SELECT Defense FROM market WHERE Name LIKE "{armor}"')
            defense = cursor.fetchone()[0]
        if companion != 'None':
            cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{companion}"')
            companion_info = cursor.fetchall()[0]
            special = companion_info[5]

            if special == 'Attack':
                attack += companion_info[3]
            elif special == 'Defense':
                defense += companion_info[4]
            
        db.commit()
        cursor.close()
        db.close()

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT House FROM users WHERE UserID = {user.id}')
        house = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()

        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {user.id}')
        points = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()
        
        embed = discord.Embed(colour = discord.Colour(0xefe61))
        embed.set_author(name = f"{user.name}'s RPG Profile", icon_url = f'{user.avatar_url}')
        embed.set_thumbnail(url = user.avatar_url)
        embed.add_field(name = 'House:', value = house)
        embed.add_field(name = 'Points earned:', value = points)
        embed.add_field(name = 'XP:', value = result[0][1])
        embed.add_field(name = 'Rubies:', value = result[0][2])
        embed.add_field(name = 'HP:', value = result[0][3])
        embed.add_field(name = 'Weapon:', value = weapon)
        embed.add_field(name = 'Armor:', value = armor)
        embed.add_field(name = 'Attack:', value = attack)
        embed.add_field(name = 'Defense:', value = defense)
        embed.add_field(name = 'Health potions:', value = result[0][6])
        embed.add_field(name = 'Companion:', value = companion)
        embed.add_field(name = 'Job:', value = result[0][8])
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Guide', 'rpg', 'RPG'])
    async def guide(self, ctx):
        embed = discord.Embed(title = 'The Ultimate Guide to the Houses & RPG system', colour = discord.Colour(0xefe61),
        description = "**1.** Set up your profile using `k.profile_set`. You may customize your profile using \
`k.profile_bio [bio message]`, but this is entirely optional.\n\n\
**2.** Get sorted into a house with `k.get_sorted`. Afterwards, you can take a look at each of houses using \
`k.house [house name]`. The five different houses are: **Pink**, **Yellow**, **Blue**, **Green**, and **Purple**.\n\n\
**3.** View your updated profile (`k.profile`) as well as your RPG profile (`k.profile_rpg`). The entire RPG system is now yours \
to explore!\n\n\
**4.** Browse the market using `k.market`. Item info can be accessed using `k.item [item name]`. Items can be purchased using \
`k.buy [item name]` and sold using `k.sell [item name]`. If you already have a weapon/armor/companion, you must either sell it \
for rubies or dismantle it for house points (`k.dismantle [item name])` before purchasing another one.\n\n\
**5.** Explore the different jobs on the job board at the market \n\
(`k.item [job name]`), and apply for one that you're qualified for \n\
(`k.buy [job name]`). Afterwards, work a shift using `k.work`. Shifts can be worked every 8 hours. If you want to change your job, \
you must first leave your current one using `k.sell [job name]`.\n\n\
**6.** When you're ready, go on your first quest using `k.quest`. You can check your chances of survival using `k.quest_check`. \
To increase your chances, upgrade your weapons/armor/companion, and make sure you're fully healed by purchasing a \
health potion from the market and using it with `k.heal`. Quests can be done every 12 hours.\n\n\
**7.** Work towards the ultimate goal: winning the House Cup! For more info about the House Cup, check `k.house_cup`.")
        embed.set_thumbnail(url = 'https://imgur.com/VisvCB9.png')
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['House', 'house_info', 'House_info'])
    async def house(self, ctx, house = None):
        if house is None:
            await ctx.send('You must specify a house, pabo. Try again.')
            return

        house = house.lower().capitalize()
        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM {house} ORDER BY IN_points DESC;')
        result = cursor.fetchmany(3)
        cursor.execute(f'SELECT Count(*) FROM {house}')
        total = cursor.fetchone()[0]

        embed = discord.Embed(title = f'{house} House')
        
        if house == 'Pink':
            colour = 0xe985d5
            description = 'Pink is the house of winners. You have a competitive nature and a penchant for good RNG. \
People fear you, not just because you look cold and unapproachable, but because you can and will defeat them.'
            thumbnail = 'https://imgur.com/NRnQhgO.png'
        elif house == 'Yellow':
            colour = 0xfbe732
            description = 'Yellow is the house of kind souls. People often overlook you for your calm and demure nature, \
but deep down, you know you could beat them all if you set your mind to it.'
            thumbnail = 'https://imgur.com/gDiKLcZ.png'
        elif house == 'Blue':
            colour = 0x40a5f3
            description = "Blue is the house of achievers. It's not enough to just be book-smart; you must also be generous, \
amicable, and all-around a good person. You like making others laugh, even if it's at your own expense."
            thumbnail = 'https://imgur.com/6RRzdTf.png'
        elif house == 'Green':
            colour = 0x34b657
            description = "Green is the house of the cool kids. You ooze confidence, and people know you as being unashamedly \
and unapologetically you. But despite your image, when you're with close friends, you tend to let your sensitive side show."
            thumbnail = 'https://imgur.com/apid8O2.png'
        elif house == 'Purple':
            colour = 0x923df9
            description = 'Purple is the house of social butterflies. You make friends wherever you go, and you prefer being \
with others rather than being alone. Social situations are where you thrive.'
            thumbnail = 'https://imgur.com/QMsYrjP.png'

        embed.colour = discord.Colour(colour)
        embed.description = description
        embed.set_thumbnail(url = thumbnail)

        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT {house} FROM House_points')
        points = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()

        embed.add_field(name = 'House Points:', value = points)

        if total >= 3:
            embed.add_field(name = 'Top Members:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}\n\
                                                             2. **{self.bot.get_user(int(result[1][0]))}** - {result[1][1]}\n\
                                                             3. **{self.bot.get_user(int(result[2][0]))}** - {result[2][1]}')
        elif total == 2:
            embed.add_field(name = 'Top Members:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}\n\
                                                             2. **{self.bot.get_user(int(result[1][0]))}** - {result[1][1]}')
        elif total == 1:
            embed.add_field(name = 'Top Members:', value = f'1. **{self.bot.get_user(int(result[0][0]))}** - {result[0][1]}')
        elif total == 0:
            embed.add_field(name = 'Top Members:', value = 'None')

        embed.add_field(name = 'Member Count:', value = total)
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['House_ex', 'house_info_ex', 'House_info_ex'])
    async def house_ex(self, ctx):
        await ctx.send('```k.house Pink\n>>> [Information about Pink house]```')

    @commands.command(aliases = ['House_leaderboard', 'house_lb', 'House_lb'])
    async def house_leaderboard(self, ctx):
        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute('SELECT * FROM House_points')
        result = cursor.fetchall()[0]
        
        embed = discord.Embed(title = 'House Points', colour = discord.Colour(0xefe61),
        description = 'See `k.house_cup` for information about how to get points for your house, \
how to win the House Cup, and the prizes associated with winning.')
        embed.add_field(name = 'Pink:', value = result[0])
        embed.add_field(name = 'Yellow:', value = result[1])
        embed.add_field(name = 'Blue:', value = result[2])
        embed.add_field(name = 'Green:', value = result[3])
        embed.add_field(name = 'Purple:', value = result[4])
        embed.set_thumbnail(url = 'https://imgur.com/vCSdbvP.png')
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['House_cup', 'housecup', 'Housecup'])
    async def house_cup(self, ctx):
        embed = discord.Embed(title = 'The House Cup', colour = discord.Colour(0xefe61),
        description = f"There are **5** ways of getting points for your house:\n\n\
**1.** Win a round of Hunger Games (20 points)\n\
**2.** Complete quests\n\
**3.** Dismantle weapons/armor\n\
**4.** Convert rubies to house points\n\
**5.** Impress the Headmaster, <@!496181635952148483>\n\n\
After a set amount of time, the house with the most points wins the House Cup, an honour greater than receiving a \
Nobel Peace Prize. 100% legit. In addition, members of the winning house will get their house colour showcased in \
Kaisercord for 3 days, and the top three members will receive an extra special role for 7 days.")
        embed.set_thumbnail(url = 'https://imgur.com/vCSdbvP.png')
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Market', 'shop', 'Shop', 'store', 'Store'])
    async def market(self, ctx):
        embed = discord.Embed(title = 'RPG - Market', colour = discord.Colour(0xefe61), 
        description = '`k.item [item name]` : purchase price and info for each item\n\
            `k.item weapons` : compare prices/stats across all weapons\n\
            `k.item armor` : compare prices/stats across all armor')
        embed.set_thumbnail(url = 'https://imgur.com/sgINvsZ.png')

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()

        d = {}
        
        for i in [1, 2, 3, 4, 5]:  
            cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "weapon_{i}"')
            d[f'weapon_{i}'] = cursor.fetchall()
        for i in [1, 2, 3, 4, 5]:  
            cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "armor_{i}"')
            d[f'armor_{i}'] = cursor.fetchall()
        cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "companion"')
        d['companion'] = cursor.fetchall()
        cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "miscellaneous"')
        d['miscellaneous'] = cursor.fetchall()
        cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "job"')
        d['job'] = cursor.fetchall()

        w_t1 = ', '.join(list(map(lambda x: x[0], d['weapon_1'])))
        w_t2 = ', '.join(list(map(lambda x: x[0], d['weapon_2'])))
        w_t3 = ', '.join(list(map(lambda x: x[0], d['weapon_3'])))
        w_t4 = ', '.join(list(map(lambda x: x[0], d['weapon_4'])))
        w_t5 = ', '.join(list(map(lambda x: x[0], d['weapon_5'])))

        a_t1 = ', '.join(list(map(lambda x: x[0], d['armor_1'])))
        a_t2 = ', '.join(list(map(lambda x: x[0], d['armor_2'])))
        a_t3 = ', '.join(list(map(lambda x: x[0], d['armor_3'])))
        a_t4 = ', '.join(list(map(lambda x: x[0], d['armor_4'])))
        a_t5 = ', '.join(list(map(lambda x: x[0], d['armor_5'])))

        c = ', '.join(list(map(lambda x: x[0], d['companion'])))
        m = ', '.join(list(map(lambda x: x[0], d['miscellaneous'])))
        j = ', '.join(list(map(lambda x: x[0], d['job'])))

        embed.add_field(name = 'Blacksmith:', value = f'**Tier 1:** {w_t1}\n\
                                                        **Tier 2:** {w_t2}\n\
                                                        **Tier 3:** {w_t3}\n\
                                                        **Tier 4:** {w_t4}\n\
                                                        **Tier 5:** {w_t5}',
                                                        inline = False)
        embed.add_field(name = 'Armorer:', value = f'**Tier 1:** {a_t1}\n\
                                                        **Tier 2:** {a_t2}\n\
                                                        **Tier 3:** {a_t3}\n\
                                                        **Tier 4:** {a_t4}\n\
                                                        **Tier 5:** {a_t5}',
                                                        inline = False)
        embed.add_field(name = 'Breeder:', value = c, inline = False)
        embed.add_field(name = 'Mage:', value = m, inline = False)
        embed.add_field(name = 'Job Board:', value = j, inline = False)
        
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Item', 'item_info', 'Item_info'])
    async def item(self, ctx, *, item = None):
        if item is None:
            await ctx.send('You need to specify an item, pabo. Try again.')
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()

        if item.lower() == 'weapons' or item.lower() == 'weapon':
            d = {}
            for i in [1, 2, 3, 4, 5]:  
                cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "weapon_{i}"')
                names = list(map(lambda x: x[0], cursor.fetchall()))
                cursor.execute(f'SELECT Price FROM market WHERE Class LIKE "weapon_{i}"')
                prices = list(map(lambda x: x[0], cursor.fetchall()))
                cursor.execute(f'SELECT Attack FROM market WHERE Class LIKE "weapon_{i}"')
                stats = list(map(lambda x: x[0], cursor.fetchall()))

                L = []
                for j in [0, 1, 2, 3, 4]:
                    L.append(f'*{names[j]}* - {prices[j]} - {stats[j]}')

                d[f'weapon_{i}'] = L

            db.commit()
            cursor.close()
            db.close()
            
            w_t1 = '\n'.join(d['weapon_1'])
            w_t2 = '\n'.join(d['weapon_2'])
            w_t3 = '\n'.join(d['weapon_3'])
            w_t4 = '\n'.join(d['weapon_4'])
            w_t5 = '\n'.join(d['weapon_5'])

            wembed = discord.Embed(title = 'RPG - Market - Weapons', colour = discord.Colour(0xefe61),
            description = '`[Weapon name] - [Price] - [Attack damage]`')
            wembed.add_field(name = 'Tier 1:', value = w_t1)
            wembed.add_field(name = 'Tier 2:', value = w_t2)
            wembed.add_field(name = 'Tier 3:', value = w_t3)
            wembed.add_field(name = 'Tier 4:', value = w_t4)
            wembed.add_field(name = 'Tier 5:', value = w_t5)
            wembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            wembed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = wembed)
            return

        elif item.lower() == 'armor':
            d = {}
            for i in [1, 2, 3, 4, 5]:  
                cursor.execute(f'SELECT Name FROM market WHERE Class LIKE "armor_{i}"')
                names = list(map(lambda x: x[0], cursor.fetchall()))
                cursor.execute(f'SELECT Price FROM market WHERE Class LIKE "armor_{i}"')
                prices = list(map(lambda x: x[0], cursor.fetchall()))
                cursor.execute(f'SELECT Defense FROM market WHERE Class LIKE "armor_{i}"')
                stats = list(map(lambda x: x[0], cursor.fetchall()))

                L = []
                for j in [0, 1, 2]:
                    L.append(f'*{names[j]}* - {prices[j]} - {stats[j]}')

                d[f'armor_{i}'] = L

            db.commit()
            cursor.close()
            db.close()
            
            a_t1 = '\n'.join(d['armor_1'])
            a_t2 = '\n'.join(d['armor_2'])
            a_t3 = '\n'.join(d['armor_3'])
            a_t4 = '\n'.join(d['armor_4'])
            a_t5 = '\n'.join(d['armor_5'])

            aembed = discord.Embed(title = 'RPG - Market - Armor', colour = discord.Colour(0xefe61),
            description = '`[Armor name] - [Price] - [Defense]`')
            aembed.add_field(name = 'Tier 1:', value = a_t1)
            aembed.add_field(name = 'Tier 2:', value = a_t2)
            aembed.add_field(name = 'Tier 3:', value = a_t3)
            aembed.add_field(name = 'Tier 4:', value = a_t4)
            aembed.add_field(name = 'Tier 5:', value = a_t5)
            aembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            aembed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = aembed)
            return

        if not item_check(item):
            await ctx.send('Item not found, pabo. Try again.')
            return
        
        cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{item}"')
        result = cursor.fetchall()[0]

        item_title = string.capwords(item)
        embed = discord.Embed(title = f'RPG - Item Info - {item_title}', colour = discord.Colour(0xefe61), 
        description = 'Description')

        category = result[1]

        if category[0] == 'w':
            attack = result[3]
            embed.description = 'Weapons allow you to do more attack damage, which increases your chances of \
success on quests. The higher the tier of the weapon, the higher the damage. Weapons across the same tier share \
similar prices and stats.\n\n\
Before purchasing a new weapon, your current weapon must be either sold \n\
(`k.sell [item name]`) for rubies or dismantled (`k.dismantle [item name]`) \n\
for house points.'
            embed.add_field(name = 'Class:', value = f'Weapon - Tier {category[-1]}')
            embed.add_field(name = 'Attack:', value = attack)
        elif category[0] == 'a':
            defense = result[4]
            embed.description = 'Armor builds up your defense, which increases your chances of success on quests. \
The higher the tier of the armor, the higher the defense. Armor across the same tier share similar prices and stats.\n\n\
Before purchasing new armor, your current armor must be either sold \n\
(`k.sell [item name]`) for rubies or dismantled (`k.dismantle [item name]`) \n\
for house points.'
            embed.add_field(name = 'Class:', value = f'Armor - Tier {category[-1]}')
            embed.add_field(name = 'Defense:', value = defense)
        elif category[0] == 'c':
            special = result[5]
            embed.description = 'Companions provide a special ability: attack, defense, looting, or revive.\n\
- **Attack:** increases attack damage by **25** points\n\
- **Defense:** increases defense by **25** points\n\
- **Looting:** increases chance of earning loot on quests\n\
- **Revive:** revives you if you die on a quest (single-use)\n\n\
Before purchasing a new companion, your current companion must be sold \n\
(`k.sell [item name]`) for rubies.'
            embed.add_field(name = 'Class:', value = 'Companion')
            embed.add_field(name = 'Special:', value = f'{special}')
        elif category[0] == 'm':
            special= result[5]
            embed.description = '**Health potion:** fully restores your health to 100 HP\n\
                                 **House points:** 20 rubies -> 1 point'
            embed.add_field(name = 'Class:', value = 'Miscellaneous')
            embed.add_field(name = 'Special:', value = f'{special}')
        elif category[0] == 'j':
            special = result[5]
            embed.description = 'Jobs provide a secure source of income. To obtain a job, you must have a sufficient amount \
of XP, as well as enough rubies to pay the application fee. Higher-paying jobs require more XP and have a higher application \
fee. After obtaining a job, shifts can be worked every 8 hours (`k.work`).\n\n\
Before applying for a new job, you must leave your current job (`k.sell [job name]`).'
            embed.add_field(name = 'Class:', value = 'Job')
            embed.add_field(name = 'Special:', value = f'{special} rubies / shift')

        price = result[2]
        if category[0] != 'j':
            embed.add_field(name = 'Price:', value = f'{price} rubies')
        else:
            embed.add_field(name = 'Price:', value = f'Minimum of {price} XP\nApplication fee of {price} rubies')

        db.commit()
        cursor.close()
        db.close()

        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Item_ex', 'item_info_ex', 'Item_info_ex'])
    async def item_ex(self, ctx):
        await ctx.send('```k.item [Item name]\n>>> [Retrieves information about the specified item]```')

    @commands.command(aliases = ['Buy', 'purchase', 'Purchase'])
    async def buy(self, ctx, *, item = None):
        if not profile_check(ctx.author.id):
            await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            return
        if not house_check(ctx.author.id):
            await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            return
        if item is None:
            await ctx.send('You must specify an item to buy, pabo. Try again.')
            return
        if not item_check(item):
            await ctx.send('Item not found, pabo. Try again.')
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{item}"')
        buy_item = cursor.fetchall()
        buy_item = buy_item[0]
        name = buy_item[0]
        category = buy_item[1]
        price = buy_item[2]
        
        cursor.execute(f'SELECT * FROM users WHERE UserID = {ctx.author.id}')
        user_info = cursor.fetchall()[0]
        rubies = user_info[2]
        weapon = user_info[4]
        armor = user_info[5]
        hps = user_info[6]
        companion = user_info[7]
        job = user_info[8]
        xp = user_info[1]

        if rubies < price:
            db.commit()
            cursor.close()
            db.close()
            await ctx.send("You are too poor to purchase this item, pabo. Get some more rubies and come back.")
            return

        quantity = 1
        if category[0] == 'w':
            if weapon == 'None':
                insert = (f'UPDATE users SET Weapon = ? WHERE UserID = ?')
                values = (name, ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'⚔ Purchased a **{item.lower()}** for {price} rubies.')
            else:
                await ctx.send('You already have a weapon, pabo. Either sell it or dismantle it before you purchase another one.')
                db.commit()
                cursor.close()
                db.close()
                return

        elif category[0] == 'a':
            if armor == 'None':
                insert = (f'UPDATE users SET Armor = ? WHERE UserID = ?')
                values = (name, ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'🛡️ Purchased a **{item.lower()}** for {price} rubies.')
            else:
                await ctx.send('You already have armor, pabo. Either sell it or dismantle it before you purchase another one.')
                db.commit()
                cursor.close()
                db.close()
                return

        elif category[0] == 'c':
            if companion == 'None':
                insert = (f'UPDATE users SET Companion = ? WHERE UserID = ?')
                values = (name, ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'🐕 Purchased a **{item.lower()}** for {price} rubies. You have gained a new companion!')
            else:
                await ctx.send('You already have a companion, pabo. Sell it before you purchase another one.')
                db.commit()
                cursor.close()
                db.close()
                return

        elif category[0] == 'm':
            if item.lower() == 'health potion':
                item = 'health potions'

            quantityembed = discord.Embed(title = 'RPG - Market - Mage', colour = discord.Colour(0xefe61), 
            description = f"**Mage:** Good day, brave adventurer! What quantity of {item.lower()} would you like to purchase?")
            quantityembed.set_thumbnail(url = 'https://imgur.com/sgINvsZ.png')
            quantityembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            quantityembed.timestamp = datetime.datetime.utcnow()
            quantitymessage = await ctx.send(embed = quantityembed)

            await quantitymessage.add_reaction('1️⃣')
            await quantitymessage.add_reaction('2️⃣')
            await quantitymessage.add_reaction('3️⃣')
            await quantitymessage.add_reaction('4️⃣')
            await quantitymessage.add_reaction('5️⃣')
            await quantitymessage.add_reaction('❌')

            def check(reaction, user):
                return (user == ctx.message.author and \
                    (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or \
                    str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or \
                    str(reaction.emoji) == '5️⃣' or str(reaction.emoji) == '❌') and \
                    reaction.message.id == quantitymessage.id)
                
            try: 
                reaction, user = await self.bot.wait_for('reaction_add', timeout = 120, check = check) 
            except asyncio.TimeoutError:
                db.commit()
                cursor.close()
                db.close()
                await quantitymessage.delete()
                await ctx.send('Buy item timed out. Be faster next time, pabo.')
                return
            else:
                if str(reaction.emoji) == '1️⃣':
                    quantity = 1
                elif str(reaction.emoji) == '2️⃣':
                    quantity = 2
                elif str(reaction.emoji) == '3️⃣':
                    quantity = 3
                elif str(reaction.emoji) == '4️⃣':
                    quantity = 4
                elif str(reaction.emoji) == '5️⃣':
                    quantity = 5
                elif str(reaction.emoji) == '❌':
                    db.commit()
                    cursor.close()
                    db.close()
                    await quantitymessage.delete()
                    cancelled = await ctx.send('Buy item cancelled.')
                    await asyncio.sleep(10)
                    await cancelled.delete()
                    return

            await quantitymessage.delete()

            if rubies < (price * quantity):
                db.commit()
                cursor.close()
                db.close()
                await ctx.send("You are too poor to purchase this item, pabo. Get some more rubies and come back.")
                return

            if item == 'health potions':
                insert = (f'UPDATE users SET Hpotions = ? WHERE UserID = ?')
                updated = hps + quantity
                values = (updated, ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'🍷 Purchased **{quantity} {item.lower()}** for {price * quantity} rubies.')
            elif item == 'house points':
                pdb = sql.connect('Profiles.sqlite')
                pcursor = pdb.cursor()
                pcursor.execute(f'SELECT House FROM users WHERE UserID = {ctx.author.id}')
                house = pcursor.fetchone()[0].lower().capitalize()
                pdb.commit()
                pcursor.close()
                pdb.close()

                hdb = sql.connect('Houses.sqlite')
                hcursor = hdb.cursor()
                hcursor.execute(f'SELECT {house} FROM House_points')
                updated = hcursor.fetchone()[0] + quantity
                insert = (f'UPDATE House_points SET {house} = ?')
                values = (updated,)
                hcursor.execute(insert, values)
                hcursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {ctx.author.id}')
                INupdated = hcursor.fetchone()[0] + quantity
                INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
                INvalues = (INupdated, ctx.author.id)
                hcursor.execute(INinsert, INvalues)
                hdb.commit()
                hcursor.close()
                hdb.close()
                await ctx.send(f'💎 Purchased **{quantity} {item.lower()}** for {price * quantity} rubies.')

        elif category[0] == 'j':
            if xp < price:
                await ctx.send("You don't have enough XP to hold this job, pabo. Come back later.")
            if job == 'None':
                insert = (f'UPDATE users SET Job = ? WHERE UserID = ?')
                values = (item.capitalize(), ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'⚒ After paying a job application fee of **{price}** rubies, you are now a **{item.lower()}**!')
            else:
                await ctx.send('You already have a job, pabo. Leave it before you apply for another one.')
                db.commit()
                cursor.close()
                db.close()
                return

        insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
        updated = rubies - price * quantity
        values = (updated, ctx.author.id)
        cursor.execute(insert, values)

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases = ['Buy_ex', 'purchase_ex', 'Purchase_ex'])
    async def buy_ex(self, ctx):
        await ctx.send('```k.buy [Item name]\n>>> [Purchases the specified item]```')

    @commands.command(aliases = ['Sell', 'sold', 'Sold'])
    async def sell(self, ctx, *, item = None):
        if not profile_check(ctx.author.id):
            await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            return
        if not house_check(ctx.author.id):
            await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            return
        if item is None:
            await ctx.send('You must specify an item to sell, pabo. Try again.')
            return
        if not item_check(item):
            await ctx.send('Item not found, pabo. Try again.')
            return
        if item == 'house points':
            await ctx.send("You can't sell house points, pabo. Try again.")
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{item}"')
        sell_item = cursor.fetchall()
        sell_item = sell_item[0]
        name = sell_item[0]
        category = sell_item[1]
        price = sell_item[2]
        
        cursor.execute(f'SELECT * FROM users WHERE UserID = {ctx.author.id}')
        user_info = cursor.fetchall()[0]
        rubies = user_info[2]
        weapon = user_info[4]
        armor = user_info[5]
        hps = user_info[6]
        companion = user_info[7]
        job = user_info[8]

        if category[0] == 'w':
            if weapon == 'None' or weapon != name:
                await ctx.send("You can't sell something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Weapon = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'⚔ Sold your **{item.lower()}** for {price // 2} rubies. You are now free to purchase a new weapon!')

        elif category[0] == 'a':
            if armor == 'None' or armor != name:
                await ctx.send("You can't sell something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Armor = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'🛡️ Sold your **{item.lower()}** for {price // 2} rubies. You are now free to purchase new armor!')

        elif category[0] == 'c':
            if companion == 'None' or companion != name:
                await ctx.send("You can't sell something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Companion = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f"🐕 Sold your **{item.lower()}** for {price // 2} rubies. You'll miss him/her. :pensive:")

        elif category[0] == 'm':
            if hps == 0:
                await ctx.send("You can't sell something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Hpotions = ? WHERE UserID = ?')
                updated = hps - 1
                values = (updated, ctx.author.id)
                cursor.execute(insert, values)
                await ctx.send(f'🍷 Sold a **{item.lower()}** for {price // 2} rubies.')

        elif category[0] == 'j':
            if job.lower() != item.lower():
                await ctx.send("You can't retire from a job you don't have, pabo. Try again.")
            else:
                insert = (f'UPDATE users SET Job = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)

                insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
                updated = rubies + price // 2
                values = (updated, ctx.author.id)
                cursor.execute(insert, values)

                await ctx.send(f'⚒ You are now unemployed! You also received a severance package of **{price // 2}** rubies!')

            db.commit()
            cursor.close()
            db.close()
            return

        insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
        updated = rubies + price // 2
        values = (updated, ctx.author.id)
        cursor.execute(insert, values)

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases = ['Sell_ex', 'sold_ex', 'Sold_ex'])
    async def sell_ex(self, ctx):
        await ctx.send('```k.sell [Item name]\n>>> [Sells the specified item]```')

    @commands.command(aliases = ['Dismantle', 'destroy', 'Destroy', 'disassemble', 'Disassemble'])
    async def dismantle(self, ctx, *, item = None):
        if not profile_check(ctx.author.id):
            await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            return
        if not house_check(ctx.author.id):
            await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            return
        if item is None:
            await ctx.send('You must specify an item to dismantle, pabo. Try again.')
            return
        if not item_check(item):
            await ctx.send('Item not found, pabo. Try again.')
            return

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT House FROM users WHERE UserID = {ctx.author.id}')
        house = cursor.fetchone()[0]
        db.commit()
        cursor.close()
        db.close()

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{item}"')
        dis_item = cursor.fetchall()
        dis_item = dis_item[0]
        name = dis_item[0]
        category = dis_item[1]
        
        cursor.execute(f'SELECT * FROM users WHERE UserID = {ctx.author.id}')
        user_info = cursor.fetchall()[0]
        weapon = user_info[4]
        armor = user_info[5]

        if category[0] == 'w':
            if weapon == 'None' or weapon != name:
                await ctx.send("You can't dismantle something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Weapon = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f'⚔ Dismantled your **{item.lower()}** for **{int(category[-1]) ** 2}** points to **{house}** house! \
You are now free to purchase a new weapon.')

        elif category[0] == 'a':
            if armor == 'None' or armor != name:
                await ctx.send("You can't dismantle something you don't own, pabo. Try again.")
                db.commit()
                cursor.close()
                db.close()
                return
            else:
                insert = (f'UPDATE users SET Armor = ? WHERE UserID = ?')
                values = ('None', ctx.author.id)
                cursor.execute(insert, values)
                db.commit()
                cursor.close()
                db.close()
                await ctx.send(f'🛡️ Dismantled your **{item.lower()}** for **{int(category[-1]) ** 2}** points to **{house}** house! \
You are now free to purchase new armor.')

        elif category[0] == 'c' or category[0] == 'j' or category[0] == 'm':
            await ctx.send("You can't dismantle this item, pabo. Try again.")
            db.commit()
            cursor.close()
            db.close()
            return

        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT {house} FROM House_points')
        updated = cursor.fetchone()[0] + (int(category[-1]) ** 2)
        insert = (f'UPDATE House_points SET {house} = ?')
        values = (updated,)
        cursor.execute(insert, values)

        cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {ctx.author.id}')
        INupdated = cursor.fetchone()[0] + (int(category[-1]) ** 2)
        INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
        INvalues = (INupdated, ctx.author.id)
        cursor.execute(INinsert, INvalues)

        db.commit()
        cursor.close()
        db.close()

    @commands.command(aliases = ['Dismantle_ex', 'destroy_ex', 'Destroy_ex', 'disassemble_ex', 'Disassemble_ex'])
    async def dismantle_ex(self, ctx):
        await ctx.send('```k.dismantle [Item name]\n>>> [Dismantles the specified item]```')

    @commands.command(aliases = ['Quest', 'loot', 'Loot'])
    @commands.cooldown(1, 43200, commands.BucketType.user)
    async def quest(self, ctx):
        if not profile_check(ctx.author.id):
            self.bot.get_command('quest').reset_cooldown(ctx)
            await ctx.send('Please create a profile (`k.profile_set`) before attempting to loot.')
            return
        if not house_check(ctx.author.id):
            self.bot.get_command('quest').reset_cooldown(ctx)
            await ctx.send('Please set your house (`k.get_sorted`) before attempting to loot, pabo.')
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE UserID = {ctx.author.id}')
        user_info = cursor.fetchall()[0]
        health = user_info[3]
        weapon = user_info[4]
        armor = user_info[5]
        companion = user_info[7]

        attack = 0
        defense = 0
        loot_bonus = False
        comp_bonus = 0
        revive = False
        if weapon != 'None':
            cursor.execute(f'SELECT Attack FROM market WHERE Name LIKE "{weapon}"')
            attack = cursor.fetchone()[0]
        if armor != 'None':
            cursor.execute(f'SELECT Defense FROM market WHERE Name LIKE "{armor}"')
            defense = cursor.fetchone()[0]
        if companion != 'None':
            cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{companion}"')
            companion_info = cursor.fetchall()[0]
            special = companion_info[5]
            if special == 'Attack':
                attack += companion_info[3]
            elif special == 'Defense':
                defense += companion_info[4]
            elif special == 'Looting':
                loot_bonus = True
                comp_bonus = 10
            elif special == 'Revive':
                revive = True

        quest_attack1 = 10
        quest_defense1 = 10
        quest_attack2 = 30
        quest_defense2 = 30
        quest_attack3 = 50
        quest_defense3 = 50
        quest_attack4 = 75
        quest_defense4 = 75
        health_chance1 = 60
        health_chance2 = 80
        health_chance3 = 100
        health_chance4 = 150

        health_chance1 = health / health_chance1 * 0.1
        attack_chance1 = attack / quest_attack1 * 0.45
        defense_chance1 = defense / quest_defense1 * 0.45
        avg1 = (attack_chance1 + defense_chance1 + health_chance1)  * 100

        health_chance2 = health / health_chance2 * 0.1
        attack_chance2 = attack / quest_attack2 * 0.45
        defense_chance2 = defense / quest_defense2 * 0.45
        avg2 = (attack_chance2 + defense_chance2 + health_chance2)  * 100

        health_chance3 = health / health_chance3 * 0.1
        attack_chance3 = attack / quest_attack3 * 0.45
        defense_chance3 = defense / quest_defense3 * 0.45
        avg3 = (attack_chance3 + defense_chance3 + health_chance3)  * 100

        health_chance4 = health / health_chance4 * 0.1
        attack_chance4 = attack / quest_attack4 * 0.45
        defense_chance4 = defense / quest_defense4 * 0.45
        avg4 = (attack_chance4 + defense_chance4 + health_chance4)  * 100

        if avg1 >= 100:
            avg1 = 100
        if avg2 >= 100:
            avg2 = 100
        if avg3 >= 100:
            avg3 = 100
        if avg4 >= 100:
            avg4 = 100

        chooseembed = discord.Embed(title = 'RPG - Quest Picker', colour = discord.Colour(0xefe61), 
        description = f"Be careful! If you die, you lose *everything*.\n\n\
                       **Attack:** {attack}\n**Defense:** {defense}")
        chooseembed.set_thumbnail(url = 'https://imgur.com/zXZtR0U.png')
        chooseembed.add_field(name = 'Quest 1 - Difficulty: Newcomer', 
        value = f'Recommended: Attack: **{quest_attack1}**, Defense: **{quest_defense1}** \n\
                  Chance of survival: **{avg1:.2f}%**',
        inline = False)
        chooseembed.add_field(name = 'Quest 2 - Difficulty: Adventurer', 
        value = f'Recommended: Attack: **{quest_attack2}**, Defense: **{quest_defense2}** \n\
                  Chance of survival: **{avg2:.2f}%**',
        inline = False)
        chooseembed.add_field(name = 'Quest 3 - Difficulty: Experienced', 
        value = f'Recommended: Attack: **{quest_attack3}**, Defense: **{quest_defense3}** \n\
                  Chance of survival: **{avg3:.2f}%**',
        inline = False)
        chooseembed.add_field(name = 'Boss Battle - Difficulty: Professional', 
        value = f'Recommended: Attack: **{quest_attack4}**, Defense: **{quest_defense4}** \n\
                  Chance of survival: **{avg4:.2f}%**',
        inline = False)
        chooseembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        chooseembed.timestamp = datetime.datetime.utcnow()

        choosemessage = await ctx.send(embed = chooseembed)
        await choosemessage.add_reaction('1️⃣')
        await choosemessage.add_reaction('2️⃣')
        await choosemessage.add_reaction('3️⃣')
        await choosemessage.add_reaction('4️⃣')
        await choosemessage.add_reaction('❌')

        def check(reaction, user):
            return (user == ctx.message.author and \
            (str(reaction.emoji) == '1️⃣' or str(reaction.emoji) == '2️⃣' or \
            str(reaction.emoji) == '3️⃣' or str(reaction.emoji) == '4️⃣' or \
            str(reaction.emoji) == '❌') and \
            reaction.message.id == choosemessage.id)
                    
        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = check) 
        except asyncio.TimeoutError:
            db.commit()
            cursor.close()
            db.close()
            await choosemessage.delete()
            await ctx.send('RPG Quest timed out. Be faster next time, pabo.')
            return
        else:
            points_bonus = 0
            if str(reaction.emoji) == '1️⃣':
                avg = avg1
                quest_loot_bonus = 0
            elif str(reaction.emoji) == '2️⃣':
                avg = avg2
                quest_loot_bonus = 5
            elif str(reaction.emoji) == '3️⃣':
                avg = avg3
                quest_loot_bonus = 15
            elif str(reaction.emoji) == '4️⃣':
                avg = avg4
                quest_loot_bonus = 40
                points_bonus = 10
            elif str(reaction.emoji) == '❌':
                db.commit()
                cursor.close()
                db.close()
                self.bot.get_command('quest').reset_cooldown(ctx)
                await choosemessage.delete()
                cancelled = await ctx.send('RPG Quest cancelled.')
                await asyncio.sleep(10)
                await cancelled.delete()
                return

        await choosemessage.delete()

        phoenix_death = ''

        avg /= 100
        if avg >= 1:
            lost_HP_bonus = 0
        else:
            if random.randint(1, 100) >= (avg * 100):
                if revive:
                    insert = (f'UPDATE users SET Companion = ? WHERE UserID = ?')
                    values = ('None', ctx.author.id)
                    cursor.execute(insert, values)
                    phoenix_death = 'Unfortunately, your phoenix died reviving you.'
                else:
                    cursor.execute(f'SELECT XP FROM users WHERE UserID = {ctx.author.id}')
                    xp = cursor.fetchone()[0]
                    saved = xp // 10
                    cursor.execute(f'UPDATE users SET XP = 0 WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Rubies = {saved} WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET HP = 100 WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Weapon = "None" WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Armor = "None" WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Hpotions = 0 WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Companion = "None" WHERE UserID = {ctx.author.id}')
                    cursor.execute(f'UPDATE users SET Job = "None" WHERE UserID = {ctx.author.id}')
                    db.commit()
                    cursor.close()
                    db.close()
                    await ctx.send('Unfortunately, you were insufficiently prepared for this quest and died.')
                    return

            lost_HP_bonus = (100 - (avg * 100)) // 2

        items = {'tier_1': ['Wooden cup', 'Stone goblet', 'Kindling', 'Leather scraps', 'Twine', 'Parchment', 
                            'Firewood', 'Stale bread', 'Cotton seeds'],
                 'tier_2': ['Steel plates', 'Broken blade', 'Broken shield', 'Shovel', 'Gunpowder', 
                            'Dried fruit', 'Beef jerky', 'Canned soup', 'Oil', 'Spices', 'Flint'],
                 'tier_3': ['Diamond necklace', 'Golden locket', 'Bejeweled goblet', 'Dragon scales', 'Unicorn horn'],
                 'HP': None}

        looted = {}

        cursor.execute(f'SELECT HP FROM users WHERE UserID = {ctx.author.id}')
        current_HP = cursor.fetchone()[0]
        lost_HP = random.randint(0, current_HP // 3) + lost_HP_bonus
        updated =  current_HP - lost_HP
        if updated <= 0:
            updated = 1
            lost_HP = current_HP - 1
        insert = ('UPDATE users SET HP = ? WHERE UserID = ?')
        values = (updated, ctx.author.id)
        cursor.execute(insert, values)
            
        if loot_bonus or random.randint(1, 100) <= 90:
            rubies_loot = True
        else: 
            rubies_loot = False
        if rubies_loot:
            loot_rubies = random.randint(1 + comp_bonus + quest_loot_bonus, 25 + comp_bonus + quest_loot_bonus) 
            looted['rubies'] = f'{loot_rubies} rubies' 
            cursor.execute(f'SELECT Rubies FROM users WHERE UserID = {ctx.author.id}')
            updated = cursor.fetchone()[0] + loot_rubies
            insert = ('UPDATE users SET Rubies = ? WHERE UserID = ?')
            values = (updated, ctx.author.id)
            cursor.execute(insert, values)

        if loot_bonus or random.randint(1, 100) <= 80:
            xp_loot = True
        else: 
            xp_loot = False
        if xp_loot:
            loot_xp = random.randint(1 + comp_bonus + quest_loot_bonus, 25 + comp_bonus + quest_loot_bonus) 
            looted['xp'] = f'{loot_xp} XP' 
            cursor.execute(f'SELECT XP FROM users WHERE UserID = {ctx.author.id}')
            updated = cursor.fetchone()[0] + loot_xp
            insert = ('UPDATE users SET XP = ? WHERE UserID = ?')
            values = (updated, ctx.author.id)
            cursor.execute(insert, values)

        if random.randint(1, 100) <= (70 + comp_bonus + quest_loot_bonus):
            looted['t1'] = random.choice(items['tier_1'])
        if random.randint(1, 100) <= (50  + comp_bonus + quest_loot_bonus):
            looted['t2'] = random.choice(items['tier_2'])
        if random.randint(1, 100) <= (25  + comp_bonus + quest_loot_bonus):
            loot_points = random.randint(1 + points_bonus, 10 + points_bonus)
            looted['points'] = f'{loot_points} house points'
        if random.randint(1, 100) <= (10  + comp_bonus + quest_loot_bonus):
            looted['HP'] = '1 health potion'
        if random.randint(1, 100) <= (5  + comp_bonus + quest_loot_bonus):
            looted['t3'] = random.choice(items['tier_3'])

        lootlist = list(looted.values())

        if len(lootlist) == 0:
            unlucky = ':pensive: Somehow, you got incredibly unlucky and found nothing.'
            if lost_HP != 0:
                unlucky += f' You also lost {lost_HP} HP on your journey. Sucks for you.'
            await ctx.send(unlucky)
            db.commit()
            cursor.close()
            db.close()
            return
            
        embed1 = discord.Embed(title = "RPG - Quest - Looting", colour = discord.Colour(0xefe61),
        description = f'You break into an ancient tomb and fight off a few foes, looting whatever chests you encounter along the way. \
You find **{len(lootlist)}** items in total and lose **{int(lost_HP)}** HP along the way. ' + phoenix_death)
        embed1.set_thumbnail(url = 'https://imgur.com/zXZtR0U.png')

        for i in list(range(len(lootlist))):
            embed1.add_field(name = '\u200b', value = f'- {lootlist[i]}', inline = False)

        embed1.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed1.timestamp = datetime.datetime.utcnow()

        startmessage = await ctx.send(embed = embed1)

        if 't1' not in list(looted.keys()) and 't2' not in list(looted.keys()) and 't3' not in list(looted.keys()):
            await startmessage.delete()
            db.commit()
            cursor.close()
            db.close()
            return

        await startmessage.add_reaction('▶️')

        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = lambda reaction, 
            user: (str(reaction.emoji) == '▶️' and user == ctx.author and reaction.message.id == startmessage.id))
        except asyncio.TimeoutError:
            await startmessage.delete()
            await ctx.send('Looting timed out. Remaining processes completed automatically. Be faster next time, pabo.')
            db.commit()
            cursor.close()
            db.close()
            return
        else:
            if str(reaction.emoji) == '▶️':

                embed2 = discord.Embed(title = 'RPG - Quest - Market', colour = discord.Colour(0xefe61), 
                description = 'Hauling along your spoils, you make it to a nearby market and barter with the merchants.')
                embed2.set_thumbnail(url = 'https://imgur.com/sgINvsZ.png')

                sold_rubies = 0
                if 't1' in list(looted.keys()):
                    t1_rubies = random.randint(1, 10)
                    sold_rubies = t1_rubies
                    embed2.add_field(name = '\u200b', 
                    value = f"- Sold **{looted['t1'].lower()}** for **{t1_rubies}** rubies", 
                    inline = False)

                if 't2' in list(looted.keys()):
                    t2_rubies = random.randint(20, 35)
                    sold_rubies += t2_rubies
                    embed2.add_field(name = '\u200b', 
                    value = f"- Sold **{looted['t2'].lower()}** for **{t2_rubies}** rubies",
                    inline = False)
                    
                if 't3' in list(looted.keys()):
                    t3_rubies = random.randint(50, 75)
                    sold_rubies += t3_rubies
                    embed2.add_field(name = '\u200b', 
                    value = f"- Sold **{looted['t3'].lower()}** for **{t3_rubies}** rubies",
                    inline = False)
                
                if 'HP' in list(looted.keys()):
                    cursor.execute(f'SELECT Hpotions FROM users WHERE UserID = {ctx.author.id}')
                    updated = cursor.fetchone()[0] + 1
                    insert = ('UPDATE users SET Hpotions = ? WHERE UserID = ?')
                    values = (updated, ctx.author.id)
                    cursor.execute(insert, values)

                if 'points' in list(looted.keys()):
                    pdb = sql.connect('Profiles.sqlite')
                    pcursor = pdb.cursor()
                    pcursor.execute(f'SELECT House FROM users WHERE UserID = {ctx.author.id}')
                    house = pcursor.fetchone()[0].lower().capitalize()
                    pdb.commit()
                    pcursor.close()
                    pdb.close()

                    hdb = sql.connect('Houses.sqlite')
                    hcursor = hdb.cursor()
                    hcursor.execute(f'SELECT {house} FROM House_points')
                    updated = hcursor.fetchone()[0] + loot_points
                    insert = (f'UPDATE House_points SET {house} = ?')
                    values = (updated,)
                    hcursor.execute(insert, values)
                    hcursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {ctx.author.id}')
                    INupdated = hcursor.fetchone()[0] + loot_points
                    INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
                    INvalues = (INupdated, ctx.author.id)
                    hcursor.execute(INinsert, INvalues)
                    hdb.commit()
                    hcursor.close()
                    hdb.close()

                cursor.execute(f'SELECT Rubies FROM users WHERE UserID = {ctx.author.id}')
                updated = cursor.fetchone()[0] + sold_rubies
                insert = ('UPDATE users SET Rubies = ? WHERE UserID = ?')
                values = (updated, ctx.author.id)
                cursor.execute(insert, values)

                db.commit()
                cursor.close()
                db.close()

                embed2.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed2.timestamp = datetime.datetime.utcnow()

        endmessage = await ctx.send(embed = embed2)
        await endmessage.add_reaction('✅')

        try: 
            reaction, user = await self.bot.wait_for('reaction_add', timeout = 300, check = lambda reaction, 
            user: (str(reaction.emoji) == '✅' and user == ctx.author and reaction.message.id == endmessage.id))
        except asyncio.TimeoutError:
            await startmessage.delete()
            await endmessage.delete()
            await ctx.send('Looting timed out. Remaining processes completed automatically. Be faster next time, pabo.')
            return
        else:
            if str(reaction.emoji) == '✅':
                await startmessage.delete()
                await endmessage.delete()

    @commands.command(aliases = ['questcheck', 'Questcheck', 'check', 'Check', 'checker', 'Checker'])
    async def quest_check(self, ctx):
        def check(answer: discord.Message): 
            return answer.channel == ctx.channel and answer.author.id == ctx.author.id

        description = 'The Quest Checker calculates your chances of surviving each type of quest depending on what \
weapon/armor/companion/health you choose. "None" is a valid answer for any of the fields except for health.\n\n\
`quit` / `exit` to stop the command prematurely.'

        weaponembed = discord.Embed(title = 'RPG - Quest Checker', colour = discord.Colour(0xefe61), 
        description = description)
        weaponembed.add_field(name = '\u200b', value = '**Choose a weapon:**', inline = False)
        weaponembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        weaponembed.timestamp = datetime.datetime.utcnow()
        weaponmessage = await ctx.send(embed = weaponembed)
        try:
            weapon = await self.bot.wait_for('message', timeout = 120, check = check)
            weapon = weapon.content.lower().capitalize()
        except asyncio.TimeoutError:
            await weaponmessage.delete()
            await ctx.send('Quest Checker timed out.')
            return
        else:
            if weapon == 'Quit' or weapon == 'Exit':
                await weaponmessage.delete()
                await ctx.send('Quest Checker cancelled.')
                return
            if weapon != 'None':
                if not item_check(weapon):
                    await weaponmessage.delete()
                    await ctx.send('Item not found, pabo. Try again.')
                    return

            await weaponmessage.delete()

            armorembed = discord.Embed(title = 'RPG - Quest Checker', colour = discord.Colour(0xefe61), 
            description = description)
            armorembed.add_field(name = '\u200b', value = '**Choose a weapon:** ' + weapon, inline = False)
            armorembed.add_field(name = '\u200b', value = '**Choose armor:**', inline = False)
            armorembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            armorembed.timestamp = datetime.datetime.utcnow()
            armormessage = await ctx.send(embed = armorembed)

            try:
                armor = await self.bot.wait_for('message', timeout = 120, check = check)
                armor = armor.content.lower().capitalize()
            except asyncio.TimeoutError:
                await armormessage.delete()
                await ctx.send('Quest Checker timed out.')
                return
            else:
                if armor == 'Quit' or armor == 'Exit':
                    await armormessage.delete()
                    await ctx.send('Quest Checker cancelled.')
                    return
                if armor != 'None':
                    if not item_check(armor):
                        await armormessage.delete()
                        await ctx.send('Item not found, pabo. Try again.')
                        return

                companionembed = discord.Embed(title = 'RPG - Quest Checker', colour = discord.Colour(0xefe61),
                description = description)
                companionembed.add_field(name = '\u200b', value = '**Choose a weapon:** ' + weapon, inline = False)
                companionembed.add_field(name = '\u200b', value = '**Choose armor:** ' + armor, inline = False)
                companionembed.add_field(name = '\u200b', value = '**Choose a companion:**', inline = False)
                companionembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                companionembed.timestamp = datetime.datetime.utcnow()
                companionmessage = await ctx.send(embed = companionembed)

                try:
                    companion = await self.bot.wait_for('message', timeout = 120, check = check)
                    companion = companion.content.lower().capitalize()
                except asyncio.TimeoutError:
                    await companionmessage.delete()
                    await ctx.send('Quest Checker timed out.')
                    return
                else:
                    if companion == 'Quit' or companion == 'Exit':
                        await companionmessage.delete()
                        await ctx.send('Quest Checker cancelled.')
                        return
                    if companion != 'None':
                        if not item_check(companion):
                            await companionmessage.delete()
                            await ctx.send('Item not found, pabo. Try again.')
                            return

                    healthembed = discord.Embed(title = 'RPG - Quest Checker', colour = discord.Colour(0xefe61), 
                    description = description)
                    healthembed.add_field(name = '\u200b', value = '**Choose a weapon:** ' + weapon, inline = False)
                    healthembed.add_field(name = '\u200b', value = '**Choose armor:** ' + armor, inline = False)
                    healthembed.add_field(name = '\u200b', value = '**Choose a companion:** ' + companion, inline = False)
                    healthembed.add_field(name = '\u200b', value = '**Choose amount of health (1-100):** ', inline = False)
                    healthembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    healthembed.timestamp = datetime.datetime.utcnow()
                    healthmessage = await ctx.send(embed = healthembed)

                    try:
                        health = await self.bot.wait_for('message', timeout = 120, check = check)
                        health = health.content
                    except asyncio.TimeoutError:
                        await healthmessage.delete()
                        await ctx.send('Quest Checker timed out.')
                        return
                    else:
                        if health.lower() == 'quit' or health.lower() == 'exit':
                            await healthmessage.delete()
                            await ctx.send('Quest Checker cancelled.')
                            return
                        health = int(health)
                        if health > 100 or health < 1:
                            await healthmessage.delete()
                            await ctx.send("That's an invalid amount, pabo. Try again.")
                            return

                        db = sql.connect('RPG.sqlite')
                        cursor = db.cursor()

                        if weapon != 'None':
                            cursor.execute(f'SELECT Attack FROM market WHERE Name LIKE "{weapon}"')
                            attack = cursor.fetchone()[0]
                        else:
                            attack = 0
                        if armor != 'None':
                            cursor.execute(f'SELECT Defense FROM market WHERE Name LIKE "{armor}"')
                            defense = cursor.fetchone()[0]
                        else:
                            defense = 0
                        if companion != 'None':
                            cursor.execute(f'SELECT * FROM market WHERE Name LIKE "{companion}"')
                            companion_info = cursor.fetchall()[0]
                            special = companion_info[5]
                            if special == 'Attack':
                                attack += companion_info[3]
                            elif special == 'Defense':
                                defense += companion_info[4]

                        quest_attack1 = 10
                        quest_defense1 = 10
                        quest_attack2 = 30
                        quest_defense2 = 30
                        quest_attack3 = 50
                        quest_defense3 = 50
                        quest_attack4 = 75
                        quest_defense4 = 75
                        health_chance1 = 60
                        health_chance2 = 80
                        health_chance3 = 100
                        health_chance4 = 150

                        health_chance1 = health / health_chance1 * 0.1
                        attack_chance1 = attack / quest_attack1 * 0.45
                        defense_chance1 = defense / quest_defense1 * 0.45
                        avg1 = (attack_chance1 + defense_chance1 + health_chance1)  * 100

                        health_chance2 = health / health_chance2 * 0.1
                        attack_chance2 = attack / quest_attack2 * 0.45
                        defense_chance2 = defense / quest_defense2 * 0.45
                        avg2 = (attack_chance2 + defense_chance2 + health_chance2)  * 100

                        health_chance3 = health / health_chance3 * 0.1
                        attack_chance3 = attack / quest_attack3 * 0.45
                        defense_chance3 = defense / quest_defense3 * 0.45
                        avg3 = (attack_chance3 + defense_chance3 + health_chance3)  * 100

                        health_chance4 = health / health_chance4 * 0.1
                        attack_chance4 = attack / quest_attack4 * 0.45
                        defense_chance4 = defense / quest_defense4 * 0.45
                        avg4 = (attack_chance4 + defense_chance4 + health_chance4)  * 100

                        if avg1 >= 100:
                            avg1 = 100
                        if avg2 >= 100:
                            avg2 = 100
                        if avg3 >= 100:
                            avg3 = 100
                        if avg4 >= 100:
                            avg4 = 100

                        questembed = discord.Embed(title = 'RPG - Quest Checker', colour = discord.Colour(0xefe61),
                        description = f'**Weapon:** {weapon}\n**Armor:** {armor}\n**Companion:** {companion}\n\
                            **Health:** {health}/100\n\n**Attack:** {attack}\n**Defense:** {defense}')
                        questembed.set_thumbnail(url = 'https://imgur.com/zXZtR0U.png')
                        questembed.add_field(name = 'Quest 1 - Difficulty: Newcomer', 
                        value = f'Recommended: Attack: **{quest_attack1}**, Defense: **{quest_defense1}** \n\
                                  Chance of survival: **{avg1:.2f}%**',
                        inline = False)
                        questembed.add_field(name = 'Quest 2 - Difficulty: Adventurer', 
                        value = f'Recommended: Attack: **{quest_attack2}**, Defense: **{quest_defense1}** \n\
                                  Chance of survival: **{avg2:.2f}%**',
                        inline = False)
                        questembed.add_field(name = 'Quest 3 - Difficulty: Experienced', 
                        value = f'Recommended: Attack: **{quest_attack3}**, Defense: **{quest_defense3}** \n\
                                  Chance of survival: **{avg3:.2f}%**',
                        inline = False)
                        questembed.add_field(name = 'Boss Battle - Difficulty: Professional', 
                        value = f'Recommended: Attack: **{quest_attack4}**, Defense: **{quest_defense4}** \n\
                                  Chance of survival: **{avg4:.2f}%**',
                        inline = False)
                        questembed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                        questembed.timestamp = datetime.datetime.utcnow()

                        await ctx.send(embed = questembed)

    @commands.command(aliases = ['Heal', 'health', 'Health'])
    async def heal(self, ctx):
        if not profile_check(ctx.author.id):
            await ctx.send('Please create a profile (`k.profile_set`) before attempting to use a health potion, pabo.')
            return
        if not house_check(ctx.author.id):
            await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            return

        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT HP FROM users WHERE UserID = {ctx.author.id}')
        insert = ('UPDATE users SET HP = ? WHERE UserID = ?')
        values1 = (100, ctx.author.id)
        cursor.execute(insert, values1)
        
        cursor.execute(f'SELECT Hpotions FROM users WHERE UserID = {ctx.author.id}')
        HP_count = cursor.fetchone()[0]

        if HP_count == 0:
            await ctx.send("You don't have any health potions to use, pabo. Head to the market to purchase some.")
            db.commit()
            cursor.close()
            db.close()
            return

        updated = HP_count - 1
        insert = ('UPDATE users SET Hpotions = ? WHERE UserID = ?')
        values2 = (updated, ctx.author.id)
        cursor.execute(insert, values2)
        
        db.commit()
        cursor.close()
        db.close()

        await ctx.send('🍷 You drink a health potion and restore your health to **100** HP.')

    @commands.command(aliases = ['Work', 'shift', 'Shift'])
    @commands.cooldown(1, 28800, commands.BucketType.user) 
    async def work(self, ctx):
        if not profile_check(ctx.author.id):
            self.bot.get_command('work').reset_cooldown(ctx)
            await ctx.send("You haven't set a profile yet, pabo. Create one with `k.profile_set`.")
            return
        if not house_check(ctx.author.id):
            self.bot.get_command('work').reset_cooldown(ctx)
            await ctx.send("You don't have a house yet, pabo. Get sorted into one with `k.get_sorted`.")
            return
        
        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT * FROM users WHERE UserID = {ctx.author.id}')
        user_info = cursor.fetchall()[0]
        job = user_info[8]
        rubies = user_info[2]

        if job == 'None':
            self.bot.get_command('work').reset_cooldown(ctx)
            await ctx.send('You are unemployed, pabo. Get a job first.')
            return

        if job == 'Pickpocket':
            wage = random.randint(1, 5)
        else:
            cursor.execute(f'SELECT Special FROM market WHERE Name LIKE "{job}"')
            wage = int(cursor.fetchone()[0])

        insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
        updated = rubies + wage
        values = (updated, ctx.author.id)
        cursor.execute(insert, values)

        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'⚒ You earned **{wage}** rubies at your job!')

    @commands.command(aliases = ['add_points', 'points_add'])
    async def points_to(self, ctx, house, points, member: discord.Member = None):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only the Headmaster can do that, pabo.')
            return 
        if member is not None:
            if not profile_check(member.id):
                await ctx.send("This user doesn't have an RPG profile, pabo. Try again with someone else.")
                return
            if not house_check(member.id):
                await ctx.send("This user doesn't have a house, pabo. Try again with someone else.")
                return

        house = house.lower().capitalize()
        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT {house} FROM House_points')
        updated = cursor.fetchone()[0] + int(points)
        insert = (f'UPDATE House_points SET {house} = ?')
        values = (updated,)
        cursor.execute(insert, values)

        if member is not None:
            cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {member.id}')
            INupdated = cursor.fetchone()[0] + int(points)
            INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
            INvalues = (INupdated, member.id)
            cursor.execute(INinsert, INvalues)

        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'💎 **{points}** points to {house} House!')

    @commands.command(aliases = ['add_points_ex', 'points_add_ex'])
    async def points_to_ex(self, ctx):
        await ctx.send('```k.points_to Pink 50 @Kaiserrollii\n\
>>> [Adds 50 points to Pink house and 50 individual points to @Kaiserrollii]```')

    @commands.command(aliases = ['subtract_points', 'points_subtract'])
    async def points_from(self, ctx, house, points, member: discord.Member = None):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only the Headmaster can do that, pabo.')
            return 
        if member is not None:
            if not profile_check(member.id):
                await ctx.send("This user doesn't have an RPG profile, pabo. Try again with someone else.")
                return
            if not house_check(member.id):
                await ctx.send("This user doesn't have a house, pabo. Try again with someone else.")
                return

        house = house.capitalize()
        db = sql.connect('Houses.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT {house} FROM House_points')
        updated = cursor.fetchone()[0] - int(points)
        insert = (f'UPDATE House_points SET {house} = ?')
        values = (updated,)
        cursor.execute(insert, values)

        if member is not None:
            cursor.execute(f'SELECT IN_points FROM {house} WHERE UserID = {member.id}')
            INupdated = cursor.fetchone()[0] - int(points)
            INinsert = (f'UPDATE {house} SET IN_points = ? WHERE UserID = ?')
            INvalues = (INupdated, member.id)
            cursor.execute(INinsert, INvalues)

        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'💎 **{points}** points from {house} House!')

    @commands.command(aliases = ['subtract_points_ex', 'points_subtract_ex'])
    async def points_from_ex(self, ctx):
        await ctx.send('```k.points_from Pink 50 @Kaiserrollii\n\
>>> [Takes 50 points from Pink house and 50 individual points from @Kaiserrollii]```')

    @commands.command(aliases = ['add_rubies', 'rubies_add'])
    async def rubies_to(self, ctx, member: discord.Member, amount):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only the Headmaster can do that, pabo.')
            return 
        if not profile_check(member.id):
            await ctx.send("This user doesn't have an RPG profile, pabo. Try again with someone else.")
            return
        if not house_check(member.id):
            await ctx.send("This user doesn't have a house, pabo. Try again with someone else.")
            return
        
        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT Rubies FROM users WHERE UserID = {member.id}')
        updated = cursor.fetchone()[0] + int(amount)
        insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
        values = (updated, member.id)
        cursor.execute(insert, values)
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'💎 **{amount}** rubies added to {member.mention}.')

    @commands.command(aliases = ['add_rubies_ex', 'rubies_add_ex'])
    async def rubies_to_ex(self, ctx):
        await ctx.send('```k.rubies_to @Kaiserrollii 500\n>>> [Gives 500 rubies to @Kaiserrollii]```')

    @commands.command(aliases = ['subtract_rubies', 'rubies_subtract'])
    async def rubies_from(self, ctx, member: discord.Member, amount):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only the Headmaster can do that, pabo.')
            return 
        if not profile_check(member.id):
            await ctx.send("This user doesn't have an RPG profile, pabo. Try again with someone else.")
            return
        if not house_check(member.id):
            await ctx.send("This user doesn't have a house, pabo. Try again with someone else.")
            return
        
        db = sql.connect('RPG.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT Rubies FROM users WHERE UserID = {member.id}')
        updated = cursor.fetchone()[0] - int(amount)
        insert = (f'UPDATE users SET Rubies = ? WHERE UserID = ?')
        values = (updated, member.id)
        cursor.execute(insert, values)
        db.commit()
        cursor.close()
        db.close()

        await ctx.send(f'💎 **{amount}** rubies taken from {member.mention}.')

    @commands.command(aliases = ['subtract_rubies_ex', 'rubies_subtract_ex'])
    async def rubies_from_ex(self, ctx):
        await ctx.send('```k.rubies_from @Kaiserrollii 500\n>>> [Takes 500 rubies from @Kaiserrollii]```')      

    @commands.command(aliases = ['Delete_user', 'remove_user', 'Remove_user'])
    async def delete_user(self, ctx, member: discord.Member):
        if ctx.author.id != 496181635952148483:
            await ctx.send('Only the Headmaster can do that, pabo.')
            return 
        if not profile_check(member.id):
            await ctx.send("This user doesn't have a profile, pabo. Try again with someone else.")
            return

        db = sql.connect('Profiles.sqlite')
        cursor = db.cursor()

        if house_check(member.id):
            cursor.execute(f'SELECT House FROM users WHERE UserID = {member.id}')
            house = cursor.fetchone()[0]

            db1 = sql.connect('RPG.sqlite')
            cursor1 = db1.cursor()
            cursor1.execute(f'DELETE FROM users WHERE UserID = {member.id}')
            db1.commit()
            cursor1.close()
            db1.close()

            db2 = sql.connect('Houses.sqlite')
            cursor2 = db2.cursor()
            cursor2.execute(f'DELETE FROM {house} WHERE UserID = {member.id}')
            db2.commit()
            cursor2.close()
            db2.close()

        cursor.execute(f'DELETE FROM users WHERE UserID = {member.id}')
        db.commit()
        cursor.close()
        db.close()

        await ctx.send('User has been deleted.')

    @commands.command(aliases = ['Delete_user_ex', 'remove_user_ex', 'Remove_user_ex'])
    async def delete_user_ex(self, ctx):
        await ctx.send("```k.delete_user @Kaiserrollii\n>>> [Deletes @Kaiserrollii from the Houses & RPG system]```")

def setup(bot):
    bot.add_cog(System(bot))
