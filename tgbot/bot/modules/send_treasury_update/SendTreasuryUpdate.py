from bot import bot
from defs import beauty_sum, update_data
from datetime import datetime
from motor_client import SingletonClient


async def send_treasury_update(from_monday: datetime, to_monday: datetime):
    """
    Отправляет уведомление
    :return:
    """
    await update_data()
    
    db = SingletonClient.get_data_base()
    collection = db.transactions

    cursor = collection.find({
        "date": {
            "$gte": str(from_monday),
            "$lte": str(to_monday)
        }
    })

    week_data = await cursor.to_list(length=await collection.count_documents({}))

    users_cursor = db.users.find({})

    users = await users_cursor.to_list(length=await db.users.count_documents({}))

    string = 'Транзакции произошедшие за последнюю неделю:\n'
    for data in week_data:
        string += '\n{name}: <b>{amount}</b> ₽ - фонд: {fund_name}\n'.format(
            name=data['from'], amount=beauty_sum(data['total']), fund_name=data['fund'])
    
    for user in users:
        print("user: ")
        print(user)
        await bot.send_message(user['user_id'], string, parse_mode='HTML')
