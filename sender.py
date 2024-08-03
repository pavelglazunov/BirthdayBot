import asyncio
import datetime
import time

from aiogram import Bot
from sqlalchemy.ext.asyncio import async_sessionmaker

from config.config import config
from src.repo import DB
from src.services import aio


async def run(bot: Bot, session_pool: async_sessionmaker):
    now = datetime.datetime.utcnow()
    send_time = config.time.send_time

    if now >= config.time.send_time:
        send_time += datetime.timedelta(days=1)

    seconds_until_next_send = int((send_time - now).total_seconds())

    await asyncio.sleep(seconds_until_next_send)

    while True:
        async with session_pool() as session:
            db = DB(session)
            today_birthdays = await db.birthday.today()

            for birthday in today_birthdays:
                await aio.send_message(
                    bot=bot,
                    chat_id=birthday.from_user,
                    content="Сегодня день рождения у \n"
                            f"{birthday.name}\n\n"
                            f"Обязательно хорошо поздравь его\\её",
                )

            await asyncio.sleep(60 * 60 * 24)
