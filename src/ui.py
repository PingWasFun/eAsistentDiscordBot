import datetime
import logging
import traceback

import discord
from discord import Embed

from src.database.db_api import reset_user_data
from util import get_today
from formatter import format_day_embed, no_permission_embed, \
    format_config_user_embed
from eAsistentAPI import (
    get_day_data,
    get_next_weekday_int,
    get_week_data,
    data_to_date,
)


# It's a view that displays a schedule
class ScheduleView(discord.ui.View):
    def __init__(self, freeze=False):
        super().__init__(timeout=60.0)
        self.date: datetime.date = get_today()
        self.day_int = None
        self.week_relative: int = 0
        self.embed: discord.Embed = None

        if freeze:
            self.clear_items()
            self.stop()

    # async def on_timeout(self):
    #     # It's setting the color of the embed to a dark grey on timeout
    #     if self.embed is None:
    #         embed = self.message.embeds[0]
    #     else:
    #         embed = self.embed
    #     embed.color = 0x383838
    #     self.clear_items()
    #     await self.message.edit(view=self, embed=embed)

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

        week_data = get_week_data(
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        dates_raw: list = week_data["request_data"]["dates"]
        last_day: datetime.date = data_to_date(dates_raw[len(dates_raw) - 1])
        self.date = last_day

        day_data = get_day_data(
            self.date.weekday(),
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        if day_data.request_week <= 1:
            button.disabled = True
            self.last_day.disabled = True
        else:
            button.disabled = False
            self.last_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:leftarrow:960972043199868968>"
    )
    async def last_day(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the previous day and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """

        week_data = get_week_data(
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        day_int = get_next_weekday_int(
            week_data["request_data"]["dates"], self.date, invert=True
        )

        if type(day_int) is str:
            if day_int == "last":
                self.week_relative = self.week_relative - 1
                week_data = get_week_data(
                    week_relative=self.week_relative,
                    user_id=interaction.user.id,
                    guild_id=interaction.guild.id,
                )

                dates = week_data["request_data"]["dates"]

                last_day: datetime.date = data_to_date(dates[len(dates) - 1])
                last_day_int: int = last_day.weekday()
                day_data = get_day_data(
                    last_day_int,
                    week_data=week_data,
                    user_id=interaction.user.id,
                    guild_id=interaction.guild.id,
                )
                self.date = last_day
            else:
                await interaction.response.edit_message(
                    Embed(description="Prišlo je do napake.")
                )
                return
        else:
            day_data = get_day_data(
                day_int,
                week_relative=self.week_relative,
                user_id=interaction.user.id,
                guild_id=interaction.guild.id,
            )
            self.date = self.date - datetime.timedelta(days=1)

        if day_data.request_week <= 1:
            button.disabled = True
            self.last_day.disabled = True
        else:
            button.disabled = False
            self.last_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:roundedblacksquare:962292311293829160>",
    )
    async def today(self, interaction: discord.Interaction,
                    button: discord.ui.Button):
        """
        It gets the data for the today and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """
        self.date = get_today()
        self.week_relative = 0
        day_int = self.date.weekday()

        day_data = get_day_data(
            day_int,
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        self.last_week.disabled = False
        self.last_day.disabled = False
        self.next_day.disabled = False
        self.next_week.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        style=discord.ButtonStyle.blurple,
        emoji="<:rightarrow:960972043178893382>"
    )
    async def next_day(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        """
        It gets the data for the next day and formats it into an embed

        :type interaction: discord.Interaction
        :type button: discord.ui.Button
        """
        week_data = get_week_data(
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )
        day_int = get_next_weekday_int(week_data["request_data"]["dates"],
                                       self.date)
        if type(day_int) is str:
            if day_int == "next":
                self.week_relative = self.week_relative + 1
                week_data = get_week_data(
                    week_relative=self.week_relative,
                    user_id=interaction.user.id,
                    guild_id=interaction.guild.id,
                )
                dates = week_data["request_data"]["dates"]
                # only need
                # the first list item to be converted to date

                first_day: datetime.date = data_to_date(dates[0])
                last_day_int: int = first_day.weekday()
                day_data = get_day_data(
                    last_day_int,
                    week_data=week_data,
                    user_id=interaction.user.id,
                    guild_id=interaction.guild.id,
                )
                self.date = first_day
            else:
                await interaction.response.edit_message(
                    Embed(description="Prišlo je do napake.")
                )
                return
        else:
            day_data = get_day_data(
                day_int,
                week_relative=self.week_relative,
                user_id=interaction.user.id,
                guild_id=interaction.guild.id,
            )
            self.date = self.date + datetime.timedelta(days=1)

        if day_data.request_week >= 53:
            button.disabled = True
            self.next_week.disabled = True
        else:
            button.disabled = False
            self.next_week.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(view=self, embed=embed)

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

        week_data = get_week_data(
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        dates_raw: list = week_data["request_data"]["dates"]
        first_day: datetime.date = data_to_date(dates_raw[0])
        self.date = first_day

        day_data = get_day_data(
            self.date.weekday(),
            week_relative=self.week_relative,
            user_id=interaction.user.id,
            guild_id=interaction.guild.id,
        )

        if day_data.request_week >= 53:
            button.disabled = True
            self.next_day.disabled = True
        else:
            button.disabled = False
            self.next_day.disabled = False

        embed = format_day_embed(day_data.raw_data)
        self.embed = embed

        await interaction.response.edit_message(view=self, embed=embed)


class Confirm(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    @discord.ui.button(label='Ja', style=discord.ButtonStyle.red)
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        user_id = interaction.user.id
        reset_user_data(user_id)
        await interaction.response.edit_message(
            content=f"Vaši podatki so bili ponstavljeni.",
            view=None
        )
        self.stop()

    @discord.ui.button(label='Ne', style=discord.ButtonStyle.green)
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        await interaction.response.edit_message(
            content=f"Ponstavitev podatkov preklicana.", view=None
        )
        self.stop()


class Feedback(discord.ui.Modal, title="Feedback"):
    # Our modal classes MUST subclass `discord.ui.Modal`,
    # but the title can be whatever you want.

    # This will be a short input, where the user can enter their name
    # It will also have a placeholder, as denoted by the `placeholder` kwarg.
    # By default, it is required and is a short-style input which is exactly
    # what we want.
    name = discord.ui.TextInput(
        label="Name",
        placeholder="Your name here...",
    )

    # This is a longer, paragraph style input, where user can submit feedback
    # Unlike the name, it is not required. If filled out, however, it will
    # only accept a maximum of 300 characters, as denoted by the
    # `max_length=300` kwarg.
    feedback = discord.ui.TextInput(
        label="What do you think of this new feature?",
        style=discord.TextStyle.long,
        placeholder="Type your feedback here...",
        required=False,
        max_length=300,
    )

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            f"Thanks for your feedback, {self.name.value}!", ephemeral=True
        )

    async def on_error(
            self, error: Exception, interaction: discord.Interaction
    ) -> None:
        await interaction.response.send_message(
            "Oops! Something went wrong.", ephemeral=True
        )

        # Make sure we know what the error actually is
        traceback.print_tb(error.__traceback__)


class ConfigView(discord.ui.View):
    def __init__(self, ctx, administrator=False):
        super().__init__(timeout=60.0)
        self.ctx = ctx
        self.administrator = administrator
        if not administrator:
            self.guild_config.style = discord.ButtonStyle.red

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        emoji="<:person_icon:966417436675026954>"
    )
    async def user_config(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        embed = format_config_user_embed(self.ctx.author.id)
        await interaction.response.send_modal(Feedback())
        await interaction.response.edit_message(view=self, embed=embed)

    @discord.ui.button(
        style=discord.ButtonStyle.green,
        emoji="<:server_icon:966420133620891698>"
    )
    async def guild_config(
            self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        if not self.administrator:
            embed = no_permission_embed("Administrator")
            await interaction.response.edit_message(view=self, embed=embed)
        embed = self.ctx.author.id
        await interaction.response.edit_message(view=self, embed=embed)
