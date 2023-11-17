import requests
import time
import os
from bs4 import BeautifulSoup
import telebot
import logging
from token import *
from web_pages import *

is_sent = False

logging.basicConfig(filename='logger.log', level=logging.INFO,
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %H:%M:%S', encoding="utf-8", filemode="w")

bot = telebot.TeleBot(API_KEY)

logging.info('Bot is running...')


# Функция забирает данные о последней выгруженной новости в переменную. Если данных нет создает пустой файл
def file_to_str(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    else:
        with open(file_path, 'w') as file:
            file.write('')
        return ''


# Функция перезаписывает соответствующий файл, содержащий идентификатор последней отправленнй новости
def write_to_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(f'{data}\n')


# Функция отправляет новость, если она ещё не была отправлена
def send_if_upd(path, title, link, id):
    try:
        global is_sent
        dataset = file_to_str(path)
        if id not in dataset:
            write_to_file(path, id)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
            is_sent = True
            logging.info(f'New message on {path}')
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


# Словарь, где ключ - ссылка на страницу для парсинга,
# значение - кортеж из имени соответствующих функции и файла записи новостей
site_process = {
    'https://rosavtodor.gov.ru': (rosavtodor, 'db/rosavtodor.txt'),
    'https://rosdornii.ru/press-center/event/': (rosdornii_events, 'db/rosdornii_events.txt'),
    'https://rosdornii.ru/press-center/news/': (rosdornii_news, 'db/rosdornii_news.txt'),
    'https://www.nopriz.ru/news/': (nopriz_news, 'db/nopriz_news.txt'),
    'https://www.nopriz.ru/events/': (nopriz_events, 'db/nopriz_events.txt'),
    'https://bkdrf.ru/News/': (proekt_ros_news, 'db/proekt_ros_news.txt'),
    'https://nostroy.ru/company/news/': (nostroy_news, 'db/nostroy_news.txt'),
    'https://nostroy.ru/company/anonsy-meropriyatiy/': (nostroy_events, 'db/nostroy_events.txt'),
    'https://russianhighways.ru/press/news/': (avtodor_news, 'db/avtodor_news.txt'),
    'https://rosdornii.ru/press-center/digest/': (rosdornii_digest, 'db/rosdornii_digest.txt'),
    'https://rosasfalt.org/about/news/': (rosasfalt, 'db/rosasfalt.txt'),
    'https://minstroyrf.gov.ru/': (minstroy, 'db/minstroy.txt'),
    'https://tk418.ru/': (tk418, 'db/tk418.txt'),
    'https://gge.ru/press-center/news/': (gge, 'db/gge.txt'),
}


def parse_site(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")

        process_func, path = site_process[url]
        title, link, id = process_func(soup, url)
        send_if_upd(path, title, link, id)
    except Exception as e:
        logging.error(f"Ошибка при парсинге страницы {url}: {str(e)}")
        time.sleep(5)


# Функция, содержащая петлю, выполняющую весь парсинг
def main_loop():
    global is_sent
    while True:
        for url in site_process.keys():
            parse_site(url)
        if is_sent:
            logging.info('News successfully updated! 15 minute sleep.')
            is_sent = False
        time.sleep(15 * 60)


def poll():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.error(f"Ошибка при запуске polling: {str(e)}")
            time.sleep(5)


if __name__ == '__main__':
    main_loop()
