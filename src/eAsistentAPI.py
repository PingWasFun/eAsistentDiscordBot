import collections
import datetime
import logging

import eAsisitent_scraper

from src.database.db_api import get_user_data, get_guild_data


def data_to_date(date: str):
    """
    Convert date to datetime

    :param date: Works for dates formatted with YYYY-MM-DD
    :return: datetime.date
    """
    split_date = date.split("-")
    return datetime.date(
        year=int(split_date[0]), month=int(split_date[1]),
        day=int(split_date[2])
    )


def hour_from_to_to_time(hour_from_to: str):
    """
    It takes a string of the form "HH:MM-HH:MM" and returns a list of two
    datetime.time objects

    :param hour_from_to: str
    :type hour_from_to: str
    :return: A list of two datetime.time objects.
    """

    split_time = hour_from_to.split("-")
    hour_from = split_time[0].split(":")
    hour_to = split_time[1].split(":")
    return [
        datetime.time(hour=int(hour_from[0]), minute=int(hour_from[1])),
        datetime.time(hour=int(hour_to[0]), minute=int(hour_to[1])),
    ]


def hour_data_to_tuple(hour_data: dict):
    """
    It takes an hour_data dictionary
    and returns a namedtuple

    :param hour_data: a dictionary with the following keys:
    :return: A named tuple with the following fields:
        subject,
        teacher,
        classroom,
        group,
        event,
        hour,
        week_day,
        hour_in_block,
        date
    """
    try:
        subject = hour_data["subject"]
        teacher = hour_data["teacher"]
        classroom = hour_data["classroom"]
        group = hour_data["group"]
        event = hour_data["event"]
        hour = hour_data["hour"]
        week_day = hour_data["week_day"]
        hour_in_block = hour_data["hour_in_block"]
        date = hour_data["date"]
    finally:
        pass
    HourData = collections.namedtuple(
        "HourData",
        [
            "subject",
            "teacher",
            "classroom",
            "group",
            "event",
            "hour",
            "week_day",
            "hour_in_block",
            "date",
        ],
    )
    return HourData(
        subject, teacher, classroom, group, event, hour, week_day,
        hour_in_block, date
    )


def get_next_weekday_int(dates: list, date: datetime.date, invert=False):
    """
    If the date is in the list, return the index of the date in the list. If the
    date is not in the list, return the index of the next date in the list

    :param dates: list of dates in the format of "YYYY-MM-DD"
    :type dates: list
    :param date: the date you want to find the next weekday for
    :type date: datetime.date
    :param invert: if True, then we're looking for the last weekday in the list.
     If False, then we're looking for the next weekday in the list, defaults to
    False (optional)
    :return: int for weekday, if the day is in last week "last", if day is
    in nex week "next"
    """

    dates = [data_to_date(i) for i in dates]
    for count, list_day in enumerate(dates):
        if list_day == date:
            if count == 0 and invert:
                return "last"
            elif count == (len(dates) - 1) and not invert:
                return "next"
            else:
                if invert:
                    return date.weekday() - 1
                return date.weekday() + 1


def get_request_response(
        week_data=None, user_id=None, guild_id=None, week=0,
        week_relative=None, ignore_user_id=False
):
    if week != 0 and week_relative is not None:
        raise ValueError(
            "You can't use week and week_relative in the same function call."
        )

    db_user_data = None
    db_guild_data = None

    if user_id is not None:
        db_user_data = get_user_data(user_id)
    if guild_id is not None:
        db_guild_data = get_guild_data(guild_id)

    if week_data is not None:
        request_response = week_data
    elif db_user_data is not None and ignore_user_id is False:
        school_id = db_user_data.school_id
        class_id = db_user_data.class_id

        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=week
        )
    elif db_guild_data is not None:
        school_id = db_guild_data.school_id
        class_id = db_guild_data.class_id

        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=week
        )
    else:
        raise ValueError("No school_id adn class_id provided.")

    request_week = request_response["request_data"]["request_week"]
    school_id = request_response["request_data"]["used_data"]["school_id"]
    class_id = request_response["request_data"]["used_data"]["class_id"]

    if week_relative is not None:
        get_relative_week = week_relative + request_week
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id,
            school_week=get_relative_week
        )
    elif week == "next":
        next_week = request_week + 1
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=next_week
        )
    elif week == "last":
        last_week = request_week - 1
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=last_week
        )

    return request_response


def get_day_data(
        day: int,
        week=0,
        week_data=None,
        week_relative=None,
        guild_id=None,
        user_id=None,
        ignore_user_id=False
):
    """
    It gets the data for a specific day

    :param ignore_user_id:
    :param user_id: id of the user
    :param guild_id: id of the guild
    :param day: The day you want to get the data from
    :type day: int
    :param week: The week you want to get the data from,0 is this week,
    defaults to 0 (optional)
    :param week_data: Use this data instead of requesting
    :param week_relative: This is the relative week you want to get
    :return: A namedtuple with the raw data and the week number.
    """

    if not 6 >= day >= 0:
        raise ValueError(f"Day {day} is invalid.")

    request_response = get_request_response(
        week_data=week_data,
        user_id=user_id,
        guild_id=guild_id,
        week=week,
        week_relative=week_relative,
        ignore_user_id=ignore_user_id
    )
    DayData = collections.namedtuple("DayData", ["raw_data", "request_week"])

    try:
        day_data = DayData(
            request_response[str(day)],
            request_response["request_data"]["request_week"]
        )
    except KeyError:
        return DayData(
            request_response["0"],
            request_response["request_data"]["request_week"]
        )
    return day_data


def get_week_data(
        week=0, week_relative=None, week_data=None, user_id=None,
        guild_id=None, ignore_user_id=False
):
    """
    It gets the schedule data
    for a specific week

    :param ignore_user_id:
    :param guild_id:
    :param user_id:
    :param week: The week you want to get the data from,0 is this week,
    defaults to 0 (optional)
    :param week_data: Use this data instead of requesting
    :param week_relative: This is the relative week you want to get
    :return: A dictionary with the week data
    """

    request_response = get_request_response(
        week_data=week_data,
        user_id=user_id,
        guild_id=guild_id,
        week=week,
        week_relative=week_relative,
        ignore_user_id=ignore_user_id
    )
    return request_response
