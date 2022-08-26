import random, datetime


def flatten_list(nested_list):
    return [element for sublist in nested_list for element in sublist]


def ordinal(n: int) -> str:
    return f"{n:d}{'tsnrhtdd'[(n//10%10!=1)*(n%10<4)*n%10::4]}"


def time_to_timestamp(timeformat):
    return int(datetime.datetime.strptime(timeformat,"%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp())


def timestamp_to_utcdatetime(timestamp):
    return datetime.datetime.utcfromtimestamp(timestamp)


def timestamp_to_utctime_string(timestamp: int) -> str:
    """Transform timestamp to string datetime"""
    return str(timestamp_to_utcdatetime(timestamp))


def get_utc_time():
    return int(datetime.datetime.now(datetime.timezone.utc).timestamp())


def timestamp_to_formatted_date_with_time(date):
    date = timestamp_to_utcdatetime(date)
    return date.strftime(f'{ordinal(date.day)} %B %Y at %H:%m UTC')


def timestamp_to_formatted_date(date):
    date = timestamp_to_utcdatetime(date)
    return date.strftime(f'{ordinal(date.day)} %B %Y')


def get_random_between(start: int = 1, end: int = 100):
    return str(random.choice(list(range(start, end+1))))


def get_random_quantity():
    random_q = list(range(2_000_000, 2_999_999))
    return str(random.choice(random_q)/1_000_000)