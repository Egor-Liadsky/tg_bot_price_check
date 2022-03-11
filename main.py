import datetime
from aiogram import Dispatcher, Bot, executor, types
import logging
from bs4 import BeautifulSoup
import requests
import re

URL = 'http://gendalf.cf/'

HEADERS = {
    'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.30',
}

bot = Bot(token='5253577953:AAFsfNyxmkvxiRgCRaprROhy4CimFvY0L58')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='check')
async def start(message: types.Message, res=False):
    await message.reply('Начало')

    get_product_name = check()[1]
    old_price = check()[0]

    date: datetime.datetime = datetime.datetime.now()
    date_format: str = date.strftime("%d/%m/%Y  %H:%M:%S")

    while True:
        actual_price = check()[0]
        if old_price != actual_price:
            await message.reply(f'Наименование товара:{get_product_name}'
                                f'\nНовая цена: {actual_price}, старая цена: {old_price}'
                                f'\nДата изменения: {date_format}')
            old_price = actual_price
        else:
            continue


def check():
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_name = soup.find('h1').get_text(strip=True)
    product_name = re.sub("[Ð|Ñ°·²½µ¸:³¾»º]", "", product_name)

    price = soup.find('h2').get_text(strip=True)
    price = re.sub("[^0-9]", "", price)

    return int(price), str(product_name)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
