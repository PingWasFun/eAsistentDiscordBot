import datetime

import discord
from discord import Embed
from util import get_today
from formatter import format_day_embed
from eAsistentAPI import (
    get_day_data,
    get_next_weekday_int,
    get_week_data,
    data_to_date,
)


# It's a view that displays a schedule
class Schedule(discord.ui.View):
    def __init__(self, freeze=False):
        super().__init__(timeout=10.0)
        self.date: datetime.date = get_today()
        self.day_int = None
        self.week_relative: int = 0
        self.embed: discord.Embed = None

        if freeze:
            self.clear_items()
            self.stop()

    async def on_timeout(self):
        # It's setting the color of the embed to a dark grey on timeout
        if self.embed is None:
            embed = self.message.embeds[0]
        else:
            embed = self.embed
        embed.color = 0x383838
        self.clear_items()
        await self.message.edit(view=self, embed=embed)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:doubleleftarrows:960978910403760238>",
    )
    async def last_week(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the previous week, and then formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """
        self.week_relative = self.week_relative - 1

        week_data = get_week_data(week_relative=self.week_relative)

        dates_raw: list = week_data["request_data"]["dates"]
        last_day: datetime.date = data_to_date(dates_raw[len(dates_raw) - 1])
        self.date = last_day

        day_data = get_day_data(self.date.weekday(), week_relative=self.week_relative)

        if day_data.request_week <= 1:
            button.disabled = True
            self.last_day.disabled = True
        else:
            button.disabled = False
            self.last_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(
            view=self, embed=embed
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple, emoji="<:leftarrow:960972043199868968>"
    )
    async def last_day(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the previous day and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """

        week_data = get_week_data(week_relative=self.week_relative)

        day_int = get_next_weekday_int(
            week_data["request_data"]["dates"], self.date, invert=True
        )

        if type(day_int) is str:
            if day_int == "last":
                self.week_relative = self.week_relative - 1
                week_data = get_week_data(week_relative=self.week_relative)

                dates = week_data["request_data"]["dates"]

                last_day: datetime.date = data_to_date(dates[len(dates) - 1])
                last_day_int: int = last_day.weekday()
                day_data = get_day_data(last_day_int, week_data=week_data)
                self.date = last_day
            else:
                await interaction.response.edit_message(
                    Embed(description="Prišlo je do napake.")
                )
                return
        else:
            day_data = get_day_data(day_int, week_relative=self.week_relative)
            self.date = self.date - datetime.timedelta(days=1)

        if day_data.request_week <= 1:
            button.disabled = True
            self.last_day.disabled = True
        else:
            button.disabled = False
            self.last_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(
            view=self, embed=embed
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:roundedblacksquare:962292311293829160>",
    )
    async def today(self, interaction: discord.Interaction, button: discord.ui.Button):
        """
        It gets the data for the today and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """
        self.date = get_today()
        self.week_relative = 0
        day_int = self.date.weekday()

        day_data = get_day_data(day_int, week_relative=self.week_relative)

        self.last_week.disabled = False
        self.last_day.disabled = False
        self.next_day.disabled = False
        self.next_week.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(
            view=self, embed=embed
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple, emoji="<:rightarrow:960972043178893382>"
    )
    async def next_day(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the next day and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """
        week_data = get_week_data(week_relative=self.week_relative)
        day_int = get_next_weekday_int(week_data["request_data"]["dates"], self.date)
        if type(day_int) is str:
            if day_int == "next":
                self.week_relative = self.week_relative + 1
                week_data = get_week_data(week_relative=self.week_relative)
                dates = week_data["request_data"]["dates"]
                # only need
                # the first list item to be converted to date

                first_day: datetime.date = data_to_date(dates[0])
                last_day_int: int = first_day.weekday()
                day_data = get_day_data(last_day_int, week_data=week_data)
                self.date = first_day
            else:
                await interaction.response.edit_message(
                    Embed(description="Prišlo je do napake.")
                )
                return
        else:
            day_data = get_day_data(day_int, week_relative=self.week_relative)
            self.date = self.date + datetime.timedelta(days=1)

        if day_data.request_week >= 53:
            button.disabled = True
            self.next_week.disabled = True
        else:
            button.disabled = False
            self.next_week.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(
            view=self, embed=embed
        )

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:doublerightarrows:960978910424731768>",
    )
    async def next_week(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the next week and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """

        self.week_relative = self.week_relative + 1

        week_data = get_week_data(week_relative=self.week_relative)

        dates_raw: list = week_data["request_data"]["dates"]
        first_day: datetime.date = data_to_date(dates_raw[0])
        self.date = first_day

        day_data = get_day_data(self.date.weekday(), week_relative=self.week_relative)

        if day_data.request_week >= 53:
            button.disabled = True
            self.next_day.disabled = True
        else:
            button.disabled = False
            self.next_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(
            view=self, embed=embed
        )
