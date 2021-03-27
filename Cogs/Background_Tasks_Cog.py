import discord
import asyncio
import random
import requests
from bs4 import BeautifulSoup
from discord.ext import commands 


class Background_Tasks_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.status())
        self.bg_task = self.bot.loop.create_task(self.daily_affirmation())
        self.bg_task = self.bot.loop.create_task(self.daily_bible())
        self.bg_task = self.bot.loop.create_task(self.daily_ariana_quote())

    @commands.Cog.listener()
    async def on_ready(self):
        print ('Background_Tasks: Online')

    async def status(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(630633322686578689)
        while not self.bot.is_closed():
            await channel.send('**Status:** Online')
            await channel.send(f'{len(self.bot.guilds)} | {len(self.bot.users)}')
            await asyncio.sleep(3600) 

    # Sends a daily affirmation into #the-spa every 24h
    async def daily_affirmation(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(627970443361648685)
        while not self.bot.is_closed():

            url = 'https://www.developgoodhabits.com/positive-affirmations/'
            user_agent = {'User-Agent': 'Mozilla/5.0'}

            response = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(response.text, 'html.parser')
            affirms = list(soup.find_all('em'))
            text = list(map(lambda x: x.text, affirms))

            await channel.send(f'{random.choice(text)}')
            await asyncio.sleep(86400) 

    # Sends a daily bible quote into #the-spa every 24h
    async def daily_bible(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(627970443361648685)
        while not self.bot.is_closed():

            user_agent = {'User-Agent': 'Mozilla/5.0'}
            url = requests.get('https://www.verseoftheday.com/', user_agent)
            soup = BeautifulSoup(url.text, 'html.parser')
            verse = soup.find('div', {'class': 'bilingual-left'})
            formatted = ''.join(verse.text.replace('—', '\n- '))

            await channel.send(f'**Daily Bible Verse:**\n{formatted}')
            await asyncio.sleep(86400)

    # Sends a daily Ariana Grande quote into #ariana-chat every 24h
    # As per request from Aricord
    async def daily_ariana_quote(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(778771519362957342)
        while not self.bot.is_closed():

            url = 'https://quotes.thefamouspeople.com/ariana-grande-15637.php'
            user_agent = {'User-Agent': 'Mozilla/5.0'}

            response = requests.get(url, headers = user_agent)
            soup = BeautifulSoup(response.text, 'html.parser')
            quotes = soup.find_all('div', {'class': 'quote'})
            random_quote = random.choice(quotes)
            processed = random_quote.find('q').text

            await channel.send(f'**Daily Ariana Quote:**\n{processed}')
            await asyncio.sleep(86400)


def setup(bot):
    bot.add_cog(Background_Tasks_Cog(bot))
