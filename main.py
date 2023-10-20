import requests
import time
import os
from bs4 import BeautifulSoup
import re
import telebot
import logging

# from t0ken import *

is_sent = False

logging.basicConfig(filename='logger.log', level=logging.INFO,
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %H:%M:%S', encoding="utf-8", filemode="w")

API_KEY = "6313360423:AAFnAi6FglZYbnU6hglG04PKLy7Ee9d-Lfw"
channel_id = "@test_apvgk"
bot = telebot.TeleBot(API_KEY)

logging.info('Bot is running...')


# Функция забирает данные о последней выгруженной новости в переменную. Если данных нет создает пустой файл
def file2set(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = file.read()
            return data
    else:
        with open(file_path, 'w'):
            pass


# Функция перезаписывает соответствующий файл, содержащий идентификатор последней отправленнй новости
def add2file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(f'{data}\n')


# Функция отправляет новость, если она ещё не была отправлена
def send_if_upd(path, title, link, id):
    try:
        global is_sent
        dataset = file2set(path)
        if id != dataset:
            add2file(path, id)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
            is_sent = True
            logging.info(f'New message on {path}')
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


def rosavtodor(soup, url):
    parsed = soup.find_all("div", class_='newsList')[0]
    raw_link = parsed.findAll(class_="boxLink")

    link = url + re.findall(r'href="(\/.*?)"', str(raw_link))[0]
    title = parsed.find("p", class_="newsList__text").text.strip()

    return title, link, link


def rosdornii_events(soup, url):
    parsing = soup.findAll("h3",
                           class_="t-1 my-2 t-title с-text-primary l-inherit l-hover-primary l-hover-underline-none transition")[
        0].find('a')
    parsed = re.findall(r'href="\/press-center\/event\/(.*?\/.*)"', str(parsing))[0]

    link = url + parsed
    title = parsing.text.strip()
    # date = soup.find_all("p", class_="t--1 c-text-secondary mb-2")[0].text.strip()
    return title, link, parsed


def rosdornii_news(soup, url):
    parsing = soup.findAll("div", class_="iblock-list-item-text w-md-60 pl-md-4")[0]
    parsed_link = re.findall(r'href="(\/.*?\/.*)"', str(parsing))[0]

    title = parsing.find('a', hidefocus="true")
    if title:
        title = title.get_text(strip=True)

    link = "https://rosdornii.ru" + parsed_link

    try:
        return title, link, parsed_link
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


def nopriz_news(soup, url):
    parsing = soup.find('div', class_='title font_md').find('a')

    title = parsing.text.strip()
    link = url + re.findall(r'href="\/news\/(.*)"', str(parsing))[0]

    return title, link, link


def nopriz_events(soup, url):
    parsing = soup.findAll('div', class_='title font_md')[-1]

    title = parsing.text.strip()
    link = url + re.findall(r'href="\/events\/(.*)"', str(parsing))[0]

    return title, link, link


def proekt_ros_news(soup, url):
    parsing = soup.find('a', class_='nb_link')

    title = parsing.text.strip()
    link = url + re.findall(r'href="/News/([^"]+)"', str(parsing))[0]

    return title, link, link


def nostroy_news(soup, url):
    parsing = soup.find('div', class_="m-info-item__title title font_mlg")

    title = parsing.text.strip()
    link = url + re.findall(r'href="/company/news/([^"]+)"', str(parsing))[0]

    return title, link, link


def nostroy_events(soup, url):
    parsing = soup.find('div', class_='preview-text')

    title = parsing.text.strip()
    link = url + re.findall(r'href="/company/anonsy-meropriyatiy/([^"]+)"', str(parsing))[0]

    return title, link, link


def avtodor_news(soup, url):
    parsing = soup.find('a', class_="press-item-large")

    id = re.findall(r'href="/press/news/([^"]+)"', str(parsing))[0]
    link = url + id
    title = parsing.find('span', class_="press-item-large__h").text.strip()

    return title, link, id


def rosdornii_digest(soup, url):
    parsing = soup.findAll("p",
                           class_="left t-1 my-2 t-title с-text-primary l-inherit l-hover-primary l-hover-underline-none transition")

    parsed_link = re.findall(r'href="(\/.*?\/.*)">Дайджест новостей РФ \((\d\d\.\d\d\.\d\d\d\d)\).*', str(parsing))[
        0]
    parsed_link = "https://rosdornii.ru" + parsed_link[0]

    return null, parsed_link, parsed_link


def rosasfalt(soup, url):
    parsing = soup.find('p', class_="title")

    title = parsing.text.strip()
    id = re.findall(r'href="/about/news/([^"]+)"', str(parsing))[0]
    link = url + id

    return title, link, id


def minstroy(soup, url):
    parsing = soup.find('div', class_="new-text")

    title = parsing.text.strip()
    id = re.findall(r'href="([^"]+)"', str(parsing))[0]
    link = url + id

    return title, link, id


def tk418(soup, url):
    parsing = soup.find('p', class_="news-item")
    title = parsing.text.strip()

    return title, url, title


def gge(soup, url):
    parsing = str(soup.find('a', class_="press-item-inline"))

    link = url + re.findall(r'href="/press-center/news/([^"]+)"', parsing)[0]
    title = soup.find('div', class_="press-item-inline__title").text.strip()

    return title, link, title


# Словарь, где ключ - ссылка на страницу для парсинга,
# значение - кортеж из имени соответствующих функции и файла записи новостей
site_process = {
    'https://rosavtodor.gov.ru': (rosavtodor, 'rosavtodor.txt'),
    'https://rosdornii.ru/press-center/event/': (rosdornii_events, 'rosdornii_events.txt'),
    'https://rosdornii.ru/press-center/news/': (rosdornii_news, 'rosdornii_news.txt'),
    'https://www.nopriz.ru/news/': (nopriz_news, 'nopriz_news.txt'),
    'https://www.nopriz.ru/events/': (nopriz_events, 'nopriz_events.txt'),
    'https://bkdrf.ru/News/': (proekt_ros_news, 'proekt_ros_news.txt'),
    'https://nostroy.ru/company/news/': (nostroy_news, 'nostroy_news.txt'),
    'https://nostroy.ru/company/anonsy-meropriyatiy/': (nostroy_events, 'nostroy_events.txt'),
    'https://russianhighways.ru/press/news/': (avtodor_news, 'avtodor_news.txt'),
    # 'https://rosdornii.ru/press-center/digest/': (rosdornii_digest, 'rosdornii_digest.txt'),
    'https://rosasfalt.org/about/news/': (rosasfalt, 'rosasfalt.txt'),
    'https://minstroyrf.gov.ru/': (minstroy, 'minstroy.txt'),
    'https://tk418.ru/': (tk418, 'tk418.txt'),
    'https://gge.ru/press-center/news/': (gge, 'gge.txt'),
}


def parse_site(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    process_func, path = site_process[url]
    title, link, id = process_func(soup, url)
    send_if_upd(path, title, link, id)


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
            logging.error(f"Ошибка при запуске polling: {e}")
            time.sleep(5)


if __name__ == '__main__':
    main_loop()
