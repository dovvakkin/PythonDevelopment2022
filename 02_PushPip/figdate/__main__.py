import sys
import locale
from figdate import date


if __name__ == '__main__':
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

    if len(sys.argv) == 2:
        print(date(sys.argv[1]))

    elif len(sys.argv) == 3:
        print(date(sys.argv[1], sys.argv[2]))

    elif len(sys.argv) == 1:
        print(date())
