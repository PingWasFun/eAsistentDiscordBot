import datetime
import logging
import typing
from zoneinfo import ZoneInfo

import discord
from discord import Embed, app_commands
from discord.ext import commands, tasks

from src.eAsistentAPI import (
    get_day_data,
    get_week_data,
    get_next_weekday_int,
    data_to_date,
)
from src.formatter import format_day_embed, error_in_config_emebd
from src.ui import ScheduleView
from src.util import get_today


class ScheduleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logging.debug(f"commands.schedule (ScheduleCog) started")
        self.daily_schedule.start()

    @commands.command(name="commands.schedule.ping")
    @commands.is_owner()
    async def ping(self, ctx):
        await ctx.send(f"Pong")

    @app_commands.command(
        name="urnik", description="Prikeže urnik"
    )
    async def schedule(self, interaction: discord.Interaction,
                       za: typing.Literal["server", "uporabnik"] = None
                       ):
        today_int = get_today().weekday()
        day_int = today_int
        get_data_from = za
        try:
            if get_data_from == "uporabnik":
                day_data = get_day_data(
                    day_int, user_id=interaction.user.id
                ).raw_data
            elif get_data_from == "server":
                day_data = get_day_data(
                    day_int, guild_id=interaction.guild.id
                ).raw_data
            else:
                day_data = get_day_data(
                    day_int, user_id=interaction.user.id,
                    guild_id=interaction.guild.id
                ).raw_data

        except ValueError:
            # logging.error(error)
            await interaction.response.send_message(
                ephemeral=True,
                embed=error_in_config_emebd(
                    "school_id, class_id")
            )

            return
        if False is True:  # if args == "next_day_freeze":
            week_relative = 0
            date = get_today()
            week_data = get_week_data(week_relative=week_relative)
            day_int = get_next_weekday_int(week_data["request_data"]["dates"],
                                           date)
            if type(day_int) is str:
                if day_int == "next":
                    week_relative = week_relative + 1
                    week_data = get_week_data(week_relative=week_relative)
                    dates = week_data["request_data"]["dates"]

                    first_day: datetime.date = data_to_date(dates[0])
                    last_day_int: int = first_day.weekday()
                    day_data = get_day_data(last_day_int, week_data=week_data)
                else:
                    await interaction.response.send_message(
                        ephemeral=True,
                        embed=Embed(description="Prišlo je do napake."))
                    return
            else:
                day_data = get_day_data(day_int, week_relative=week_relative)
            await interaction.response.send_message(
                ephemeral=True,
                embed=format_day_embed(day_data.raw_data))

        else:
            view = ScheduleView()
            await interaction.response.send_message(
                ephemeral=True,
                embed=format_day_embed(day_data),
                view=view)

    loop_time = datetime.time(
        hour=18, minute=0, second=0, tzinfo=ZoneInfo("Europe/Ljubljana")
    )

    @tasks.loop(time=loop_time)
    async def daily_schedule(self):
        pass
        # send_schedule_channel = await client.Client.fetch_channel(
        #     self.bot, SCHEDULE_CHANNEL_ID
        # )
        # await self.schedule(send_schedule_channel, args="next_day_freeze")


async def setup(bot):
    await bot.add_cog(
        ScheduleCog(bot), guilds=[discord.Object(id=882993496141729792)]
    )
