import aiohttp
import json
import time
from loop import loop
import re
import ujson
from PIL import Image, ImageDraw, ImageFont
import os


def get_from_config(value: str) -> str:
    with open('config.json', 'r', encoding='utf-8') as f:
        jsn = json.loads(f.read())
    return jsn[value]


url_all_funds = get_from_config('url_all_funds')
url_with_goal_funds = get_from_config('url_with_goal_funds')
URL = get_from_config('URL')  # URL апи телеграм бота с ключем 'https://api.telegram.org/bot316674800:XXX'

excel_url = get_from_config('excel_url')


async def get_from_excel(sheet_title: str, frm: str, to: str, url=excel_url) -> dict:
    """
    Возвращает response от запроса к Excel таблице
    :param url: ["https://sheets.googleapis.com/v4/spreadsheets/","sheet_id", "/values/", "sheet_title", "!","from",
    ":", "to","?key=apikey"]
    :param sheet_title: Название листа в эксель таблице
    :param frm: С какой ячейки начинается
    :param to: Какой ячейкой заканчивается
    :return: 
    """
    string = ''
    here_url = url
    here_url[3] = sheet_title
    here_url[5] = frm
    here_url[7] = to
    for i in here_url:
        string += i
    
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(string) as resp:
            return await resp.json()


def parse_command(text):
    pattern = r'\A/\w+'  # Для паттерна используется pythex.org
    try:
        formated = re.search(pattern, text).group()
    except AttributeError:
        formated = None
    return formated


def beauty_sum(just_sum: int) -> str:
    """
    Превращает число в красивую строку
    :param just_sum:
    :return:
    """
    temp_sum = str(int(float(just_sum)))
    beautiful_sum = ''
    for i in range(round(len(temp_sum) / 3 + 0.49)):
        beautiful_sum = temp_sum[-3:] + ' ' + beautiful_sum
        temp_sum = temp_sum[0:-3]
    return beautiful_sum


