from pyfiglet import figlet_format
from datetime import datetime
from time import strftime, time

DEFAULT_FORMAT = "%Y %d %b, %A"
DEFAULT_FONT = "graceful"


def date(format=DEFAULT_FORMAT, font=DEFAULT_FONT):
    date_str = datetime.now().strftime(format=format)
    return figlet_format(date_str, font=font)
