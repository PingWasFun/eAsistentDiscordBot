exit()
import logging

import discord
from discord.ext import commands

development = False

intents = discord.Intents(
    messages=True,
    guilds=True,
    reactions=True,
    members=True,
    presences=True,
    message_content=True,
)

if development == "beta":
    bot = commands.Bot(
        command_prefix=">",
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="¯\_(ツ)_/¯ work?  ¯\_(ツ)_/¯"
        ),
        status=discord.Status.idle,
        intents=intents,
    )

elif development is True:
    bot = commands.Bot(
        command_prefix="<",
        activity=discord.Activity(
            type=discord.ActivityType.playing, name="IN DEVELPOMENT"
        ),
        status=discord.Status.do_not_disturb,
        intents=intents,
    )
else:
    bot = commands.Bot(
        command_prefix=">",
        activity=discord.Activity(type=discord.ActivityType.listening, name=">help"),
        status=discord.Status.online,
        intents=intents,
    )


@bot.event
async def test():
    print(test)
