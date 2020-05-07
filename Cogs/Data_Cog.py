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
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = 'https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')
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
    @commands.command(aliases = ['rh', 'RH', 'Rh', 'rH'])
    async def reddit_hot(self, ctx, subreddit):
        for submission in reddit.subreddit(f'{subreddit}').hot(limit=1):
            if reddit.subreddit(f'{subreddit}').over18:
                await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
            else:
                await ctx.send(f'```{submission.title}```\n**Submitted by:** u/*{submission.author.name}* to r/{subreddit}\n\
**Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                await ctx.send('https://www.reddit.com' + submission.permalink)

    @commands.command(aliases = ['rh_ex', 'RH_ex', 'Rh_ex', 'rH_ex'])
    async def reddit_hot_ex(self, ctx):
        await ctx.send("```k.reddit_hot movies\n>>> Hi! I'm Jeff Orlowski, director of the documentaries Chasing Coral...```")

    # Consumes a str, subreddit, which must be a valid SFW subreddit
    # Returns the all-time top post from the specified subreddit, along with submission author, flair, score, and amount of comments
    @commands.command(aliases = ['rt', 'RT', 'Rt', 'rT'])
    async def reddit_top(self, ctx, subreddit):
        for submission in reddit.subreddit(f'{subreddit}').top(limit=1):
            if reddit.subreddit(f'{subreddit}').over18:
                await ctx.send(f"**r/{subreddit}** is NSFW. Choose an SFW one, pabo. We aren't about breaking rool2 in here, smh.")
            else:
                await ctx.send(f'```{submission.title}```\n**Submitted by:** u/*{submission.author.name}* to r/{subreddit}\n\
**Flair:** {submission.link_flair_text}\n**Score:** {submission.score} karma\n**Comments:** {submission.num_comments}')
                await ctx.send('https://www.reddit.com' + submission.permalink)

    @commands.command(aliases = ['rt_ex', 'RT_ex', 'Rt_ex', 'rT_ex'])
    async def reddit_top_ex(self, ctx):
        await ctx.send('```k.reddit_top jailbreak \n>>> [Release] Introducing checkm8 (read "checkmate"), a permanent unpatchable...```')

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
If nothing is returned after ~15 seconds, it's safe to assume either the group/soloist requested is invalid or something else has gone wrong..\n\n\
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
If nothing is returned after ~15 seconds, it's safe to assume either the location requested is invalid or something else has gone wrong..\n\n\
k.twitter_trends 10 Worldwide\n>>> [10 trending topics on Twitter - Worldwide]\n\n\
k.twitter_trends 25 Canada\n>>> [25 trending topics on Twitter in Canada]```\n\
Full Location List: https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md")

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
                embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
                icon_url = 'https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')
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
If nothing is returned after ~20 seconds, it's safe to assume either the location requested is invalid or something else has gone wrong..\n\n\
k.twitter_graph 10 Worldwide\n>>> [Graph of tweet volume of 10 trending topics - Worldwide]\n\n\
k.twitter_graph 25 Canada\n>>> [Graph of tweet volume of 10 trending topics in Canada]```\n\
Full Location List: https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/WOEIDs.md")

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
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = 'https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')
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
            
            embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
            icon_url = 'https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')
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
        embed.set_footer(text = f'KaiserBot | {ctx.guild.name}',
        icon_url = 'https://cdn.discordapp.com/attachments/630633322686578689/699425742752317490/KaiserBotcircular.png')
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
has been reached, or something else has gone wrong..\n\n\
k.stock AAPL long\n>>> [Graph of AAPL stock - Historic data (yearly)]\n\n\
k.stock NVDA medium\n>>> [Graph of NVDA stock - Historic data (monthly)]\n\n\
k.stock 182360.KQ short\n>>> [Graph of Cube Entertainment stock - Recent]```\n\
To pull data from outside the USA, please read this info page: https://github.com/Kaiserrollii/KaiserBot/blob/master/Cogs/StockInfo.md")


def setup(bot):
    bot.add_cog(Data_Cog(bot))