import datetime
import logging
from zoneinfo import ZoneInfo

import discord
from discord import client, Embed
from discord.ext import commands, tasks
from src.formatter import format_day_embed
from setup import SCHEDULE_CHANNEL_ID

from src.eAsistentAPI import (
    get_day_data,
    get_week_data,
    get_next_weekday_int,
    data_to_date,
)
from src.util import get_today
from ui import Schedule

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
        activity=discord.Activity(type=discord.ActivityType.listening,
                                  name=">help"),
        status=discord.Status.online,
        intents=intents,
    )


@bot.event
async def on_ready():
    print(f"Bot stated. Logged in as {bot.user}.")
    channel = await client.Client.fetch_channel(bot, 882993496141729795)
    await channel.send("Bot started")
    daily_schedule.start()


@bot.command()
async def ping(ctx):
    await ctx.send("pong")


@bot.command(name="urnik", aliases=["u"])
async def schedule(ctx, args=""):
    today_int = get_today().weekday()
    day_int = today_int
    day_data = get_day_data(day_int).raw_data

    if args == "next_day_freeze":
        week_relative = 0
        date = get_today()
        week_data = get_week_data(week_relative=week_relative)
        day_int = get_next_weekday_int(week_data["request_data"]["dates"], date)
        if type(day_int) is str:
            if day_int == "next":
                week_relative = week_relative + 1
                week_data = get_week_data(week_relative=week_relative)
                dates = week_data["request_data"]["dates"]

                first_day: datetime.date = data_to_date(dates[0])
                last_day_int: int = first_day.weekday()
                day_data = get_day_data(last_day_int, week_data=week_data)
            else:
                ctx.send(embed=Embed(description="Prišlo je do napake."))
                return
        else:
            day_data = get_day_data(day_int, week_relative=week_relative)
        await ctx.send(embed=format_day_embed(day_data.raw_data))
    else:
        view = Schedule()
        view.message = await ctx.send(embed=format_day_embed(day_data), view=view)


@bot.command(aliases=["shutdown"])
@commands.has_permissions(administrator=True)
async def close(ctx):
    await ctx.send("Shutting down bot...")
    await bot.close()
    logging.warning(
        f"Bot shutdown from command. name: {ctx.author.name}"
        f"#{ctx.author.discriminator} ({ctx.author.display_name}), "
        f"id: {ctx.author.id}"
    )


loop_time = datetime.time(
    hour=18, minute=0, second=0, tzinfo=ZoneInfo("Europe/Ljubljana")
)


@tasks.loop(time=loop_time)
async def daily_schedule():
    send_schedule_channel = await client.Client.fetch_channel(bot, SCHEDULE_CHANNEL_ID)
    await schedule(send_schedule_channel, args="next_day_freeze")
