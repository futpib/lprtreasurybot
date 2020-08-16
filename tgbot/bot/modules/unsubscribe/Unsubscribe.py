from bot import dp, types
from motor_client import SingletonClient


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    db = SingletonClient.get_data_base()
    users_collection = db.users

    user = await users_collection.find_one({
        "user_id": message.from_user.id
    })

    if user:
        result = await users_collection.delete_one({"user_id": message.from_user.id})
        print('Unsubscribe. Delete user:\n' + str(result.raw_result))
        await message.reply('Вы успешно отписались от обновлений')
    else:
        await message.reply('Вы не подписаны на обновления')
