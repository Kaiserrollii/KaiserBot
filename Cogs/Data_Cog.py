import discord
import datetime 
import asyncio
import io
import praw
import requests
import tweepy as tw
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
from datetime import date 
from datetime import timedelta 
from googletrans import Translator
from PyDictionary import PyDictionary as pyd
from alpha_vantage.timeseries import TimeSeries
from bs4 import BeautifulSoup
from discord.ext import commands 


fin = open('Saved/Confidential.txt')
lines = list(map(lambda x: x.strip(), fin.readlines()))
fin.close()

reddit = praw.Reddit(client_id = lines[1],
                     client_secret = lines[2],
                     user_agent = lines[3])

consumer_key = lines[4]
consumer_secret = lines[5]
access_token = lines[6]
access_token_secret = lines[7]

auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit = True)

api_key = lines[8]

plt.style.use('dark_background')

class Data_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Data: Online')

    # Consumes word, which must be a valid word that is either a noun, verb, adjective, or adverb
    # Returns an embed with the definitions of the specified word
    # Very buggy in the presence of '(' or ')' -- may fix later or completely remove command
    @commands.command(aliases = ['Define', 'def', 'Def', 'word', 'Word'])
    async def define(self, ctx, *, word):
        if len(word.split()) > 1:
            await ctx.send('You can only search for a *single* word, pabo. Try again.')
        else:
            embed = discord.Embed(title = f"Define: {word.capitalize()}", colour = discord.Colour(0xefe61),
            description = '*N: Noun* | *V: Verb* | *Adj: Adjective* | *Adv: Adverb*')
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()
            
            d = pyd.meaning(word)
            if 'Noun' in d.keys():
                for i in d['Noun']:
                    if i == '(computer science':
                        continue
                    if '(' in i:
                        i = i.replace('(', '')
                        embed.add_field(name ='\u200b', value = '**N:** ' + i.capitalize(), inline = False)
                    else:
                        embed.add_field(name ='\u200b', value = '**N:** ' + i.capitalize(), inline = False)
            if 'Verb' in d.keys():
                for i in d['Verb']:
                    if '(' in i:
                        i = i.replace('(', '')
                        embed.add_field(name ='\u200b', value = '**V:** ' + i.capitalize(), inline = False)
                    else:
                        embed.add_field(name ='\u200b', value = '**V:** ' + i.capitalize(), inline = False)
            if 'Adjective' in d.keys():
                for i in d['Adjective']:
                    if i == '(computer science':
                        continue
                    if '(' in i:
                        i = i.replace('(', '')
                        embed.add_field(name ='\u200b', value = '**Adj:** ' + i.capitalize(), inline = False)
                    else:
                        embed.add_field(name ='\u200b', value = '**Adj:** ' + i.capitalize(), inline = False)
            if 'Adverb' in d.keys():
                for i in d['Adverb']:
                    if i == '(computer science':
                        continue
                    if '(' in i:
                        i = i.replace('(', '')
                        embed.add_field(name ='\u200b', value = '**Adv:** ' + i.capitalize(), inline = False)
                    else:
                        embed.add_field(name ='\u200b', value = '**Adv:** ' + i.capitalize(), inline = False)
        
            await ctx.send(embed = embed)

    @commands.command(aliases = ['Define_ex', 'def_ex', 'Def_ex', 'word_ex', 'Word_ex'])
    async def define_ex(self, ctx):
        await ctx.send('```k.define Kaiser \n>>> The title of the holy roman emperors or the emperors of austria or of...```\n\
Scrapes definitions from https://wordnet.princeton.edu/')

    # Consumes parameters start and end, which must be valid language codes, and message, a string
    # Returns the translated message according to the specified start and end languages
    @commands.command(aliases = ['Translate', 'trans', 'Trans', 'tr', 'Tr'])
    async def translate(self, ctx, start, end, *, message):
        translated = Translator().translate(message, src = start, dest = end)
        formatted = str(translated).split(',')[2][6:]
        await ctx.send(f'**Source ({start})**: {message}\n**Translation ({end})**: {formatted}')

    @commands.command(aliases = ['Translate_ex', 'trans_ex', 'Trans_ex', 'tr_ex', 'Tr_ex'])
    async def translate_ex(self, ctx):
        await ctx.send('''```k.tr en ko Irene is the best. \n>>> 아이린은 최고입니다.```
Language codes: https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages''')

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the current hot post from the specified subreddit, along with submission author, flair, score, and amount of comments
    # Skips over pinned posts
    @commands.command(aliases = ['rh', 'RH', 'Rh', 'rH'])
    async def reddit_hot(self, ctx, subreddit):
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        else:
            hotposts = list(reddit.subreddit(f'{subreddit}').hot(limit = 3))
            for submission in hotposts:
                if submission.stickied:
                    hotposts[1:]
                else:
                    date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
                    if submission.selftext != '':
                        embed = discord.Embed(title = f'Current Hot Post from r/{subreddit}', color = discord.Colour(0xefe61),
                        description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                        **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                        embed.add_field(name = 'Contents:', value = f'{submission.selftext[:300]}...', inline = False)
                        embed.add_field(name = 'Link to post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed = embed)
                        break
                    else:
                        embed = discord.Embed(title = f'Current Hot Post from r/{subreddit}', color = discord.Colour(0xefe61),
                        description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                        **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                        embed.timestamp = datetime.datetime.utcnow()

                        link = submission.url
                        linksplit = submission.url.split('.')
                        if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                            embed.set_image(url = f'{submission.url}')
                            embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                            await ctx.send(embed = embed)
                            break
                        elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                            url = requests.get(f'{link}')
                            soup = BeautifulSoup(url.text, 'html.parser')
                            directlink = soup.select('link[rel = image_src]')[0]['href']
                            embed.set_image(url = directlink)
                            embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                            await ctx.send(embed = embed)
                            break
                        elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                            or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                            or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                            embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                            await ctx.send(embed = embed)
                            await ctx.send(f'**Post Content:** {link}')
                            break
                        else:
                            embed.add_field(name = 'Post Content:', value = f'{submission.url}', inline = False)
                            embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                            await ctx.send(embed = embed)
                            break

    @commands.command(aliases = ['rh_ex', 'RH_ex', 'Rh_ex', 'rH_ex'])
    async def reddit_hot_ex(self, ctx):
        await ctx.send("```k.reddit_hot movies\n>>> [Current hot post in r/movies]```")

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the all-time top post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['rt', 'RT', 'Rt', 'rT'])
    async def reddit_top(self, ctx, subreddit, timeframe = None):
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        elif timeframe is None:
            await ctx.send('You need to pick a timeframe, pabo. Check `k.reddit_top_ex` for a full list.')
        else:
            timeframe = timeframe.lower()
            if timeframe == 'hour' or timeframe == 'h':
                timeframe = 'hour'
            elif timeframe == 'day' or timeframe == 'd':
                timeframe = 'day'
            elif timeframe == 'w' or timeframe == 'w':
                timeframe = 'week'
            elif timeframe == 'month' or timeframe == 'm':
                timeframe = 'month'
            elif timeframe == 'year' or timeframe == 'y':
                timeframe = 'year'
            elif timeframe == 'all' or timeframe == 'a':
                timeframe = 'all'
            else:
                await ctx.send("That's not a valid timeframe, pabo. Check the full list at `k.reddit_top_ex`.")
                return

            topposts = list(reddit.subreddit(f'{subreddit}').top(limit = 1, time_filter = timeframe))
            timeframe = timeframe.capitalize()
            for submission in topposts:
                date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
                if submission.selftext != '':
                    embed = discord.Embed(title = f'Top Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.add_field(name = 'Contents:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.add_field(name = 'Link to post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Top Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Post Content:', value = f'{submission.url}', inline = False)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['rt_ex', 'RT_ex', 'Rt_ex', 'rT_ex'])
    async def reddit_top_ex(self, ctx):
        d = {'Timeframe': ['Hour', 'Day', 'Week', 'Month', 'Year', 'All'], 'Alias': ['h', 'd', 'w', 'm', 'y', 'a']}
        index = [1, 2, 3, 4, 5, 6]
        df = pd.DataFrame(data = d, index = index)

        await ctx.send(f'```Full list of timeframes:\n\n{df}\n\nk.reddit_top jailbreak All \n\
>>> [All-time top post in r/jailbreak]```')

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the newest post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['rn', 'RN', 'Rn', 'rN'])
    async def reddit_new(self, ctx, subreddit):
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        else:
            newposts = list(reddit.subreddit(f'{subreddit}').new(limit = 1))
            for submission in newposts:
                date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
                if submission.selftext != '':
                    embed = discord.Embed(title = f'Newest Post from r/{subreddit}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.add_field(name = 'Contents:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.add_field(name = 'Link to post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Newest Post from r/{subreddit}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Content:', value = f'{submission.url}', inline = False)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['rn_ex', 'RN_ex', 'Rn_ex', 'rN_ex'])
    async def reddit_new_ex(self, ctx):
        await ctx.send('```k.reddit_new books \n>>> [Newest post in r/books]```')

    # Consumes a str, subreddit, which must be a valid SFW subreddit, and a str, timeframe, which must be a valid timeframe (k.rc_ex for full list)
    # Returns the most controversial post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['rc', 'RC', 'Rc', 'rC'])
    async def reddit_controversial(self, ctx, subreddit, timeframe = None):
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        elif timeframe is None:
            await ctx.send('You need to pick a timeframe, pabo. Check `k.reddit_controversial_ex` for a full list.')
        else:
            timeframe = timeframe.lower()
            if timeframe == 'hour' or timeframe == 'h':
                timeframe = 'hour'
            elif timeframe == 'day' or timeframe == 'd':
                timeframe = 'day'
            elif timeframe == 'w' or timeframe == 'w':
                timeframe = 'week'
            elif timeframe == 'month' or timeframe == 'm':
                timeframe = 'month'
            elif timeframe == 'year' or timeframe == 'y':
                timeframe = 'year'
            else:
                await ctx.send("That's not a valid timeframe, pabo. Check the full list at `k.reddit_controversial_ex`.")
                return

            controversialposts = reddit.subreddit(f'{subreddit}').controversial(limit = 1, time_filter = timeframe)
            timeframe = timeframe.capitalize()
            for submission in controversialposts:
                date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
                if submission.selftext != '':
                    embed = discord.Embed(title = f'Most Controversial Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.add_field(name = 'Contents:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.add_field(name = 'Link to post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Most Controversial Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Content:', value = f'{submission.url}', inline = False)
                        embed.add_field(name = 'Link to Post:', value = f'https://www.reddit.com{submission.permalink}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['rc_ex', 'RC_ex', 'Rc_ex', 'rC_ex'])
    async def reddit_controversial_ex(self, ctx):
        d = {'Timeframe': ['Hour', 'Day', 'Week', 'Month', 'Year'], 'Alias': ['h', 'd', 'w', 'm', 'y']}
        index = [1, 2, 3, 4, 5]
        df = pd.DataFrame(data = d, index = index)

        await ctx.send(f'```Full list of timeframes:\n\n{df}\n\nk.reddit_controversial politics Day \n\
>>> [Most controversial post in r/politics within the past day]```')

    # Consumes one parameter, search, which must be a valid group/soloist on kprofiles (works for some group members as well)
    # Returns the profile of the specified search
    @commands.command(aliases = ['Pop', 'profiles', 'Profiles', 'profile', 'Profile', 'pro', 'Pro'])
    async def pop(self, ctx, *, search):
        if search.lower() == 'blackpink':
            await ctx.send('https://kprofiles.com/black-pink-members-profile/')
        if search.lower() == 'bts':
            await ctx.send('https://kprofiles.com/bts-bangtan-boys-members-profile/')
        if search.lower() == 'leebada':
            await ctx.send('https://kprofiles.com/lee-ba-da-profile-facts/')
        else:
            gg = requests.get('https://kprofiles.com/k-pop-girl-groups/')
            bg = requests.get('https://kprofiles.com/k-pop-boy-groups/')
            solo = requests.get('https://kprofiles.com/kpop-solo-singers/')
            gg_soup = BeautifulSoup(gg.text, 'html.parser')
            bg_soup = BeautifulSoup(bg.text, 'html.parser')
            solo_soup = BeautifulSoup(solo.text, 'html.parser')
            gg_links = gg_soup.findAll('a')
            bg_links = bg_soup.findAll('a')
            solo_links = solo_soup.findAll('a')

            for link in gg_links:
                link = str(link).split('"')
                last = link[-1]
                new = last[1:(len(last) - 4)]
                if search.lower() == new.lower():
                    await ctx.send(link[1])
                    return
            for link in bg_links:
                link = str(link).split('"')
                last = link[-1]
                new = last[1:(len(last) - 4)]
                if search.lower() == new.lower():
                    await ctx.send(link[1])
                    return
            for link in solo_links:
                link = str(link).split('"')
                last = link[-1]
                new = last[1:(len(last) - 4)]
                if search.lower() == new.lower():
                    await ctx.send(link[1])
                    return

    @commands.command(aliases = ['Pop_ex', 'profiles_ex', 'Profiles_ex', 'profile_ex', 'Profile_ex', 'pro_ex', 'Pro_ex'])
    async def pop_ex(self, ctx):
        await ctx.send("```Please don't spam this command, and be patient if the links take a while to retrieve. \
If nothing is returned after ~15 seconds, it's safe to assume either the group/soloist requested is invalid or something else has gone wrong.\n\n\
k.pop Red Velvet\n>>> https://kprofiles.com/irene-facts-profile-irene-ideal-type/\n\n\
k.pop Kim Chungha\n>>> https://kprofiles.com/kim-chungha-profile-facts/```")

    # Consumes amount, an int between 1-25, and location, which must be a valid location (see WOEIDs.md for full list)
    # Returns a dataframe of the trending topics on Twitter according to the specified amount and location
    @commands.command(aliases = ['Twitter_trends', 'twt', 'Twt', 'twitter_trending', 'Twitter_trending'])
    async def twitter_trends(self, ctx, amount, *, location):
        if int(amount) < 1 or int(amount) > 25:
            await ctx.send('Amount should be an integer between 1 - 25, pabo. Choose something within that range.')
        else:
            fin = open('Saved/WOEIDs.txt')
            line = fin.readline()
            while(line != ''):
                lst = line.split(':')
                if lst[0].lower() == location.lower():
                    WOEID = lst[1]
                    geoloc = lst[0]
                    break 
                else:
                    line = fin.readline()
            fin.close()

            trends = str(api.trends_place(int(WOEID))).split("{'name': '")[1:int(amount)+1]
            await ctx.send(f'**{amount} Latest Trending Twitter Topics - {geoloc}**')

            d = {}
            for i in trends:
                n = i.find("'")
                v = i.find("'tweet_volume': ") + len("'tweet_volume': ")
                name = i[:n]
                volume = i[v:len(i)-3]
                if volume == 'None':
                    volume = 0
                d[name] = int(volume)

            d_sort = sorted(d.items(), key = lambda x: x[1], reverse = True)  
            df = pd.DataFrame(data = d_sort, columns = ['Topic', 'Tweet Volume'])
            df.index = np.arange(1, len(df) + 1)
            await ctx.send(f'`{df}`')
            await ctx.send('*0 = Unable to retrieve tweet volume data*')

    @commands.command(aliases = ['Twitter_trends_ex', 'twt_ex', 'Twt_ex', 'twitter_trending_ex', 'Twitter_trending_ex'])
    async def twitter_trends_ex(self, ctx):
        await ctx.send("```Please don't spam this command, and be patient if the table take a while to generate. \
If nothing is returned after ~15 seconds, it's safe to assume either the location requested is invalid or something else has gone wrong.\n\n\
k.twitter_trends 10 Worldwide\n>>> [10 trending topics on Twitter - Worldwide]\n\n\
k.twitter_trends 25 Canada\n>>> [25 trending topics on Twitter in Canada]```\n\
Full location list: <https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md>")

    # Consumes amount, an int between 1-25, and location, which must be a valid location (see WOEIDs.md for full list)
    # Returns a plot of the tweet volume of trending topics on Twitter, according to the specified amount and location
    @commands.command(aliases = ['Twitter_graph', 'twg', 'Twg', 'trend_graph', 'Trend_graph', 'trends_graph', 'Trends_graph'])
    async def twitter_graph(self, ctx, amount, *, location):
        if int(amount) < 1 or int(amount) > 25:
            await ctx.send('Amount should be an integer between 1 - 25, pabo. Choose something within that range.')
        else:
            fin = open('Saved/WOEIDs.txt')
            line = fin.readline()
            while(line != ''):
                lst = line.split(':')
                if lst[0].lower() == location.lower():
                    WOEID = lst[1]
                    geoloc = lst[0]
                    break 
                else:
                    line = fin.readline()
            fin.close()

            trends = str(api.trends_place(int(WOEID))).split("{'name': '")[1:int(amount)+1]

            d = {}
            for i in trends:
                n = i.find("'")
                v = i.find("'tweet_volume': ") + len("'tweet_volume': ")
                name = i[:n]
                volume = i[v:len(i)-3]
                if volume == 'None':
                    volume = 0
                d[name] = int(volume)

            d_sort = sorted(d.items(), key = lambda x: x[1], reverse = True)  
            df = pd.DataFrame(data = d_sort, columns = ['Topic', 'Tweet Volume'])
            df.index = np.arange(1, len(df)+1)

            if int(amount) == 1:
                await ctx.send('No graph is able to be shown. Use an amount > 1, pabo.')
            else:
                embed = discord.Embed(colour = discord.Colour(0xefe61))
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()

                df.plot(kind = 'line', x ='Topic', y ='Tweet Volume', color = '#1DA1F2')
                plt.suptitle(f'Tweet Volume of Latest Trending Twitter Topics - {geoloc}')
                plt.xticks(fontsize = 7)
                plt.ylabel('0 = Unable to retrieve', fontsize = 8)
                plt.savefig('Graphs/twitter_graph.png', transparent = True)
                with open('Graphs/twitter_graph.png', 'rb') as f: file = BytesIO(f.read())
                twitter_graph = discord.File(file, filename = 'twitter_graph.png')
                embed.set_image(url = f'attachment://twitter_graph.png')

                message = await ctx.send('*Generating graph...*')
                await asyncio.sleep(2)
                await message.edit(content = '*Generating graph... ✅*')
                await asyncio.sleep(1)
                await ctx.send(file = twitter_graph, embed = embed)
                await message.delete()

    @commands.command(aliases = ['Twitter_graph_ex', 'twg_ex', 'Twg_ex', 'trend_graph_ex', 'Trend_graph_ex', 'trends_graph_ex', 'Trends_graph_ex'])
    async def twitter_graph_ex(self, ctx):
        await ctx.send("```Please don't spam this command, and be patient if the graph takes a while to generate. \
If nothing is returned after ~20 seconds, it's safe to assume either the location requested is invalid or something else has gone wrong.\n\n\
k.twitter_graph 10 Worldwide\n>>> [Graph of tweet volume of 10 trending topics - Worldwide]\n\n\
k.twitter_graph 25 Canada\n>>> [Graph of tweet volume of 10 trending topics in Canada]```\n\
Full location list: <https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md>")

    # Consumes query, which must be a valid search, category, which must be either popular/recent, and timeframe, an integer between 0 - 7
    # Returns three tweets according to the specified query, category, and timeframe
    # If category is recent, leave timeframe blank
    # A timeframe of 0 also returns recent tweets
    @commands.command(aliases = ['Twitter_search', 'tws', 'Tws', 'search', 'Search'])
    async def twitter_search(self, ctx, query, category, *, timeframe = None):
        category = category.lower()
        if category != 'popular' and category != 'p' and category != 'recent' and category != 'r':
            await ctx.send('Category must be either `popular` / `p` or `recent` / `r`, pabo. Try again.')
            return
        if timeframe is None:
            timeframe = 0
            category = 'recent'
            tweets = tw.Cursor(api.search, q = f"{query} -filter:retweets", lang = 'en', since = date.today() - timedelta(days = timeframe),
            tweet_mode = 'extended', result_type = f'{category}').items(3)
            
            query = query.replace('+', ' ')
            embed = discord.Embed(title = f"Twitter Search: {query} - Recent", colour = discord.Colour(0xefe61))
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            for i in tweets:
                if not i.user.location:
                    i.user.location = 'Unable to locate' 
                    embed.add_field(name = f"@{i.user.screen_name} | {i.user.location}" , value = i.full_text, inline = False)
                else:
                    embed.add_field(name = f"@{i.user.screen_name} | {i.user.location}" , value = i.full_text, inline = False)

            await ctx.send(embed = embed)
        
        elif int(round(float(timeframe))) > 7 or int(round(float(timeframe))) < 0:
            await ctx.send("Timeframe must be an integer between 0 - 7, pabo. To search for current tweets, set timeframe to `0`.")
            return
        else:
            if category == 'p':
                category = 'popular'
            if category == 'r':
                category = 'recent'
            timeframe = int(round(float(timeframe)))
            tweets = tw.Cursor(api.search, q = f"{query} -filter:retweets", lang = 'en', since = date.today() - timedelta(days = timeframe),
            tweet_mode = 'extended', result_type = f'{category}').items(3)

            query = query.replace('+', ' ')
            if category == 'recent':
                embed = discord.Embed(title = f"Twitter Search: {query} - Recent", colour = discord.Colour(0xefe61))
            elif category == 'popular' and timeframe == 0:
                embed = discord.Embed(title = f"Twitter Search: {query} - Popular Now", colour = discord.Colour(0xefe61))
            else:
                embed = discord.Embed(title = f"Twitter Search: {query} - {category.capitalize()} - Past {timeframe} days", 
                colour = discord.Colour(0xefe61))
            
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            for i in tweets:
                if not i.user.location:
                    i.user.location = 'Unable to locate' 
                    embed.add_field(name = f"@{i.user.screen_name} | {i.user.location}" , value = i.full_text, inline = False)
                else:
                    embed.add_field(name = f"@{i.user.screen_name} | {i.user.location}" , value = i.full_text, inline = False)

            await ctx.send(embed = embed)
        
    @commands.command(aliases = ['Twitter_search_ex', 'tws_ex', 'Tws_ex', 'search_ex', 'Search_ex'])
    async def twitter_search_ex(self, ctx):
        await ctx.send("```[Query]: To search for multiple words, add '+' between each word (example below).\n\n\
[Category]: Either popular/p or recent/r. If searching for recent, leave timeframe blank.\n\n\
[Timeframe]: Leave timeframe blank to search for recent tweets. Otherwise, set to any integer between 0 - 7 to search for tweets within the \
past [Timeframe] days (example below).\n\n\
k.twitter_search #BLACKPINK popular 5\n>>> [Popular tweets containing #BLACKPINK within the past 5 days].\n\n\
k.twitter_search Irene+Red+Velvet recent\n>>> [Recent tweets with the phrase 'Irene Red Velvet']```")

    # Consumes ticker, which must be a valid ticker symbol (read StockInfo.md for details), and timeframe, which must be one of s/m/l
    # Returns a plot of closing price data according to the specified equity and timeframe
    @commands.command(aliases = ['Stock', 'stonk', 'Stonk', 'stonks', 'Stonks'])
    async def stock(self, ctx, ticker, timeframe):
        ticker = ticker.upper()
        timeframe = timeframe.lower()
        ts = TimeSeries(key = api_key, output_format= 'pandas')

        embed = discord.Embed(colour = discord.Colour(0xefe61))
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        if timeframe == 'short' or timeframe == 's':
            dfshort, meta_date = ts.get_intraday(symbol = ticker, interval = '1min', outputsize = 'compact')
            dfshort.plot(kind = 'line', y = '4. close', color = '#FEFFB3', legend = False)
            plt.suptitle(f'{ticker} Closing Price : Short-Term')
            plt.xlabel('Time')
            plt.ylabel('Closing Price')
            plt.savefig('Graphs/stockgraphshort.png', transparent = True)
            with open('Graphs/stockgraphshort.png', 'rb') as f: file = BytesIO(f.read())
            stockgraphshort = discord.File(file, filename = 'stockgraphshort.png')
            embed.set_image(url = f'attachment://stockgraphshort.png')

            message = await ctx.send('*Generating graph...*')
            await asyncio.sleep(2)
            await message.edit(content = '*Generating graph... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = stockgraphshort, embed = embed)
            await message.delete()
            plt.close('all')

        elif timeframe == 'medium' or timeframe == 'm':
            dfmedium, meta_date = ts.get_daily(symbol = ticker, outputsize = 'compact')
            dfmedium.plot(kind = 'line', y = '4. close', color = '#F57F73', legend = False)
            plt.suptitle(f'{ticker} Closing Price : Medium-Term')
            plt.xlabel('Time')
            plt.ylabel('Closing Price')
            plt.savefig('Graphs/stockgraphmedium.png', transparent = True)
            with open('Graphs/stockgraphmedium.png', 'rb') as f: file = BytesIO(f.read())
            stockgraphmedium = discord.File(file, filename = 'stockgraphmedium.png')
            embed.set_image(url = f'attachment://stockgraphmedium.png')
            
            message = await ctx.send('*Generating graph...*')
            await asyncio.sleep(2)
            await message.edit(content = '*Generating graph... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = stockgraphmedium, embed = embed)
            await message.delete()
            plt.close('all')

        elif timeframe == 'long' or timeframe == 'l':
            dflong, meta_date = ts.get_monthly(symbol = ticker)
            dflong.plot(kind = 'line', y = '4. close', legend = False)
            plt.suptitle(f'{ticker} Closing Price : Long-Term')
            plt.xlabel('Time')
            plt.ylabel('Closing Price')
            plt.savefig('Graphs/stockgraphlong.png', transparent = True)
            with open('Graphs/stockgraphlong.png', 'rb') as f: file = BytesIO(f.read())
            stockgraphlong = discord.File(file, filename = 'stockgraphlong.png')
            embed.set_image(url = f'attachment://stockgraphlong.png')
            
            message = await ctx.send('*Generating graph...*')
            await asyncio.sleep(2)
            await message.edit(content = '*Generating graph... ✅*')
            await asyncio.sleep(1)
            await ctx.send(file = stockgraphlong, embed = embed)
            await message.delete()
            plt.close('all')

        else:
            await ctx.send('That timeframe is invalid, pabo. Choose between short(s), medium(m), or long(l).')

    @commands.command(aliases = ['Stock_ex', 'stonk_ex', 'Stonk_ex', 'stonks_ex', 'Stonks_ex'])
    async def stock_ex(self, ctx):
        await ctx.send("```The API used for this command, Alpha Vantage, only allows for 5 calls per minute and a maximum of 500 calls daily \
since I'm not a premium user. Please don't spam this command, and be patient if the graphs take a while to generate. \
If nothing is returned after ~30 seconds, it's safe to assume either the equity/timeframe you requested is not supported by the API, the 5 call limit \
has been reached, or something else has gone wrong.\n\n\
k.stock AAPL long\n>>> [Graph of AAPL stock - Historic data (yearly)]\n\n\
k.stock NVDA medium\n>>> [Graph of NVDA stock - Historic data (monthly)]\n\n\
k.stock 182360.KQ short\n>>> [Graph of Cube Entertainment stock - Recent]```\n\
To pull data from outside the USA, please read this info page: <https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/StockInfo.md>")

    @commands.command(aliases = ['Melon', 'mel', 'Mel'])
    async def melon(self, ctx, *, timeframe = None):
        if timeframe is None:
            await ctx.send('You need to specify a timeframe, pabo. Check `k.melon_ex` for a full list.')
        else:
            timeframe = timeframe.lower()
            if timeframe == 'realtime' or timeframe == 'rt':
                url = 'https://www.melon.com/chart/'
                timeframe = 'Realtime'
            elif timeframe == 'rising' or timeframe == 'hot' or timeframe == 'r' or timeframe == 'h':
                url = 'https://www.melon.com/chart/rise/index.htm#params%5Bidx%5D=1'
                timeframe = 'Rising'
            elif timeframe == 'daily' or timeframe == 'd':
                url = 'https://www.melon.com/chart/day/index.htm'
                timeframe = 'Daily'
            elif timeframe == 'weekly' or timeframe == 'w':
                url = 'https://www.melon.com/chart/week/index.htm#params%5Bidx%5D=1&params%5BstartDay%5D=20200504&params%5BendDay%\
                5D=20200510&params%5BisFirstDate%5D=false&params%5BisLastDate%5D=true'
                timeframe = 'Weekly'
            elif timeframe == 'monthly' or timeframe == 'm':
                url = 'https://www.melon.com/chart/month/index.htm#params%5Bidx%5D=1&params%5BrankMonth%5D=202004&params%5BisFirstDate%\
                5D=false&params%5BisLastDate%5D=true'
                timeframe = 'Monthly'
            else:
                await ctx.send("That's not a valid timeframe, pabo. Check the full list at `k.melon_ex`.")
                return

            message = await ctx.send('*Retrieving chart data... ✅*')
            user_agent = {'User-Agent': 'Mozilla/5.0'}
            response = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            titles = soup.find_all('div', {'class': 'ellipsis rank01'})
            artists = soup.find_all('span', {'class': 'checkEllipsis'})
            albums = soup.find_all('div', {'class': 'ellipsis rank03'})

            embed = discord.Embed(title = f'Melon - Top Tracks - {timeframe}', colour = discord.Colour(0xefe61))
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            index = 0
            count = 1
            for i in titles[:10]:
                embed.add_field(name = f'#{count} - Album: {albums[index].text.strip()}',
                value = f'{artists[index].text.strip()} - **{i.text.strip()}**', inline = False)
                index += 1
                count += 1
            
            await message.edit(content = '*Retrieving chart data... ✅*')
            await asyncio.sleep(1)
            await ctx.send(embed = embed)
            await message.delete()

    @commands.command(aliases = ['Melon_ex', 'mel_ex', 'Mel_ex'])
    async def melon_ex(self, ctx):
        d = {'Timeframe': ['Realtime', 'Rising', 'Daily', 'Weekly', 'Monthly'], 'Alias': ['rt', 'r', 'd', 'w', 'm']}
        index = [1, 2, 3, 4, 5]
        df = pd.DataFrame(data = d, index = index)

        await ctx.send(f'```Full list of timeframes:\n\n{df}\n\nk.melon Realtime\n>>> [Top 10 tracks on Melon - Realtime]```')

    @commands.command(aliases = ['Charts', 'chart', 'Chart'])
    async def charts(self, ctx, *, artist = None):
        if artist is None:
            await ctx.send("You need to specify an artist, pabo. Try again, and make sure it's a valid artist on the charts. For a full list, check the `All` dropdown menu from <http://www.kpopchart.kr/?a=>.")
        else:
            artist = artist.lower()
            if artist == 'sm':
                artist = 'sm%20ent'
            if artist == 'jyp':
                artist = 'jyp%20ent'
            if artist == 'yg':
                artist = 'yg%20ent'
            if artist == 'bts':
                artist = '방탄소년단'
            if artist == 'chungha':
                artist = '청하'
            if artist == 'gidle':
                artist = '(G)I-DLE'

            artist = artist.replace(' ', '%20')
            link = f'http://www.kpopchart.kr/?a={artist}'
            request = requests.get(f'http://www.kpopchart.kr/?a={artist}')
            soup = BeautifulSoup(request.text, 'html.parser')

            melontable = soup.find('table', {'class': 'table chart_table table_MELON'})
            flotable = soup.find('table', {'class': 'table chart_table table_MNET'})
            genietable = soup.find('table', {'class': 'table chart_table table_GENIE'})
            bugstable = soup.find('table', {'class': 'table chart_table table_BUGS'})
            soribadatable = soup.find('table', {'class': 'table chart_table table_SORIBADA'})
            navertable = soup.find('table', {'class': 'table chart_table table_NAVER'})

            if melontable is None and flotable is None and genietable is None and bugstable is None and soribadatable is None \
            and navertable is None:
                await ctx.send("Sorry, but the artist you chose isn't on the charts. Nugu.")
                return

            if artist == 'sm%20ent' or artist == 'jyp%20ent' or artist == 'yg%20ent':
                if artist == 'sm%20ent':
                    embed = discord.Embed(title = f'Top Charts - SM Entertainment - Realtime', colour = discord.Colour(0xefe61), description = link)
                    embed.set_thumbnail(url = 'https://img1.kpopmap.com/2018/04/smentertainment.jpg')
                if artist == 'jyp%20ent':
                    embed = discord.Embed(title = f'Top Charts - JYP Entertainment - Realtime', colour = discord.Colour(0xefe61), description = link)
                    embed.set_thumbnail(url = 'https://media.glassdoor.com/sqll/192707/jyp-entertainment-usa-squarelogo-1466515471350.png')
                if artist == 'yg%20ent':
                    embed = discord.Embed(title = f'Top Charts - YG Entertainment - Realtime', colour = discord.Colour(0xefe61), description = link)
                    embed.set_thumbnail(url = 'https://yt3.ggpht.com/a-/AN66SAxq_HLhOdnNkazOJtXPOR6n6Od9WFxbcXk6cw=s900-mo-c-c0xffffffff-rj-k-no')
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()
                
                if melontable is not None:
                    fmelon = melontable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    melonstring = ''
                    melonindex = 0
                    for i in list(range((len(fmelon) // 4))):
                        text = f"{fmelon[melonindex]}. {fmelon[melonindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fmelon[melonindex+2]}** \u200b - {fmelon[melonindex+3]}\n"
                        melonstring += text
                        melonindex += 4
                    embed.add_field(name = 'Melon', value = melonstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if flotable is not None:
                    fflo = flotable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    flostring = ''
                    floindex = 0
                    for i in list(range((len(fflo) // 4))):
                        text = f"{fflo[floindex]}. {fflo[floindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fflo[floindex+2]}** \u200b - {fflo[floindex+3]}\n"
                        flostring += text
                        floindex += 4
                    embed.add_field(name = 'Flo', value = flostring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if genietable is not None:
                    fgenie = genietable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    geniestring = ''
                    genieindex = 0
                    for i in list(range((len(fgenie) // 4))):
                        text = f"{fgenie[genieindex]}. {fgenie[genieindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fgenie[genieindex+2]}** \u200b - {fgenie[genieindex+3]}\n"
                        geniestring += text
                        genieindex += 4
                    embed.add_field(name = 'genie', value = geniestring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if bugstable is not None:
                    fbugs = bugstable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    bugsstring = ''
                    bugsindex = 0
                    for i in list(range((len(fbugs) // 4))):
                        text = f"{fbugs[bugsindex]}. {fbugs[bugsindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fbugs[bugsindex+2]}** \u200b - {fbugs[bugsindex+3]}\n"
                        bugsstring += text
                        bugsindex += 4
                    embed.add_field(name = 'Bugs', value = bugsstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if soribadatable is not None:
                    fsoribada = soribadatable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    soribadastring = ''
                    soribadaindex = 0
                    for i in list(range((len(fsoribada) // 4))):
                        text = f"{fsoribada[soribadaindex]}. {fsoribada[soribadaindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fsoribada[soribadaindex+2]}** \u200b - {fsoribada[soribadaindex+3]}\n"
                        soribadastring += text
                        soribadaindex += 4
                    embed.add_field(name = 'soribada', value = soribadastring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if navertable is not None:
                    fnaver = navertable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    naverstring = ''
                    naverindex = 0
                    for i in list(range((len(fnaver) // 4))):
                        text = f"{fnaver[naverindex]}. {fnaver[naverindex+1].replace(' ', '').replace('-', '‑0')} \
                        \u200b **{fnaver[naverindex+2]}** \u200b - {fnaver[naverindex+3]}\n"
                        naverstring += text
                        naverindex += 4
                    embed.add_field(name = 'Naver', value = naverstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                    
                await ctx.send(embed = embed)

            else:
                image = soup.find('img', {'class': 'data-albumimage'}).attrs['src']
                artistname = soup.find('div', {'class': 'data-artistname'})
                embed = discord.Embed(title = f'Top Charts - {artistname.text} - Realtime', colour = discord.Colour(0xefe61), description = link)
                embed.set_thumbnail(url = f'http://www.kpopchart.kr/{image}')
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()

                if melontable is not None:
                    fmelon = melontable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    melonstring = ''
                    melonindex = 0
                    for i in list(range((len(fmelon) // 4))):
                        text = f"{fmelon[melonindex]}. {fmelon[melonindex+1].replace(' ', '').replace('-', '‑0')} \u200b **{fmelon[melonindex+2]}**\n"
                        melonstring += text
                        melonindex += 4
                    embed.add_field(name = 'Melon', value = melonstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if flotable is not None:
                    fflo = flotable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    flostring = ''
                    floindex = 0
                    for i in list(range((len(fflo) // 4))):
                        text = f"{fflo[floindex]}. {fflo[floindex+1].replace(' ', '').replace('-', '‑0')} \u200b **{fflo[floindex+2]}**\n"
                        flostring += text
                        floindex += 4
                    embed.add_field(name = 'Flo', value = flostring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if genietable is not None:
                    fgenie = genietable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    geniestring = ''
                    genieindex = 0
                    for i in list(range((len(fgenie) // 4))):
                        text = f"{fgenie[genieindex]}. {fgenie[genieindex+1].replace(' ', '').replace('-', '‑0')} \u200b **{fgenie[genieindex+2]}**\n"
                        geniestring += text
                        genieindex += 4
                    embed.add_field(name = 'genie', value = geniestring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if bugstable is not None:
                    fbugs = bugstable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    bugsstring = ''
                    bugsindex = 0
                    for i in list(range((len(fbugs) // 4))):
                        text = f"{fbugs[bugsindex]}. {fbugs[bugsindex+1].replace(' ', '').replace('-', '‑0')} \u200b **{fbugs[bugsindex+2]}**\n"
                        bugsstring += text
                        bugsindex += 4
                    embed.add_field(name = 'Bugs', value = bugsstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if soribadatable is not None:
                    fsoribada = soribadatable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    soribadastring = ''
                    soribadaindex = 0
                    for i in list(range((len(fsoribada) // 4))):
                        text = f"{fsoribada[soribadaindex]}. {fsoribada[soribadaindex+1].replace(' ', '').replace('-', '‑0')}\
                        \u200b **{fsoribada[soribadaindex+2]}**\n"
                        soribadastring += text
                        soribadaindex += 4
                    embed.add_field(name = 'soribada', value = soribadastring.replace("`", "'").replace("’", "'").strip(), inline = False)
                if navertable is not None:
                    fnaver = navertable.text.strip().replace('\n\n\n\n', '').replace('\n\n', '').split('\n')
                    naverstring = ''
                    naverindex = 0
                    for i in list(range((len(fnaver) // 4))):
                        text = f"{fnaver[naverindex]}. {fnaver[naverindex+1].replace(' ', '').replace('-', '‑0')} \u200b **{fnaver[naverindex+2]}**\n"
                        naverstring += text
                        naverindex += 4
                    embed.add_field(name = 'Naver', value = naverstring.replace("`", "'").replace("’", "'").strip(), inline = False)
                    
                await ctx.send(embed = embed)

    @commands.command(aliases = ['Charts_ex', 'chart_ex', 'Chart_ex'])
    async def charts_ex(self, ctx):
        await ctx.send('```k.charts Red Velvet\n>>> [Top charts containing Red Velvet tracks]\n\n\
k.charts SM\n>>> [Top charts containing SM Entertainment tracks]```\n\
For a full list of artists currently on the charts, check the `All` dropdown menu on <http://www.kpopchart.kr/?a=>')


def setup(bot):
    bot.add_cog(Data_Cog(bot))
