from bot import dp, types
from defs import get_from_excel, beauty_sum


@dp.message_handler(commands=['status'])
async def status(message: types.Message):
    resp = await get_from_excel("Состояние в рублях", "A2", "A2")
    resp_json = resp['values']
    string = 'Состояние казны: \n<b>' + beauty_sum(resp_json[0][0]) + '</b> ₽'
    await message.reply(string, parse_mode='HTML')
