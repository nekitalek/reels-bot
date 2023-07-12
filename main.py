import logging
import asyncio
import os
import pathlib
import aiogram
from aiogram import Bot, Dispatcher, types
import urlextract
import asyncio
from pyppeteer import launch
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import glob
from aiogram.types import InputFile

logging.basicConfig(level=logging.INFO)
bot = Bot(token='5909454942:AAFrcBLky7xrSpOKFCJivhJWcZSMTOWJiRs')
dp = Dispatcher(bot)


def find_files_by_extension(directory, extension):
    path = pathlib.Path(directory)
    files = list(path.glob(f"**/*.{extension}"))
    return [str(file) for file in files]


@dp.message_handler(commands=['video'])
async def say_hello_command(message: types.Message):
    tokens = message.text.split(' ')
    if len(tokens) != 2:
        response = f"@{message.from_user.username}\nExample of command /video <link to video>"
        await message.answer(response)
    else:
        extractor = urlextract.URLExtract()
        urls = extractor.find_urls(tokens[1])
        if len(urls) == 0:
            response = f"\'{tokens[1]}\' is not the link"
            await message.reply(response)
        elif len(urls) == 1:
            response = f"Starting downloading video..."
            sent_message = await message.answer(response)
            # Вставляем текст в поле ввода
            # Указываем путь к драйверу браузера (например, Chrome)
            options = Options()
            options.add_experimental_option("prefs", {
                "download.default_directory": "C:\\Users\\Artyomka\\PycharmProjects\\insta_bot",
                "download.prompt_for_download": False,
                "download.directory_upgrade": True,
                "safebrowsing.enabled": True
            })

            driver = webdriver.Chrome(options=options)

            # Заходим на веб-сайт
            driver.get('https://igram.world/')

            # Находим поле ввода по селектору и вставляем текст
            text_input = driver.find_element(By.CSS_SELECTOR, 'input[type="text"]')
            text_input.send_keys(tokens[1])
            time.sleep(1)

            # Находим кнопку по селектору и нажимаем на нее
            button = driver.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
            button.click()

            # Ожидаем 10 секунд
            time.sleep(10)

            # Получаем дерево исходных файлов (Sources)
            script = """
                var sources = Array.from(document.querySelectorAll('script[src], link[rel="stylesheet"][href], img[src]')).map(function(element) {
                    return element.src || element.href;
                });
                return sources;
            """

            sources = driver.execute_script(script)

            # Выводим дерево исходных файлов
            for source in sources:
                print(source)

            # Найти кнопку по селектору и выполнить нажатие
            button = driver.find_element("css selector", ".download-button.mt-3.w-50.m-auto")
            button.click()
            directory_path = 'C:\\Users\\Artyomka\\PycharmProjects\\insta_bot'  # Замените на фактический путь к директории
            extension = '*.mp4'  # Замените на нужное расширение файлов
            count = -1
            while True:
                time.sleep(1)
                video = find_files_by_extension(directory_path, extension)
                if len(video) != -1:
                    await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                                text='Video was downloaded')
                    break
                else:
                    count += 1
                    if count == 0:
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                                    text='Video is downloading')
                    if count == 1:
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                                    text='Video is downloading.')
                    if count == 2:
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                                    text='Video is downloading..')
                    if count == 3:
                        await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                                    text='Video is downloading...')
                        count = -1
            driver.quit()

            # Поиск файлов с указанным расширением в директории
            video = glob.glob(directory_path + '/' + extension)

            # Вывод найденных файлов
            for file in video:
                print(file)
            await bot.edit_message_text(chat_id=message.chat.id, message_id=sent_message.message_id,
                                        text='Sending video!')
            await bot.send_video(chat_id=message.chat.id, video=InputFile(video[0]))
            os.remove(video[0])
            # await message.reply(response)
        else:
            response = f"It is a strange link"
            await message.reply(response)


@dp.message_handler(commands=['info'])
async def say_hello_command(message: types.Message):
    await message.reply(f"Your message id - {message.message_id}\nChat id - {message.chat.id}")


# Start the bot
async def main():
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
