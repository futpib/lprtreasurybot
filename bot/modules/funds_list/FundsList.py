from bot import dp, types
from defs import get_list_funds


@dp.message_handler(commands=['funds_list'])
async def funds_list(message: types.Message):
    await message.reply(f'Список фондов: \n{await get_list_funds()}', parse_mode='HTML')
