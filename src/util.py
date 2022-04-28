import datetime
import os


def get_today():
    """
    Return today's date.

    :return: The current date.
    """
    return datetime.date.today()


def get_weekday_name(date: datetime.date):
    """
    It takes a date object and returns the name of the day of the week

    :type date: datetime.date
    :return: The name of the day of the week.
    """
    date_int = date.weekday()
    daynames = ["Ponedeljek", "Torek", "Sreda", "Četrtek", "Petek", "Sobota", "Nedelja"]
    dayname = daynames[date_int]
    return dayname


def get_data_dir_path(filename):
    a = f"{os.getcwd()}/data/{filename}"
    return a


def edit_text(text, none_set="None", prefix="", suffix=""):
    if text is None:
        return none_set
    return f"{prefix}{text}{suffix}"
