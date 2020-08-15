from loop import loop
from bot import dp
from aiogram import executor
from datetime import datetime
import asyncio

async def treasury_updates_waiter():
    today = datetime.strftime(datetime.today(), '%d.%m.%Y')
    today = datetime.strptime(today + ' 20:00', '%d.%m.%Y %H:%M')
    days_to_monday = 7 - datetime.today().weekday()
    monday_timestamp = datetime.timestamp(today) + (days_to_monday) * 86400
    monday_date = datetime.fromtimestamp(monday_timestamp)
    _monday_date = datetime.fromtimestamp(monday_timestamp - 604800)
    
    await asyncio.sleep(monday_timestamp - datetime.timestamp(datetime.now()))

    pass


if __name__ == "__main__":
    loop.create_task()
    executor.start_polling(dp, loop=loop, skip_updates=True)