def fund_string(just_sum: int, fund_name: str, goal=0) -> str:
    """
    Собирает сообщение о фонде
    :param just_sum:
    :param fund_name:
    :param goal:
    :return:
    """
    string = 'Состояние фонда <b>{}</b>: \n<b>{}</b> ₽\n'.format(fund_name, beauty_sum(just_sum))
    if goal != 0:
        string += 'Осталось собрать: \n<b>{}</b> ₽\nПрогресс: [{}{}]'.format(beauty_sum(goal - just_sum),
                                                                             int(just_sum // (goal / 10)) * '●',
                                                                             int(10 - just_sum // (goal / 10)) * '○')
    return string


def get_fund_image(just_sum: int, fund_name: str, goal: int) -> str:
    """
    Создает изображение фонда и возвращает путь к нему

    Args:
        just_sum (int): [description]
        fund_name (str): [description]
        goal (int): [description]

    Returns:
        str: Путь к изображению
    """

    in_file = 'src/fund_default.jpg'
    out_file_name = fund_name + '-' + beauty_sum(just_sum).replace(' ', '') + '-' + beauty_sum(goal).replace(' ', '') + '.png'
    out_file = f'src/fund_default/{out_file_name}'

    if os.path.isfile(out_file):
        return out_file   


    # Загрузка изображения
    img = Image.open(in_file)
    draw = ImageDraw.Draw(img)
    
    # Загрузка шрифтов
    font_title = ImageFont.truetype('src/fonts/Gilroy-Bold.ttf', 57)
    font_digitals = ImageFont.truetype('src/fonts/Gilroy-Extrabold.ttf', 31)

    # Отрисовка шрифтов
    fund_name = fund_name[0].upper() + fund_name[1:]
    draw.text((22, 40), fund_name,fill='#ffffff', font=font_title)

    draw.text((22, 157), beauty_sum(just_sum), fill='#ffffff', font=font_digitals)
    draw.text((355, 157), beauty_sum(goal) + '₽', fill='#ffffff', font=font_digitals)

    # Отрисовка прогресс бара
    width = 16 + int(just_sum/goal * 467)

    draw.rectangle([16, 113, width, 139], fill='#c1a66f')   

    img.save(out_file)
    return out_file


async def fund_sum(fund_title: str) -> [int, int]:
    """
    Парсит количество денег в фонде
    :param fund_title:
    :return:
    """
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url_with_goal_funds) as resp:
            resp_json = await resp.json()

    resp_json = resp_json['values']

    fund_title = '#' + fund_title
    try:
        numb = [val[0] for val in resp_json].index(fund_title)  # Поиск номера фонда из списка фондов с целями
        fund = int(float(resp_json[numb][2].replace(',', '.')))  # Количество денег в фонде
        fund_goal = int(float(resp_json[numb][4].replace(',', '.')))  # Цель сбора у фонда
        return [fund, fund_goal]

    except ValueError:
        async with aiohttp.ClientSession(loop=loop) as session:
            async with session.get(url_all_funds) as resp:
                resp_json = await resp.json()

        resp_json = resp_json['values']
        try:
            numb = [val[1] for val in resp_json].index(fund_title)  # Поиск номера фонда во всех фондах
        except ValueError:
            return None
        fund = int(float(resp_json[numb][0].replace(',', '.')))  # Количество денег в фонде
        return [fund, 0]


async def get_list_funds() -> str:
    """
    Возвращает строку со списком актуальных фондов
    :return:
    """
    async with aiohttp.ClientSession(loop=loop) as session:
        async with session.get(url_all_funds) as resp:
            resp_json = await resp.json()
    
    funds = await get_from_excel('Состояние по фондам в рублях', 'A2', 'B1000')
    funds = funds['values']

    funds = [[float(i[0].replace(',', '.')), i[1][1:]] for i in funds if float(i[0].replace(',', '.')) != 0]

    string = ''

    for row in funds:
        string += f'<b>{row[1]}</b> - {beauty_sum(row[0])} ₽\n'
    return string


def rating_string(month=time.strftime("%m"), year=time.strftime("%y")) -> str:
    """
    Метод возвращает строку, которая содержит топ 5 донатеров
    :return:
    """

    year = '20' + year

    with open('data.json', 'r', encoding='utf-8') as f:
        data = ujson.load(f)
    
    try:
        contributions = data.get(year).get(month)
        if contributions is None:
            return None
    except AttributeError:
        return None

    dct = {}

    if contributions:
        for i in contributions:
            if float(i[6].replace(',', '.')) > 0 and i[4] != 'Техническая':
                if dct.get(i[0]):
                    dct[i[0]] += float(i[6].replace(',', '.'))
                else:
                    dct.update({i[0]: float(i[6].replace(',', '.'))})
    
    list_d = list(dct.items())
    list_d.sort(key=lambda i: i[1], reverse=True)
    list_d = list_d[:10]

    string = f'Топ 10 жертвователей за {month}.{year}:\n'

    for i in range(len(list_d)):
        string += '{}) {} - <b>{}</b> ₽\n'.format(i+1, list_d[i][0], beauty_sum(list_d[i][1]))

    return string


# def send_notification():
#     """
#     Отправляет уведомление
#     :return:
#     """
#     with open('day_data.json', 'r', encoding='utf-8') as f:
#         day_data = json.loads(f.read())
#     if len(day_data) > 0:
#         with open('users.json', 'r', encoding='utf-8') as f:
#             users = json.loads(f.read())
#         string = 'Донаты/расходы произошедшие за последние 24 часа:\n'
#         for i in day_data:
#             string += '\n{name}: <b>{amount}</b> ₽ - фонд: {fund_name}\n'.format(
#                 name=i['name'], amount=beauty_sum(i['amount'].replace(',', '.')), fund_name=i['fund_name'])
#         for i in users:
#             send_message(i['id'], string, URL)


async def update_data():
    _data = await get_from_excel("Транзакции", "A1", "K10000")
    _data = _data['values'][1:]
    _lst = []
    for i in range(len(_data)):
        if not (bool(_data[i][0]) and bool(_data[i][5]) and bool(_data[i][6])):
            _lst.append(i)

    _lst.reverse()
    for i in _lst:
        _data.pop(i)

    dct = {}

    for value in _data:
        month = value[5].split('.')[1]
        year = value[5].split('.')[2]
        if dct.get(year):
            if dct.get(year).get(month):
                dct[year][month].append(value)
            else:
                dct[year][month] = [value]
        else:
            dct[year] = {}
            dct[year][month] = [value]
    
    with open('data.json', 'w', encoding='utf-8') as f:
        ujson.dump(dct, f, ensure_ascii=False, indent=4)
