import datetime


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
