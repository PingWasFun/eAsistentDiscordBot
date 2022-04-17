import datetime

import discord
import logging

from src.eAsistentAPI import data_to_date, hour_data_to_tuple
from src.util import get_weekday_name


def get_embed_color(date: datetime.date):
    """
    If the date is today, return a light orange color. If the date is tomorrow,
    return a light green color. If the date is in the future, return a light blue
    color. If the date is in the past, return a light red color

    :param date: The date to get the color for
    :type date: datetime.date
    :return: The color of the embed based on the date.
    """
    # https://colorhunt.co/palette/ff6b6bffd93d6bcb774d96ff
    today = datetime.date.today()
    if date == today:  # if date is today
        return 0xFFD93D
    elif date == (today + datetime.timedelta(days=1)):
        # if date is tomorrow
        return 0x6BCB77
    elif date > today:  # if date is in the future
        return 0x4D96FF
    elif date < today:  # if date is in the past
        return 0xFF6B6B


def group_formatter(group: list, split_fill: str, prefix="", suffix=""):
    """
    Formats groups

    :param group: list of groups
    :type group: list
    :param split_fill: The string to use to join the group
    :type split_fill: str
    :param prefix: The prefix to add to the beginning of the formatted string
    :param suffix: The suffix to add to the end of the formatted string
    :return: A string with the elements of the list joined by the split_fill
    string, with the prefix and suffix strings added to the beginning and end of
    the string.
    """
    if not group:
        return ""
    group_formatted = split_fill.join(group)
    return f"{prefix}{group_formatted}{suffix}"


def format_event(event: str, prefix="", suffix=""):
    """
    Formats events

    :param event: raw event name
    :type event: str
    :param prefix: The text that will be added before the formatted string
    :param suffix: The text that will be added after the formatted string
    :return: A string with the prefix, event, and suffix.
    """
    if not event:
        return ""
    event_list = {
        "cancelled": "Odpadla ura",
        "event": "Dogodek",
        "substitute": "Nadomeščanje",
        "half_hour": "Polovična ura",
        "video_call": "Videokonferenca",
        "activity": "Interesna dejavnost",
        "occupation": "Zaposlitev",
        "unfinished_hour": "Neopravljena ura",
        "office_hours": "Govorilne ure",
        "exams": "Izpiti",
        "unknown_event": "unknown_event_from_scraper",
    }
    try:
        event_formated = event_list[event]

    except KeyError:
        logging.warning(f"Unknown event detected: {event}")
        event_formated = "unknown_event_from_formater"

    return f"{prefix}{event_formated}{suffix}"


def description_part_formatter(format_data, prefix="", suffix=""):
    """
    It takes a string, and returns a string

    :param format_data: The data to be formatted
    :param prefix: The text that will be added before the formatted string
    :param suffix: The text that will be added after the formatted string
    :return: A string with the prefix, format_data, and suffix.
    """
    if not format_data:
        return ""
    return f"{prefix}{format_data}{suffix}"


def format_for_description(
    subject: str, teacher: str, classroom: str, event: str, group: list
):
    """
    It formats the description part of the embed

    :param subject: The subject of the embed part
    :param teacher: The teacher's name of the embed part
    :param classroom: The classroom of the embed part
    :param event: The event of the embed part
    :param group: The group of the embed part
    :return: Part of an embed
    """
    if event == "cancelled":
        group_part = group_formatter(
            group, split_fill=", ", prefix="  Skupina: ~~`", suffix="`~~\n"
        )
        subject = description_part_formatter(
            subject, prefix="  Predmet: ~~`", suffix="`~~\n"
        )
        teacher = description_part_formatter(
            teacher, prefix="  Učitelj: ~~`", suffix="`~~\n"
        )
        classroom = description_part_formatter(
            classroom, prefix="  Učilnica: ~~`", suffix="`~~\n"
        )
        event = format_event(event, prefix="  *", suffix="*\n")
    else:
        group_part = group_formatter(
            group, split_fill=", ", prefix="  Skupina: `", suffix="`\n"
        )
        subject = description_part_formatter(
            subject, prefix="  Predmet: `", suffix="`\n"
        )
        teacher = description_part_formatter(
            teacher, prefix="  Učitelj: `", suffix="`\n"
        )
        classroom = description_part_formatter(
            classroom, prefix="  Učilnica: `", suffix="`\n"
        )
        event = format_event(event, prefix="  *", suffix="*\n")

    embed_description_part = event + subject + teacher + classroom + group_part + "\n"

    return embed_description_part


def format_day_embed(day_data: dict):
    """
    It takes a dictionary of the day data and returns a discord embed.

    :param day_data: dictionary of data for a day
    :type day_data: dict
    :return: A discord embed object
    """
    embed_description = ""
    is_free_day = True
    for hour_data_keys, hour_data in day_data.items():
        count = 0

        if hour_data["0"]["subject"] is not None:
            is_free_day = False

        for block_data_keys, block_data_raw in hour_data.items():
            block_data = hour_data_to_tuple(block_data_raw)

            if block_data.subject is None:
                break

            if count == 0:
                hour_name = (hour_data["0"]["hour"],)

                hour_name = hour_name[0].capitalize()

                embed_hour_name_part = f"**{hour_name}:**\n"

                embed_description = embed_description + embed_hour_name_part
                count += 1

            embed_description = embed_description + format_for_description(
                block_data.subject,
                block_data.teacher,
                block_data.classroom,
                block_data.event,
                block_data.group,
            )

    if is_free_day:
        embed_description = "\n**Prost dan**\n"

    date = data_to_date(block_data.date)

    embed = discord.Embed(color=get_embed_color(date), description=embed_description)

    dayname = get_weekday_name(date)
    date_formated = date.strftime("%d. %m. %Y")
    dayname_format = f"{dayname}, {date_formated}"
    embed.set_author(name=dayname_format)

    embed.set_footer(text=f"{dayname_format}")
    return embed
