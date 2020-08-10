from bot import dp, types
from bot import ujson


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
    with open('users.json', 'r', encoding='utf-8') as f:
        users = ujson.loads(f.read())

    if message.from_user.id in [int(i['id']) for i in users]:
        numb = [int(i['id']) for i in users].index(message.from_user.id)
        users.pop(numb)

    with open('users.json', 'w', encoding='utf-8') as f:
        ujson.dump(users, f, ensure_ascii=False, indent=2)

    await message.reply('Вы успешно отписались от обновлений')
