import os
import discord
from discord.ext import commands
import random
from datetime import datetime
from .clib import crimsotools as c
from .clib import markovtools as m

# path to root
root_dir = os.path.dirname(__file__) #<-- absolute dir the script is in

class Chat:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def scatterbrain(self,ctx):
        """Short-term memory mania."""
        channel = ctx.message.channel
        messages = []
        # grab message contents (which are strings):
        async for message in self.bot.logs_from(channel,limit=500):
            if str(message.author) != 'crimsoBOT#0992':
                messages.append(message.content)

        output = m.markovScatter(messages)
        await self.bot.say(output)

    @commands.command(pass_context=True, hidden=True)
    async def scrape(self, ctx, place='here', join='space', n=10000):
        """Scrape messages from channel. >scrape [here/dm/channel_id] [space/newline]."""
        if ctx.message.author.id == '310618614497804289' or '179313752464818178':
            if os.path.exists(root_dir+'\\ref\\scrape.txt'):
                os.remove(root_dir+'\\ref\\scrape.txt')
            channel = ctx.message.channel
            await self.bot.delete_message(ctx.message)
            # grab message contents (which are strings):
            async for msg in self.bot.logs_from(channel, limit=n):
                if not msg.pinned:
                    m.scraper(msg.content)
            text = []
            for line in reversed(list(open(root_dir+'\\ref\\scrape.txt', encoding='utf8', errors='ignore'))):
                text.append(line.rstrip())
            # haiku only
            for i in range(len(text)):
                if (i + 1) % 3 == 0:
                    text[i] = text[i] + '\n\u200A'
            if join == 'space':
                joiner = ' '
            elif join == 'newline':
                joiner = '\n'
            text = joiner.join(text)

            msgs = c.crimsplit(text, '\u200A', 1950)
            try:
                if place == 'dm':
                    dest = ctx.message.author
                elif place == 'here':
                    dest = ctx.message.channel
                else:
                    dest = discord.Object(id=place)
            except:
                raise commands.errors.CommandInvokeError('wrong place!')
            for msg in msgs:
                await self.bot.send_message(dest, msg)

    @commands.command(pass_context=True)
    async def poem(self, ctx):
        """Spits out a poem."""
        fake_author = [['Crimso Allen Poe', 1827, 1848],
                       ['Maya Crimsolou', 1969, 2013],
                       ['Crimbert Frost', 1894, 1959],
                       ['Crumi', 1225, 1260],
                       ['William Crimsworth', 1793, 1843],
                       ['t.s. crimsiot', 1910, 1958],
                       ['Crimily Dickinson', 1858, 1886],
                       ['William Crimso Williams', 1910, 1962],
                       ['Crymsia Plath', 1960, 1963],
                       ['Crimtrude Stein', 1909, 1933],
                       ['Allen Crimsberg', 1950, 1997]]
        descr = m.markovPoem(int(random.gauss(5,1)))
        embed = c.crimbed('**A poem.**', descr.lower(), None)
        choice = random.randint(0, len(fake_author)-1)
        embed.set_footer(text='{}, {}'.format(fake_author[choice][0], random.randint(fake_author[choice][1], fake_author[choice][2])))
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def wisdom(self, ctx):
        """Crimsonic wisdom."""
        embed = c.crimbed('**CRIMSONIC WISDOM**', m.wisdom(), None)
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True,
                      aliases=['monty'])
    async def montyward(self, ctx):
        """Monty mindfuck!"""
        footer_text = ['Those black spots on your bananas? Those are tarantula eggs.',
                       'You don\'t know Monty but he knows you.',
                       'Look behind you. Now to your left. Now your right! Nevermind, Monty is already gone.',
                       'You wrote this story before you fell into the coma. Don\'t bother waking up, the world is ending.',
                       'You know that urge you have to scratch the itch behind your eyelids? Those are the worms.',
                       'Scream if you must, it won\'t do you any good.',
                       'Word to the wise: don\'t look at the moon.']
        title = 'An excerpt from **THE FIRST NECROMANCER (sort of)**, by Monty Ward'
        descr = m.rovin()
        embed = c.crimbed(title, descr, 'https://i.imgur.com/wOFf7PF.jpg')
        embed.set_footer(text=random.choice(footer_text) + ' Sleep tight.')
        await self.bot.send_message(ctx.message.channel, embed=embed)
    
    # @commands.command(pass_context=True, hidden=True)
    # async def final(self, ctx):
    #     await self.bot.say('`Final warning...`')
    #     channel = ctx.message.channel
    #     now = datetime.utcnow()
    #     then = now.replace(hour=2, minute=25)
    #     # grab message contents (which are strings):
    #     async for message in self.bot.logs_from(channel, limit=10000):
    #         if str(message.author.id) == '310618614497804289':
    #             if message.timestamp > then:
    #                 m.learner(message.content)
    #     await self.bot.say('`Task complete.`')

def setup(bot):
    bot.add_cog(Chat(bot))
