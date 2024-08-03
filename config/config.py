import datetime
import logging
from dataclasses import dataclass

from dotenv import load_dotenv

from .base import getenv


# logging
def init_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler("app.log")


@dataclass
class Bot:
    token: str


@dataclass
class Db:
    url: str


@dataclass
class Time:
    send_time: datetime.datetime


@dataclass
class Channels:
    backup: int


@dataclass
class Config:
    bot: Bot
    db: Db
    time: Time
    channels: Channels


def load_config() -> Config:
    now = datetime.datetime.utcnow()
    load_dotenv()
    return Config(
        bot=Bot(
            token=getenv("TOKEN"),
        ),
        db=Db(
            url=getenv("DB_URL"),
        ),
        time=Time(
            datetime.datetime(
                now.year,
                now.month,
                now.day,
                int(getenv("SEND_HOURS")),
                int(getenv("SEND_MINUTES")),
                0,
            ),
        ),
        channels=Channels(
            backup=int(getenv("CHANNEL_BACKUP")),
        )
    )


config: Config = load_config()
