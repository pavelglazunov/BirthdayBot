import datetime
from typing import Union


class UnpackError(Exception):
    pass


_months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
]


def from_text(text: str) -> tuple[Union[datetime.date, None], str]:
    date, _, month = text.lower().strip().partition(" ")
    if not (date and month):
        return None, "Простите, мне не удалось понять дату, попробуйте еще раз"

    if not date.isdigit():
        return None, "Простите, мне не удалось понять число месяца, попробуйте еще раз"

    if month not in _months:
        return None, "Простите, мне не удалось понять месяц, попробуйте еще раз"

    day = int(date)
    month = _months.index(month) + 1

    now = datetime.datetime.utcnow().date()

    try:
        return datetime.date(day=day, month=month, year=now.year), ""
    except ValueError:
        return None, "Вы ввели некорректную дату, попробуйте еще раз"


def to_text(date: datetime.date) -> str:
    return f"{date.day} {_months[date.month - 1]}"
