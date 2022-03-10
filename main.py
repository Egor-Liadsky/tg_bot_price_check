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

bot = Bot(token='5253577953:AAFGtMiESHHJpvUXfXSFCMbbaH9_b9vbdeY')
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands='check')
async def start(message: types.Message, res=False):
    await message.reply('Начало')

    real_price = check()[0]
    dt = datetime.datetime.now()
    while True:

        if real_price != check()[0]:
            await message.reply(f'Наименование товара:{check()[1]}'
                                f'\nНовая цена: {check()[0]}, старая цена: {real_price}'
                                f'\nДата изменения: {dt.strftime("%d/%m/%Y  %H:%M:%S")}')

            print(f'Наименование товара:{check()[1]}'
                  f'\nNew price: {check()[0]}\nOld price: {real_price}'
                  f'\nДата изменения: {dt.strftime("%d/%m/%Y  %H:%M:%S")}')
            real_price = check()[0]
        else:
            continue


def check():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'lxml')

    product_name = soup.find('h1').get_text(strip=True)
    product_name = re.sub("[Ð|Ñ°·²½µ¸:³¾»º]", "", product_name)

    price = soup.find('h2').get_text(strip=True)
    price = re.sub("[^0-9]", "", price)

    return int(price), str(product_name)


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
