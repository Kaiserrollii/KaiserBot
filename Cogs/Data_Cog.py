import discord
import datetime 
import asyncio
import io
import praw
import requests
import json
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
from forex_python.converter import CurrencyRates as fxp
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

API_KEY = lines[9]

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
        message = message.replace('\n', ' ')
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
    @commands.command(aliases = ['Reddit_hot', 'rh', 'RH', 'Rh', 'rH'])
    async def reddit_hot(self, ctx, subreddit = None):
        if subreddit is None:
            await ctx.send('You need to specifiy a subreddit, pabo. Try again.')
            return
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
                        **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                        url = f'https://www.reddit.com{submission.permalink}')
                        embed.add_field(name = 'Post Content:', value = f'{submission.selftext[:600]}...', inline = False)
                        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed = embed)
                        break
                    else:
                        embed = discord.Embed(title = f'Current Hot Post from r/{subreddit}', color = discord.Colour(0xefe61),
                        description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                        **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                        url = f'https://www.reddit.com{submission.permalink}')
                        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                        embed.timestamp = datetime.datetime.utcnow()

                        link = submission.url
                        linksplit = submission.url.split('.')
                        if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                            embed.set_image(url = f'{submission.url}')
                            await ctx.send(embed = embed)
                            break
                        elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                            url = requests.get(f'{link}')
                            soup = BeautifulSoup(url.text, 'html.parser')
                            directlink = soup.select('link[rel = image_src]')[0]['href']
                            embed.set_image(url = directlink)
                            await ctx.send(embed = embed)
                            break
                        elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                            or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                            or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                            await ctx.send(embed = embed)
                            await ctx.send(f'**Post Content:** {link}')
                            break
                        else:
                            embed.add_field(name = 'Post Content:', value = f'{submission.url}', inline = False)
                            await ctx.send(embed = embed)
                            break

    @commands.command(aliases = ['Reddit_hot_ex', 'rh_ex', 'RH_ex', 'Rh_ex', 'rH_ex'])
    async def reddit_hot_ex(self, ctx):
        await ctx.send("```k.reddit_hot movies\n>>> [Current hot post in r/movies]```")

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the all-time top post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['Reddit_top', 'rt', 'RT', 'Rt', 'rT'])
    async def reddit_top(self, ctx, subreddit, timeframe = None):
        if timeframe is None:
            await ctx.send('Make sure you have all the necessary parameters, pabo. Check `k.reddit_top_ex` for an example.')
            return
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
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
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.add_field(name = 'Post Content:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Top Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Post Content:', value = f'{submission.url}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['Reddit_top_ex', 'rt_ex', 'RT_ex', 'Rt_ex', 'rT_ex'])
    async def reddit_top_ex(self, ctx):
        d = {'Timeframe': ['Hour', 'Day', 'Week', 'Month', 'Year', 'All'], 'Alias': ['h', 'd', 'w', 'm', 'y', 'a']}
        index = [1, 2, 3, 4, 5, 6]
        df = pd.DataFrame(data = d, index = index)
        await ctx.send(f'```Full list of timeframes:\n\n{df}\n\nk.reddit_top jailbreak All \n\
>>> [All-time top post in r/jailbreak]```')

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the newest post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['Reddit_new', 'rn', 'RN', 'Rn', 'rN'])
    async def reddit_new(self, ctx, subreddit = None):
        if subreddit is None:
            await ctx.send('You need to specifiy a subreddit, pabo. Try again.')
            return
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        else:
            newposts = list(reddit.subreddit(f'{subreddit}').new(limit = 1))
            for submission in newposts:
                date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
                if submission.selftext != '':
                    embed = discord.Embed(title = f'Newest Post from r/{subreddit}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.add_field(name = 'Post Content:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Newest Post from r/{subreddit}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Content:', value = f'{submission.url}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['Reddit_new_ex', 'rn_ex', 'RN_ex', 'Rn_ex', 'rN_ex'])
    async def reddit_new_ex(self, ctx):
        await ctx.send('```k.reddit_new books \n>>> [Newest post in r/books]```')

    # Consumes a str, subreddit, which must be a valid SFW subreddit, and a str, timeframe, which must be a valid timeframe (k.rc_ex for full list)
    # Returns the most controversial post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['Reddit_controversial', 'rc', 'RC', 'Rc', 'rC'])
    async def reddit_controversial(self, ctx, subreddit, timeframe = None):
        if timeframe is None:
            await ctx.send('You need to pick a timeframe, pabo. Check `k.reddit_controversial_ex` for a full list.')
            return
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
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
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.add_field(name = 'Post Content:', value = f'{submission.selftext[:300]}...', inline = False)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()
                    await ctx.send(embed = embed)
                    break
                else:
                    embed = discord.Embed(title = f'Most Controversial Post from r/{subreddit} - {timeframe}', color = discord.Colour(0xefe61),
                    description = f'```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                    **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}', 
                    url = f'https://www.reddit.com{submission.permalink}')
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                    embed.timestamp = datetime.datetime.utcnow()

                    link = submission.url
                    linksplit = submission.url.split('.')
                    if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                        embed.set_image(url = f'{submission.url}')
                        await ctx.send(embed = embed)
                        break
                    elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                        url = requests.get(f'{link}')
                        soup = BeautifulSoup(url.text, 'html.parser')
                        directlink = soup.select('link[rel = image_src]')[0]['href']
                        embed.set_image(url = directlink)
                        await ctx.send(embed = embed)
                        break
                    elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                        or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                        or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                        await ctx.send(embed = embed)
                        await ctx.send(f'**Post Content:** {link}')
                        break
                    else:
                        embed.add_field(name = 'Content:', value = f'{submission.url}', inline = False)
                        await ctx.send(embed = embed)
                        break

    @commands.command(aliases = ['Reddit_controversial_ex', 'rc_ex', 'RC_ex', 'Rc_ex', 'rC_ex'])
    async def reddit_controversial_ex(self, ctx):
        d = {'Timeframe': ['Hour', 'Day', 'Week', 'Month', 'Year'], 'Alias': ['h', 'd', 'w', 'm', 'y']}
        index = [1, 2, 3, 4, 5]
        df = pd.DataFrame(data = d, index = index)
        await ctx.send(f'```Full list of timeframes:\n\n{df}\n\nk.reddit_controversial politics Day \n\
>>> [Most controversial post in r/politics within the past day]```')

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the random post from the specified subreddit, generally within the past 5 days if the sub is active. If not, returns a
    #   random post from the most recent posts
    # Only works for subreddits with random on
    @commands.command(aliases = ['Reddit_random', 'rr', 'RR', 'Rr'])
    async def reddit_random(self, ctx, *, subreddit = None):
        if subreddit is None:
            await ctx.send('You need to specifiy a subreddit, pabo. Try again.')
            return
        if reddit.subreddit(f'{subreddit}').over18:
            await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
        else:
            submission = reddit.subreddit(subreddit).random()
            date = str(datetime.datetime.fromtimestamp(submission.created)).replace(' ', ' | ') + ' | ' + 'EST'
            if submission.selftext != '':
                embed = discord.Embed(title = f"Random Post from r/{subreddit}", color = discord.Colour(0xefe61),
                description = f"```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}", 
                url = f'https://www.reddit.com{submission.permalink}')
                embed.add_field(name = 'Contents:', value = f"{submission.selftext[:600]}...", inline = False)
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)
            else:
                embed = discord.Embed(title = f"Random Post from r/{subreddit}", color = discord.Colour(0xefe61),
                description = f"```{submission.title}```\n**Submitted by:** u/{submission.author.name}\n**Date:** {date}\n\
                **Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}",
                url = f'https://www.reddit.com{submission.permalink}')
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
                embed.timestamp = datetime.datetime.utcnow()

                link = submission.url
                linksplit = submission.url.split('.')
                if 'png' in linksplit or 'jpg' in linksplit or 'jpeg' in linksplit or 'jfif' in linksplit:
                    embed.set_image(url = f'{submission.url}')
                    await ctx.send(embed = embed)
                elif ('https://imgur.com/' in link) and ('gif' not in linksplit) and ('gifv' not in linksplit):
                    url = requests.get(f'{link}')
                    soup = BeautifulSoup(url.text, 'html.parser')
                    directlink = soup.select('link[rel = image_src]')[0]['href']
                    embed.set_image(url = directlink)
                    await ctx.send(embed = embed)
                elif 'https://gfycat.com/' in link or 'https://tenor.com/' in link or 'gif' in linksplit or 'gifv' in linksplit\
                    or 'webm' in linksplit or 'mp4' in linksplit or 'mov' in linksplit or 'https://www.youtube.com/' in link\
                    or 'https://youtu.be/' in link or 'https://streamable.com/' in link:
                    await ctx.send(embed = embed)
                    await ctx.send(f'**Post Content:** {link}')
                else:
                    embed.add_field(name = 'Post Content:', value = f'{submission.url}', inline = False)
                    await ctx.send(embed = embed)

    @commands.command(aliases = ['Reddit_random_ex', 'rr_ex', 'RR_ex', 'Rr_ex'])
    async def reddit_random_ex(self, ctx):
        await ctx.send('```k.reddit_random kpics\n>>> [Random post from r/kpics (within the past ~5 days of posts)]```')

    # Consumes query, which must be a valid search on the kpop wiki
    # Returns the profile of the specified query
    @commands.command(aliases = ['Pop', 'kpop', 'Kpop'])
    async def pop(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
        else:
            if 'gidle' in query.lower():
                query = '(G)I-DLE'
            fquery = query.replace(' ', '+').lower()

            url = f'https://kpop.fandom.com/wiki/Special:Search?search={fquery}&fulltext=Search&scope=internal&ns0=1&ns14=1#'
            user_agent = {'User-Agent': 'Mozilla/5.0'}
            searchrequest = requests.get(url, headers = user_agent)
            searchsoup = BeautifulSoup(searchrequest.text, 'html.parser')

            notfound = searchsoup.find('p', {'class': 'no-result'})
            if notfound is not None:
                await ctx.send(f"I couldn't find anything related to `{query}`. Nugu.")
            else:
                message = await ctx.send('*Searching the kpop wiki...*')

                results = searchsoup.find('ul', {'class': 'Results'})
                topresult = results.find('li', {'class': 'result'})
                profilepreview = topresult.find('li')
                profilelink = profilepreview.find('a')['href']

                profilerequest = requests.get(profilelink, headers = user_agent)
                profilesoup = BeautifulSoup(profilerequest.text, 'html.parser')

                groupcategory = profilesoup.find('div', {'class': 'page-header__categories-links'})

                if 'Disambiguations' in groupcategory.text:
                    second = results.find_all('li', {'class': 'result'})[1]
                    sec = second.find('li')
                    link = sec.find('a')['href']
                    profilelink = link
                    profilerequest = requests.get(profilelink, headers = user_agent)
                    profilesoup = BeautifulSoup(profilerequest.text, 'html.parser')
                    groupcategory = profilesoup.find('div', {'class': 'page-header__categories-links'})

                title = profilesoup.find('h1', {'class': 'page-header__title'})
                image = profilesoup.find('figure', {'class': 'pi-item pi-image'})
                infoheaders = profilesoup.find_all('h3', {'class': 'pi-data-label pi-secondary-font'})
                infovalues = profilesoup.find_all('div', {'class': 'pi-data-value pi-font'})
                aside = profilesoup.find('aside')
                
                if 'bts' == query.lower():
                    description = "BTS (Korean: 방탄소년단; Japanese: 防弾少年团; also known as Bangtan Boys and Beyond the Scene)\
                         is a seven-member boy group under Big Hit Entertainment. They debuted on June 13, 2013 with their first \
                             single 2 Cool 4 Skool."
                else:
                    if aside is not None:
                        paragraph = aside.find_next('p')
                        if paragraph is None:
                            description = 'N/A'
                        else:
                            if len(paragraph) > 1:
                                description = paragraph.text.strip()
                            else:
                                description = 'N/A'
                    else:
                        description = 'N/A'

                d = {}
                if infoheaders is not None and infovalues is not None:
                    for header, value in zip(infoheaders, infovalues):
                        d[header.text] = value.text.strip() 
                else:
                    pass

                if title is None:
                    title = query
                else:
                    if 'Hangul' in d.keys():
                        title = title.text.strip() + ' ' + f"({d['Hangul']})"
                    else:
                        title = title.text.strip()

                if image is None:
                    thumbnail = 'https://www.logolynx.com/images/logolynx/97/973922683e2bef373d662c29680247ac.png'
                else:
                    thumbnail = image.find('img')['src']

                if 'Groups' in groupcategory.text or 'Duos' in groupcategory.text or 'Subunits' in groupcategory.text:
                    if 'Debut' in d.keys():
                        value = d['Debut']
                        if ')' in value:
                            debut = value.replace(')', ') | ')[:-2]
                        else:
                            debut = value
                    else:
                        debut = 'N/A'

                    if 'Label(s)' in d.keys():
                        value = d['Label(s)']
                        if ')' in value:
                            labels = value.replace(')', ') | ')[:-2]
                        else:
                            labels = value
                    else:
                        labels = 'N/A'

                    memberlist = []
                    current = profilesoup.find(text = 'Current')
                    if current is not None:
                        firstmember = current.find_next('li')
                        allmembers = firstmember.find_next_siblings('li')
                        memberlist.append(firstmember.text.strip())
                        if allmembers is not None:
                            for i in allmembers:
                                memberlist.append(i.text.strip())
                        members = ', '.join(memberlist)
                    else:
                        members = 'N/A'

                    embeddesc = f"**Debut:** {debut}\n**Label(s):** {labels}\n**Active members:** {members}" 
                    embed = discord.Embed(title = f"Kpop Wiki Search - {title}", colour = discord.Colour(0xefe61), 
                    description = embeddesc, url = profilelink)
                    embed.set_thumbnail(url = thumbnail)
                    embed.add_field(name = 'General Info:', value = description)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(content = '*Searching the kpop wiki... ✅*')
                    await asyncio.sleep(1)
                    await message.delete()
                    await ctx.send(embed = embed)

                elif 'Companies' in groupcategory.text:
                    if 'Founded' in d.keys():
                        value = d['Founded']
                        if ')' in value:
                            founded = value.replace(')', ') | ')[:-2]
                        else:
                            founded = value
                    else:
                        founded = 'N/A'

                    if 'cube' in query.lower():
                        founders = 'Hong Seung Sung, Shin Jung Hwa'
                    else:
                        if 'Founder(s)' in d.keys():
                            founders = d['Founder(s)']
                        else:
                            founders = 'N/A'

                    embeddesc = f"**Founded:** {founded}\n**Founder(s):** {founders}" 
                    embed = discord.Embed(title = f"Kpop Wiki Search - {title}", colour = discord.Colour(0xefe61), 
                    description = embeddesc, url = profilelink)
                    embed.set_thumbnail(url = thumbnail)
                    embed.add_field(name = 'General Info:', value = description)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(content = '*Searching the kpop wiki... ✅*')
                    await asyncio.sleep(1)
                    await message.delete()
                    await ctx.send(embed = embed)

                elif 'Television article stubs' in groupcategory.text or 'Survival shows' in groupcategory.text:
                    if 'Episodes' in d.keys():
                        episodes = d['Episodes']
                    else:
                        episodes = 'N/A'

                    if 'Running time' in d.keys():
                        runtime = d['Running time']
                    else:
                        runtime = 'N/A'

                    if 'Network' in d.keys():
                        network = d['Network']
                    else:
                        network = 'N/A'

                    embeddesc = f"**Episodes:** {episodes}\n**Runtime:** {runtime}\n**Network:** {network}" 
                    embed = discord.Embed(title = f"Kpop Wiki Search - {title}", colour = discord.Colour(0xefe61), 
                    description = embeddesc, url = profilelink)
                    embed.set_thumbnail(url = thumbnail)
                    embed.add_field(name = 'General Info:', value = description)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(content = '*Searching the kpop wiki... ✅*')
                    await asyncio.sleep(1)
                    await message.delete()
                    await ctx.send(embed = embed)
                
                elif 'Discography' in groupcategory.text or 'Albums' in groupcategory.text or 'singles' in groupcategory.text.lower():
                    if 'Artist' in d.keys():
                        artist = d['Artist']
                    else:
                        artist = 'N/A'

                    if 'Length' in d.keys():
                        value = d['Length']
                        if value.count(':') > 1:
                            index = []
                            for i in list(range(len(value))):
                                if value[i] == ':':
                                    index.append(i)
                            counter = 0
                            for i in index[1:]:
                                if counter > 0:
                                    i += counter * 3
                                length = value[:i-2] + ' | ' + value[i-2:]
                                value = length
                                counter += 1
                        else:
                            length = value
                    else:
                        length = 'N/A'

                    if 'Released' in d.keys():
                        value = d['Released']
                        if value.count(',') > 1:
                            index = []
                            for i in list(range(len(value))):
                                if value[i] == ',':
                                    index.append(i)
                            counter = 0
                            for i in index[1:]:
                                if counter > 0:
                                    i += counter * 3
                                reverse = value[:i-3][::-1]
                                for j in list(range(len(reverse))):
                                    if reverse[j].isnumeric() or reverse[j] == ')':
                                        pos = j
                                        break
                                breakpos = len(value[:i-3]) - pos
                                release = value[:breakpos] + ' | ' + value[breakpos:]
                                value = release
                                counter += 1
                        else:
                            release = value
                    else:
                        release = 'N/A'

                    if 'Label(s)' in d.keys():
                        labels = d['Label(s)']
                    else:
                        labels = 'N/A'

                    tlist = profilesoup.find(text = 'Track list')
                    if tlist is None:
                        fulltracks = 'N/A'
                    else:
                        ol = tlist.find_next('ol')
                        if ol is None:
                            fulltracks = 'N/A'
                        else:
                            tracklist = ol.find_all('li')
                            if tracklist is None:
                                fulltracks = 'N/A'
                            else:
                                tracks = []
                                counter = 1
                                for i in tracklist:
                                    tracks.append(f"{counter}. {i.text.strip()}")
                                    counter += 1
                                fulltracks = '\n'.join(tracks)
                            
                    embeddesc = f"**Artist:** {artist}\n**Release date:** {release}\n**Length:** {length}\n**Label(s):** {labels}" 
                    embed = discord.Embed(title = f"Kpop Wiki Search - {title}", colour = discord.Colour(0xefe61), 
                    description = embeddesc, url = profilelink)
                    embed.add_field(name = 'Tracklist:', value = fulltracks)
                    embed.add_field(name = 'General Info:', value = description)
                    embed.set_thumbnail(url = thumbnail)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(content = '*Searching the kpop wiki... ✅*')
                    await asyncio.sleep(1)
                    await message.delete()
                    await ctx.send(embed = embed)

                else:
                    if 'Birth date' in d.keys():
                        DOB = d['Birth date']
                    else:
                        DOB = 'N/A'

                    stats = []
                    if 'Height' in d.keys():
                        stats.append(d['Height'])
                    else:
                        stats.append('N/A')
                    if 'Weight' in d.keys():
                        stats.append(d['Weight'])
                    else:
                        stats.append('N/A')
                    heightweight = ' | '.join(stats)

                    if 'Solo debut' in d.keys():
                        value = d['Solo debut']
                        if ')' in value:
                            solodebut = value.replace(')', ') | ')[:-2]
                        else:
                            solodebut = value
                    else:
                        solodebut = 'N/A'

                    if 'Agency' in d.keys():
                        value = d['Agency']
                        if ')' in value:
                            company = value.replace(')', ') | ')[:-2]
                        else:
                            company = value
                    else:
                        company = 'N/A'

                    grouplist = []
                    associations = profilesoup.find(text = 'Associations')
                    if associations is not None:
                        firstgroup = associations.find_next('a')
                        allgroups = firstgroup.find_next_siblings('a')
                        grouplist.append(firstgroup.text.strip())
                        if allgroups is not None:
                            for i in allgroups:
                                grouplist.append(i.text.strip())
                        groups = ', '.join(grouplist)
                    else:
                        groups = 'N/A'

                    embeddesc = f"**DOB:** {DOB}\n**Stats:** {heightweight}\n**Solo debut:** {solodebut}\n**Company:** {company}\n\
                        **Associated with:** {groups}" 
                    embed = discord.Embed(title = f"Kpop Wiki Search - {title}", colour = discord.Colour(0xefe61), 
                    description = embeddesc, url = profilelink)
                    embed.set_thumbnail(url = thumbnail)
                    embed.add_field(name = 'General Info:', value = description)
                    embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                    embed.timestamp = datetime.datetime.utcnow()

                    await message.edit(content = '*Searching the kpop wiki... ✅*')
                    await asyncio.sleep(1)
                    await message.delete()
                    await ctx.send(embed = embed)

    @commands.command(aliases = ['Pop_ex', 'kpop_ex', 'Kpop_ex'])
    async def pop_ex(self, ctx):
        await ctx.send('```This command can retrieve data from (most) groups, soloists, individual members, entertainment companies, \
discographies, and kpop-related television shows. Everything is pulled directly from the Kpop Wiki.\n\n\
k.pop Red Velvet\n>>> [Information about Red Velvet]```')

    # Consumes query, which must be a valid group/soloist on Kprofiles (works for some group members as well)
    # Returns the profile of the specified query
    @commands.command(aliases = ['Profile', 'profiles', 'Profiles', 'pro', 'Pro'])
    async def profile(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
        else:
            if query.lower() == 'blackpink':
                await ctx.send('https://kprofiles.com/black-pink-members-profile/')
            if query.lower() == 'bts':
                await ctx.send('https://kprofiles.com/bts-bangtan-boys-members-profile/')
            if query.lower() == 'leebada':
                await ctx.send('https://kprofiles.com/lee-ba-da-profile-facts/')
            else:
                message = await ctx.send('*Searching KProfiles...*')

                gg = requests.get('https://kprofiles.com/k-pop-girl-groups/')
                bg = requests.get('https://kprofiles.com/k-pop-boy-groups/')
                solo = requests.get('https://kprofiles.com/kpop-solo-singers/')
                gg_soup = BeautifulSoup(gg.text, 'html.parser')
                bg_soup = BeautifulSoup(bg.text, 'html.parser')
                solo_soup = BeautifulSoup(solo.text, 'html.parser')
                gg_links = gg_soup.findAll('a')
                bg_links = bg_soup.findAll('a')
                solo_links = solo_soup.findAll('a')

                x = False
                for link in gg_links:
                    link = str(link).split('"')
                    last = link[-1]
                    new = last[1:(len(last) - 4)]
                    if query.lower() == new.lower():
                        x = True
                        await message.edit(content = '*Searching KProfiles... ✅*')
                        await asyncio.sleep(1)
                        await message.delete()
                        await ctx.send(link[1])
                        return
                for link in bg_links:
                    link = str(link).split('"')
                    last = link[-1]
                    new = last[1:(len(last) - 4)]
                    if query.lower() == new.lower():
                        x = True
                        await message.edit(content = '*Searching KProfiles... ✅*')
                        await asyncio.sleep(1)
                        await message.delete()
                        await ctx.send(link[1])
                        return
                for link in solo_links:
                    link = str(link).split('"')
                    last = link[-1]
                    new = last[1:(len(last) - 4)]
                    if query.lower() == new.lower():
                        x = True
                        await message.edit(content = '*Searching KProfiles... ✅*')
                        await asyncio.sleep(1)
                        await message.delete()
                        await ctx.send(link[1])
                        return

                if not x:
                    await message.delete()
                    await ctx.send(f"I wasn't able to find anything related to `{query}` on Kprofiles. Nugu.")

    @commands.command(aliases = ['Profile_ex', 'profiles_ex', 'Profiles_ex', 'pro_ex', 'Pro_ex'])
    async def profile_ex(self, ctx):
        await ctx.send('```k.profile Red Velvet\n>>> https://kprofiles.com/irene-facts-profile-irene-ideal-type/```')

    # Consumes amount, an int between 1-25, and location, which must be a valid location (see WOEIDs.md for full list)
    # Returns a dataframe of the trending topics on Twitter according to the specified amount and location
    @commands.command(aliases = ['Twitter_trends', 'twt', 'Twt', 'twitter_trending', 'Twitter_trending'])
    async def twitter_trends(self, ctx, amount, *, location = None):
        if location is None:
            await ctx.send('Make sure you have all the necessary parameters, pabo. Check `k.twitter_trends_ex` for an example.')
            return
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
    async def twitter_graph(self, ctx, amount, *, location = None):
        if location is None:
            await ctx.send('Make sure you have all the necessary parameters, pabo. Check `k.twitter_graph_ex` for an example.')
            return
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
    async def stock(self, ctx, ticker, timeframe = None):
        if timeframe is None:
            await ctx.send('Make sure you have all the necessary parameters, pabo. Check `k.stock_ex` for an example.')
            return
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
            await ctx.send("You need to specify an artist, pabo. Try again, and make sure it's a valid artist on the charts. \
For a full list, check the `All` dropdown menu from <http://www.kpopchart.kr/?a=>.")
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

    # Consumes query, any type
    # Returns the most relevant searche on YouTube of the specified query    
    @commands.command(aliases = ['Youtube_top', 'yt', 'Yt', 'YT'])
    async def youtube_top(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
        else:
            fquery = query.replace(' ', '+')
            url = f'https://www.googleapis.com/youtube/v3/search?q={fquery}&key={API_KEY}'
            request = requests.get(url)
            d = json.loads(request.text)

            for i in d['items']:
                if i['id']['kind'] == 'youtube#channel' or i['id']['kind'] == 'youtube#playlist':
                    continue
                elif i['id']['kind'] == 'youtube#video':
                    vidID = i['id']['videoId']
                    await ctx.send(f'https://www.youtube.com/watch?v={vidID}')
                    return
                else:
                    await ctx.send(f"Unable to search for `{query}`. Sorry, bro.")

    @commands.command(aliases = ['Youtube_top_ex', 'yt_ex', 'Yt_ex', 'YT_ex'])
    async def youtube_top_ex(self, ctx):
        await ctx.send("```The k.youtube_search and k.youtube_top commands both have a maximum of 100 uses (combined) \
per 24 hours due to API limitations. Thus, please don't spam these commands. If your query is valid and nothing gets returned after ~15 seconds, \
it's safe to assume the API limit has been reached for the day. If you're unsure, you can ping me, and I'll check.\n\n\
k.youtube_top Red Velvet\n>>>[Most relevant on YouTube of Red Velvet]```")

    # Consumes query, any type
    # Returns the top 5 relevant searches on YouTube of the specified query
    @commands.command(aliases = ['Youtube_search', 'yt_search', 'Yt_search', 'yts', 'Yts', 'YTS'])
    async def youtube_search(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
        else:
            fquery = query.replace(' ', '+')
            url = f'https://www.googleapis.com/youtube/v3/search?part=snippet&q={fquery}&key={API_KEY}'
            request = requests.get(url)
            d = json.loads(request.text)

            embed = discord.Embed(title = f"YouTube Search - {query}", color = discord.Colour(0xefe61))
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')           
            embed.timestamp = datetime.datetime.utcnow()

            L = []
            for i in d['items']:
                L.append(i['id']['kind'])

            x = False
            for i in d['items']:
                if i['id']['kind'] == 'youtube#channel':
                    channelID = i['id']['channelId']
                    channellink = f"https://www.youtube.com/channel/{channelID}"
                    channelthumbnail = i['snippet']['thumbnails']['default']['url']
                    timestamp = i['snippet']['publishedAt'].replace('Z', '').replace('T', ' | ')
                    channeltitle = i['snippet']['title'].replace("&#39;", "'").replace('&quot;', '"')
                    
                    if len(channeltitle) > 245:
                        channeltitle = channeltitle[:245] + '...'

                    if not x:
                        embed.set_thumbnail(url = channelthumbnail)
                        x = True

                    embed.add_field(name = f'\u200b',
                    value = f"**[{channeltitle}]({channellink})**\n**Created on:** {timestamp}", inline = False)
                elif i['id']['kind'] == 'youtube#playlist':
                    playlistIDfront = i['snippet']['thumbnails']['default']['url'].split('/')[4]
                    playlistIDback = i['id']['playlistId']
                    playlistlink = f"https://www.youtube.com/watch?v={playlistIDfront}&list={playlistIDback}"
                    playlistthumbnail = i['snippet']['thumbnails']['default']['url']
                    timestamp = i['snippet']['publishedAt'].replace('Z', '').replace('T', ' | ')
                    channeltitle = i['snippet']['channelTitle']
                    playlisttitle = i['snippet']['title'].replace("&#39;", "'").replace('&quot;', '"')

                    if len(playlisttitle) > 245:
                        playlisttitle = playlisttitle[:245] + '...'

                    if 'youtube#channel' not in L and not x:
                        embed.set_thumbnail(url = playlistthumbnail)
                        x = True

                    embed.add_field(name = f'\u200b',
                    value = f"**[{playlisttitle}]({playlistlink})**\n**Uploaded to:** {channeltitle} on {timestamp}", inline = False)
                elif i['id']['kind'] == 'youtube#video':
                    vidID = i['id']['videoId']
                    videolink = f'https://www.youtube.com/watch?v={vidID}'
                    videothumbnail = i['snippet']['thumbnails']['default']['url']
                    timestamp = i['snippet']['publishedAt'].replace('Z', '').replace('T', ' | ')
                    channeltitle = i['snippet']['channelTitle']
                    videotitle = i['snippet']['title'].replace("&#39;", "'").replace('&quot;', '"')

                    if len(videotitle) > 245:
                        videotitle = videotitle[:245] + '...'

                    if 'youtube#channel' not in L and not x:
                        embed.set_thumbnail(url = videothumbnail)
                        x = True

                    embed.add_field(name = f'\u200b',
                    value = f"**[{videotitle}]({videolink})**\n**Uploaded to:** {channeltitle} on {timestamp}", inline = False)
                else:
                    continue

            await ctx.send(embed = embed)

    @commands.command(aliases = ['Youtube_search_ex', 'yt_search_ex', 'Yt_search_ex', 'yts_ex', 'Yts_ex', 'YTS_ex'])
    async def youtube_search_ex(self, ctx):
        await ctx.send("```The k.youtube_search and k.youtube_top commands both have a maximum of 100 uses (combined) \
per 24 hours due to API limitations. Thus, please don't spam these commands. If your query is valid and nothing gets returned after ~15 seconds, \
it's safe to assume the API limit has been reached for the day. If you're unsure, you can ping me, and I'll check.\n\n\
k.youtube_search Red Velvet\n>>>[Top 5 videos/channels/playlists on YouTube of Red Velvet]```")

    @commands.command(aliases = ['Wotd', 'daily_word', 'Daily_word', 'dailyword', 'Dailyword'])
    async def wotd(self, ctx):
        url = 'https://www.merriam-webster.com/word-of-the-day'
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        word = soup.find('h1').text.capitalize()
        wordtype = soup.find('span', {'class': 'main-attr'}).text.capitalize()
        wordpronoun = soup.find('span', {'class': 'word-syllables'}).text
        definition = soup.find('p').text[2:]
        wotdexample = soup.find('div', {'class': 'wotd-examples'})
        example = wotdexample.find('p').text
        didyouknow = soup.find('div', {'class': 'left-content-box'})
        moreinfo = didyouknow.find('p').text

        if len(example) > 300:
            example = example[:295] + '...'
        if len(moreinfo) > 300:
            moreinfo = moreinfo[:295] + '...'

        embed = discord.Embed(title = f"Word of the Day: {word}", color = discord.Colour(0xefe61),
        description = f"{wordtype} | ({wordpronoun})", url = url)
        embed.add_field(name = 'Definition:', value = definition, inline = False)
        embed.add_field(name = 'Example Sentence:', value = example, inline = False)
        embed.add_field(name = 'Did You Know?', value = moreinfo, inline = False)
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.send(embed = embed)

    @commands.command(aliases = ['Urban', 'urb', 'Urb'])
    async def urban(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
        else:
            fquery = query.replace(' ', '+')
            url = f'https://www.urbandictionary.com/define.php?term={fquery}'
            request = requests.get(url)
            soup = BeautifulSoup(request.text, 'html.parser')
            definition = soup.find('div', {'class': 'meaning'})

            if definition is None:
                await ctx.send(f"I couldn't find any definitions related to `{query}`. Nugu.")
                return
                
            example = soup.find('div', {'class': 'example'})
            contributor = soup.find('div', {'class': 'contributor'})
            upvotes = soup.find('a', {'class': 'up'})
            downvotes = soup.find('a', {'class': 'down'})

            if len(definition) > 600:
                definition = definition[:595] + '...'
            if len(example) > 600:
                example = example[:595] + '...'

            embed = discord.Embed(title = f"Urban Dictionary - {query}", color = discord.Colour(0xefe61), 
            description = f"*{contributor.text}*", url = url)
            embed.add_field(name = 'Definition:', value = definition.text, inline = False)
            embed.add_field(name = 'Example:', value = example.text, inline = False)
            embed.add_field(name = 'Score:', value = f'👍 {upvotes.text} | 👎 {downvotes.text}', inline = False)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            await ctx.send(embed = embed)

    @commands.command(aliases = ['Urban_ex', 'urb_ex', 'Urb_ex'])
    async def urban_ex(self, ctx):
        await ctx.send('```k.urban bae joohyun\n>>> [Urban Dictionary definiton of bae joohyun]```')

    # Consumes query, a string 
    # Returns the novel that is the closest match to the specified query
    @commands.command(aliases = ['Book'])
    async def book(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
            return
        fquery = query.replace(' ', '%20').replace("'", '%27').replace('"', '%22').replace('?', '%3F').replace(',', '%2C')
        url = f'https://www.googleapis.com/books/v1/volumes?q={fquery}&maxResults=1&key={API_KEY}' 
        request = requests.get(url)
        d = json.loads(request.text)
        if d['totalItems'] == 0:
            await ctx.send(f'Sorry, but `{query}` is too nugu. Try again.')
        else:

            book = d['items'][0]['volumeInfo']
            bookkeys = book.keys()

            if 'title' not in bookkeys or 'infoLink' not in bookkeys:
                await ctx.send(f'Sorry, but `{query}` is too nugu. Try again.')
            else:
                title = book['title']
                author = 'N/A'
                publisher = 'N/A'
                date = 'N/A'
                thumbnail = 'https://books.google.ca/googlebooks/images/no_cover_thumb.gif'
                summary = 'N/A'
                pagecount = 'N/A'
                rating = '-'
                ratingscount = '-'
                language = 'N/A'
                link = book['infoLink']

                if 'authors' in bookkeys:
                    author = ', '.join(book['authors'])
                if 'publisher' in bookkeys:
                    publisher = book['publisher']
                if 'publishedDate' in bookkeys:
                    date = book['publishedDate']
                if 'imageLinks' in bookkeys:
                    if 'thumbnail' in book['imageLinks'].keys():
                        thumbnail = book['imageLinks']['thumbnail']
                if 'description' in bookkeys:
                    summary = book['description']
                if 'pageCount' in bookkeys:
                    pagecount = book['pageCount']
                if 'averageRating' in bookkeys:
                    rating = book['averageRating']
                if 'ratingsCount' in bookkeys:
                    ratingscount = book['ratingsCount']
                if 'language' in bookkeys:
                    language = book['language'].upper()

                if len(summary) > 800:
                    summary = summary[:800] + '...'

                embed = discord.Embed(title = f"Book Search: {title}", colour = discord.Colour(0xefe61), description = f"By: *{author}*\n\
                Published by: *{publisher}* on {date}", url = link)
                embed.set_thumbnail(url = thumbnail)
                embed.add_field(name = 'Summary:', value = summary, inline = False)
                embed.add_field(name = 'Page Count:', value = f'{pagecount} pages')
                embed.add_field(name = 'Average Rating:', value = f'⭐ {rating}/5 | {ratingscount} ratings')
                embed.add_field(name = 'Language:', value = language)
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()
                
                await ctx.send(embed = embed)

    @commands.command(aliases = ['Book_ex', 'read_ex', 'Read_ex'])
    async def book_ex(self, ctx):
        await ctx.send('```k.book Harry Potter and the Deathly Hallows\n>>> [Information about Harry Potter and the Deathly Hallows]```')

    # Consumes query, which must be a string of len three minimum
    # Returns relevant kpop servers according to the specified query
    @commands.command(aliases = ['Si', 'ksi', 'Ksi'])
    async def si(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
            return
        if len(query) <= 2:
            await ctx.send(f"Be a little more specific in your search, pabo. Three characters minimum.")
        else:
            fin = open('Saved/ServerLinks.txt', encoding = 'utf8')
            line = fin.readline()
            L = []
            x = False
            while line != '':
                start = line.find('http')
                name = line[:(start - 2)]
                if query.lower() in name.lower():
                    x = True
                    L.append(line)
                    line = fin.readline()
                else:
                    line = fin.readline()
            fin.close()

            if not x:
                await ctx.send(f"I couldn't find any servers related to `{query}`. Nugu.")
            else:
                description = f'*Servers Found: {len(L)}*' + '\n\n' + '\n'.join(L)
                embed = discord.Embed(title = f"Kpop Server Search - {query}", colour = discord.Colour(0xefe61), description = description)
                embed.set_thumbnail(url = 'https://cdn.discordapp.com/icons/265901004548079626/f6da337e987069fa8f6b50f395874c6b.png?size=512')
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed = embed)

    @commands.command(aliases = ['Si_ex', 'ksi_ex', 'Ksi_ex'])
    async def si_ex(self, ctx):
        await ctx.send('```k.si Red Velvet\n>>> [Kpop servers related to Red Velvet]```')

    # Consumes query, which must be a valid query
    # Returns information from Steam about the most relevant search to the specified query
    @commands.command(aliases = ['Steam', 'game', 'Game'])
    async def steam(self, ctx, *, query = None):
        if query is None:
            await ctx.send('You need to specify a query, pabo. Try again.')
            return
        fquery = query.replace(' ', '+').lower()
        url = f'https://store.steampowered.com/search/?term={fquery}'
        user_agent = {'User-Agent': 'Mozilla/5.0'}
        searchrequest = requests.get(url, headers = user_agent)
        searchsoup = BeautifulSoup(searchrequest.text, 'html.parser')
        topsearch = searchsoup.find('div', {'id': 'search_resultsRows'})

        if topsearch is None:
            await ctx.send(f"I couldn't find anything in Steam related to `{query}`. Nugu.")
        else:
            message = await ctx.send('*Searching Steam...*')
            
            pagelink = topsearch.find('a')['href']
            inforequest = requests.get(pagelink)
            infosoup = BeautifulSoup(inforequest.text, 'html.parser')

            name = infosoup.find('div', {'class': 'apphub_AppName'})
            image = infosoup.find('img', {'class': 'game_header_image_full'})['src'] 
            summary = infosoup.find('div', {'class': 'game_description_snippet'})
            price = infosoup.find('div', {'class': 'game_purchase_price'})
            discountpct = infosoup.find('div', {'class': 'discount_pct'})
            discountOG = infosoup.find('div', {'class': 'discount_original_price'})
            discountfinal = infosoup.find('div', {'class': 'discount_final_price'})
            ratings_dev = infosoup.find_all('div', {'class', 'summary column'}) 
            metacritic = infosoup.find('div', {'id': 'game_area_metascore'})
            genreblock = infosoup.find('div', {'class': 'block_content_inner'})
            genre_release = genreblock.find('div', {'class': 'details_block'}) 

            if name is None:
                name = query
            else:
                name = name.text.strip()
            if image is None:
                image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/83/Steam_icon_logo.svg/1200px-Steam_icon_logo.svg.png'
            if summary is None:
                summary = 'N/A'
            else:
                summary = summary.text.strip()

            if price is None:
                price = 'N/A'
            else:
                CDNprice = float(price.text.strip()[5:])
                conversion = float(fxp().get_rate('CAD', 'USD'))
                USDprice = '{:.2f}'.format(CDNprice * conversion)
                price = 'USD$' + ' ' + USDprice

            if discountpct is None and discountOG is None and discountfinal is None:
                pass
            if discountpct is not None and discountOG is not None and discountfinal is not None:
                CDNpriceOG = float(discountOG.text.strip()[5:])
                CDNpricefinal = float(discountfinal.text.strip()[5:])
                conversion = float(fxp().get_rate('CAD', 'USD'))
                USDpriceOG = '{:.2f}'.format(CDNpriceOG * conversion)
                USDpricefinal = '{:.2f}'.format(CDNpricefinal * conversion)
                discountOG = 'USD$' + ' ' + USDpriceOG
                discountfinal = 'USD$' + ' ' + USDpricefinal
                price = f"{discountpct.text.replace('-', '')} off! ➞ ~~{discountOG}~~ **{discountfinal}**"

            if metacritic is None:
                metascore = ''
            else:
                metascore = int(metacritic.find('div', {'class': 'score'}).text.strip())
                if metascore >= 90:
                    metascore = f'🌟 {metascore} Metacritic'
                elif metascore >= 80:
                    metascore = f'⭐ {metascore} Metacritic'
                elif metascore >= 70:
                    metascore = f'✅ {metascore} Metacritic'
                elif metascore >= 60:
                    metascore = f'👌 {metascore} Metacritic'
                elif metascore >= 50:
                    metascore = f'👎 {metascore} Metacritic'
                elif metascore >= 30:
                    metascore = f'❌ {metascore} Metacritic'
                elif metascore >= 10:
                    metascore = f'⛔ {metascore} Metacritic'
                elif metascore >= 0:
                    metascore = f'🖕 {metascore} Metacritic'
                else:
                    await ctx.send(f'An unexpected error has occurred. FIX IT <@496181635952148483>.')
                    return

            ratingslist = []
            devpublist = []
            for i in ratings_dev:
                replaced = i.text.replace('\t', '').replace('\r', '').replace('\n\n', '').replace('\n', '')
                ratingonly = replaced.split('-')[0]
                ratingsinfo = ' ('.join(ratingonly.split('('))
                if 'No user reviews' in ratingsinfo:
                    continue
                elif 'Overwhelmingly Positive' in ratingsinfo:
                    ratingslist.append(f'🌟 {ratingsinfo}')
                elif 'Very Positive' in ratingsinfo:
                    ratingslist.append(f'⭐ {ratingsinfo}')
                elif 'Positive' in ratingsinfo and 'Overwhelmingly Positive' not in ratingsinfo and 'Very Positive' not in ratingsinfo and \
                    'Mostly Positive' not in ratingsinfo:
                    ratingslist.append(f'✅ {ratingsinfo}')
                elif 'Mostly Positive' in ratingsinfo:
                    ratingslist.append(f'👍 {ratingsinfo}')
                elif 'Mixed' in ratingsinfo:
                    ratingslist.append(f'👌 {ratingsinfo}')
                elif 'Mostly Negative' in ratingsinfo:
                    ratingslist.append(f'👎 {ratingsinfo}')
                elif 'Negative' in ratingsinfo and 'Overwhelmingly Negative' not in ratingsinfo and 'Very Negative' not in ratingsinfo and \
                    'Mostly Negative' not in ratingsinfo:
                    ratingslist.append(f'❌ {ratingsinfo}')
                elif 'Very Negative' in ratingsinfo:
                    ratingslist.append(f'⛔ {ratingsinfo}')
                elif 'Overwhelmingly Negative' in ratingsinfo:
                    ratingslist.append(f'🖕 {ratingsinfo}')
                else:
                    devpublist.append(i.text.strip())

            if len(ratingslist) == 2:
                ratingsrecent = f'{ratingslist[0]} - Recent'
                ratingsall = f'{ratingslist[1]} - All'
                ratingslist.clear()
                ratingslist.append(ratingsrecent)
                ratingslist.append(ratingsall)
                fratings = '\n'.join(ratingslist)
            elif len(ratingslist) == 1:
                ratingsall = f'{ratingslist[0]} - All'
                ratingslist.clear()
                ratingslist.append(ratingsall)
                fratings = '\n'.join(ratingslist)
            else:
                fratings = 'N/A'
            
            if len(devpublist) == 2 or len(devpublist) == 1:
                fdevpub = '\n'.join(devpublist)
            else:
                fdevpub = 'N/A'

            lst = list(filter(lambda x: x != '', genre_release.text.split('\n')))
            genreleaselist = []
            for i in lst:
                if 'Genre:' in i or 'Release Date:'in i:
                    i = i.split(': ')
                    tab = f"**{i[0]}**: {i[1]}"
                    genreleaselist.append(tab)
            fgenre_release = '\n'.join(genreleaselist)

            await message.edit(content = '*Searching Steam... ✅*')

            description = f"**Price:** {price}\n{fgenre_release}"
            embed = discord.Embed(title = f"Steam Search - {name}", colour = discord.Colour(0xefe61), 
            description = description, url = pagelink)
            embed.add_field(name = 'Description:', value = summary, inline = False)
            embed.add_field(name = 'Ratings:', value = f'{fratings}' + '\n' + metascore)
            embed.add_field(name = 'Developer | Publisher:', value = fdevpub)
            embed.set_thumbnail(url = image)
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}', icon_url = 'https://i.imgur.com/CuNlLOP.png')
            embed.timestamp = datetime.datetime.utcnow()

            await asyncio.sleep(1)
            await message.delete()
            await ctx.send(embed = embed)

    @commands.command(aliases = ['Steam_ex', 'game_ex', 'Game_ex'])
    async def steam_ex(self, ctx):
        await ctx.send('```k.steam GTA Vice City\n>>> [Information from Steam about GTA Vice City]```')


def setup(bot):
    bot.add_cog(Data_Cog(bot))
