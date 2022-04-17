import collections
import datetime

import eAsisitent_scraper

from src.setup import SCHOOL_ID, CLASS_ID


def data_to_date(date: str):
    """
    Convert date to datetime

    :param date: Works for dates formatted with YYYY-MM-DD
    :return: datetime.date
    """
    split_date = date.split("-")
    return datetime.date(
        year=int(split_date[0]), month=int(split_date[1]), day=int(split_date[2])
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
        subject, teacher, classroom, group, event, hour, week_day, hour_in_block, date
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


def get_day_data(
    day: int,
    school_id=SCHOOL_ID,
    class_id=CLASS_ID,
    week=0,
    week_data=None,
    week_relative=None,
):
    """
    It gets the data for a specific day

    :param day: The day you want to get the data from
    :type day: int
    :param school_id: The school you want to get the schedule for
    :param class_id: The class you want to get the schedule for
    :param week: The week you want to get the data from,0 is this week,
    defaults to 0 (optional)
    :param week_data: Use this data instead of requesting
    :param week_relative: This is the relative week you want to get
    :return: A namedtuple with the raw data and the week number.
    """
    if week != 0 and week_relative is not None:
        raise ValueError(
            "You can't use week and week_relative in the same function call."
        )
    if not 6 >= day >= 0:
        raise ValueError(f"Day {day} is invalid.")

    if week_data is None:
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=week
        )
    else:
        request_response = week_data

    request_week = request_response["request_data"]["request_week"]

    if week_relative is not None:
        get_relative_week = week_relative + request_week
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=get_relative_week
        )

    if week == "next":
        next_week = request_week + 1
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=next_week
        )
    if week == "last":
        last_week = request_week - 1
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=last_week
        )

    DayData = collections.namedtuple("DayData", ["raw_data", "request_week"])

    try:
        day_data = DayData(
            request_response[str(day)], request_response["request_data"]["request_week"]
        )
    except KeyError:
        return DayData(
            request_response["0"], request_response["request_data"]["request_week"]
        )
    return day_data


def get_week_data(
    week=0, school_id=SCHOOL_ID, class_id=CLASS_ID, week_relative=None, week_data=None
):
    """
    It gets the schedule data
    for a specific week

    :param week: The week you want to get the data from,0 is this week,
    defaults to 0 (optional)
    :param school_id: The school you want to get the schedule for
    :param class_id: The class you want to get the schedule for
    :param week_data: Use this data instead of requesting
    :param week_relative: This is the relative week you want to get
    :return: A dictionary with the week data
    """
    if week != 0 and week_relative is not None:
        raise ValueError(
            "You can't use week and week_relative in the same function call."
        )

    if week_data is None:
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=week
        )
    else:
        request_response = week_data

    request_week = request_response["request_data"]["request_week"]

    if week_relative is not None:
        get_relative_week = week_relative + request_week
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=get_relative_week
        )
    else:
        request_response = eAsisitent_scraper.get_schedule_data(
            school_id=school_id, class_id=class_id, school_week=week
        )
    return request_response
