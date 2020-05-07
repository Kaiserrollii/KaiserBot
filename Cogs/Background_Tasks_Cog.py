import discord
import asyncio
import random
from discord.ext import commands 


class Background_Tasks_Cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.bg_task = self.bot.loop.create_task(self.chat_revive())

    @commands.Cog.listener()
    async def on_ready(self):
        print ('Background_Tasks: Online')

    # Chat Reviver: sends a randomized message into #the-lounge every 90 minutes
    # Suggest new responses in #suggestions or via DM
    async def chat_revive(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(623770537340174336)
        while not self.bot.is_closed():

            revive_list = ['Excuse me, sir, but do you have a moment to talk about our lord and saviour: Irene?',
                           'If you want 10000000000 months of free Nitro, please react to this message.',
                           'I dislike burgers.',
                           'I will go anywhere with anyone as long as there is sushi involved. Well, mostly anywhere. There are a few exceptions.',
                           '_deadchat or no?',
                           'Sushi is pog.',
                           '_whoasked',
                           "Don't be a simp.",
                           "Don't forget to check the Epic store for this week's free games.",
                           'sAAII MMorEE liKKEE cRRYY']

            await channel.send(f'{random.choice(revive_list)}')
            await asyncio.sleep(5400) 


def setup(bot):
    bot.add_cog(Background_Tasks_Cog(bot))