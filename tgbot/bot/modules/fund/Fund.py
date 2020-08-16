from bot import dp, types
from defs import parse_command, fund_sum, fund_string, get_fund_image


@dp.message_handler(commands=['fund'])
async def fund(message: types.Message):
    text = message.text

    if len(text.split()) > 1:
        fund_title = text.split()[1]
        _fund = await fund_sum(fund_title)
        if _fund:
            _fund, fund_goal = _fund

            if fund_goal == 0:
                await message.reply(fund_string(_fund, fund_title, fund_goal), parse_mode='HTML')
                return None
            
            image_path = get_fund_image(_fund, fund_title, fund_goal)
            await message.reply_photo(types.InputFile(image_path), parse_mode='HTML')
            
            return None
    elif len(text.split()) == 1:
        fund_title = 'офис'
        _fund = await fund_sum(fund_title)
        _fund, fund_goal = _fund

        image_path = get_fund_image(_fund, fund_title, fund_goal)
        await message.reply_photo(types.InputFile(image_path), parse_mode='HTML')
        
        # await message.reply('Я не получил название фонда, но лови\n{}'.format(
        #     fund_string(_fund, fund_title, fund_goal)), parse_mode='HTML')

        return None

    await message.reply('Фонд не найден', parse_mode='HTML')
