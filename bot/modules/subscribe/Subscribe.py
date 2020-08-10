from bot import dp, types
from bot import ujson


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
    with open('users.json', 'r', encoding='utf-8') as f:
        users = ujson.loads(f.read())

    if message.from_user.id in [int(i['id']) for i in users]:
        await message.reply('Вы уже подписаны на обновления')
    else:
        users.append(
            {"id": message.from_user.id, "first_name": message.from_user.first_name,
             "username": message.from_user.mention})

        with open('users.json', 'w', encoding='utf-8') as f:
            ujson.dump(users, f, ensure_ascii=False, indent=2)

        await message.reply('Вы успешно подписались на обновления')
