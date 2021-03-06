from bot import dp, types
from defs import get_from_excel, beauty_sum


@dp.message_handler(commands=['funds'])
async def funds(message: types.Message):
    _funds = await get_from_excel('Состояние по фондам в рублях', 'A2', 'B1000')
    _funds = _funds['values']

    _funds = [[i[0], i[1][1:]] for i in _funds if int(i[0]) != 0]

    string = ''

    for row in _funds:
        string += f'<code>{beauty_sum(row[0]).strip(): >6}</code> ₽ - <b>{row[1]}</b>\n'
    
    await message.reply(f'Список фондов: \n{string}', parse_mode='HTML')
