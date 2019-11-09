import datetime


def parse_date(date_str):
    date_str = list(map(int, date_str.split("-")))
    return datetime.datetime(year=date_str[0], month=date_str[1], day=date_str[2])
