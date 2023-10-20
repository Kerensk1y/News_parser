import requests
import time
from bs4 import BeautifulSoup
import re
import telebot
import logging
from t0ken import *

vygr = False

logging.basicConfig(filename='logger.log', level=logging.DEBUG,
                    format='%(levelname)s (%(asctime)s): %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S', encoding="utf-8", filemode="w")

bot = telebot.TeleBot(API_KEY)

logging.info('Bot is running...')


def file2set(file_path):
    dataset = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                dataset.add(line.strip())
    except FileNotFoundError:
        with open(file_path, 'w'):
            pass
    return dataset


def file_add(file_path, data):
    with open(file_path, 'w') as file:
        file.write(f'{data}\n')


def template(path, title, link, ident):
    global vygr
    try:
        dataset = file2set(path)
        if ident not in dataset:
            file_add(path, ident)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
            vygr = True
            logging.info(f'New message on {path}')
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


def rosavtodor():
    path = "rosavtodor.txt"
    URL = "https://rosavtodor.gov.ru"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsed = soup.find_all("div", class_='newsList')[0]
    link = parsed.findAll(class_="boxLink")
    link = URL + re.findall(r'href="(\/.*?)"', str(link))[0]
    title = parsed.find("p", class_="newsList__text").text.strip()
    template(path, title, link, link)


def rosdornii_events():
    path = "rosdornii_events.txt"
    URL = "https://rosdornii.ru/press-center/event/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.findAll("h3",
                           class_="t-1 my-2 t-title с-text-primary l-inherit l-hover-primary l-hover-underline-none transition")[
        0].find('a')
    parsed = re.findall(r'href="\/press-center\/event\/(.*?\/.*)"', str(parsing))[0]
    link = URL + parsed
    title = parsing.text.strip()
    # date = soup.find_all("p", class_="t--1 c-text-secondary mb-2")[0].text.strip()
    template(path, title, link, parsed)


def rosdornii_news():
    path = "rosdornii_news.txt"
    URL = "https://rosdornii.ru/press-center/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.findAll("div", class_="iblock-list-item-text w-md-60 pl-md-4")[0]
    parsed_link = re.findall(r'href="(\/.*?\/.*)"', str(parsing))[0]
    title = parsing.find('a', hidefocus="true")
    if title:
        title = title.get_text(strip=True)
    link = "https://rosdornii.ru" + parsed_link
    try:
        template(path, title, link, parsed_link)
    except Exception as e:
        logging.error(f"Произошла ошибка: {str(e)}")


def nopriz_news():
    path = "nopriz_news.txt"
    URL = "https://www.nopriz.ru/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('div', class_='title font_md').find('a')
    title = parsing.text.strip()
    link = URL + re.findall(r'href="\/news\/(.*)"', str(parsing))[0]
    template(path, title, link, link)


def nopriz_events():
    path = "nopriz_events.txt"
    URL = "https://www.nopriz.ru/events/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.findAll('div', class_='title font_md')[-1]
    title = parsing.text.strip()
    link = URL + re.findall(r'href="\/events\/(.*)"', str(parsing))[0]
    template(path, title, link, link)


def proekt_ros_news():
    path = "proekt_ros_news.txt"
    URL = "https://bkdrf.ru/News/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('a', class_='nb_link')
    title = parsing.text.strip()
    link = URL + re.findall(r'href="/News/([^"]+)"', str(parsing))[0]
    template(path, title, link, link)


def nostroy_news():
    path = "nostroy_news.txt"
    URL = "https://nostroy.ru/company/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('div', class_="m-info-item__title title font_mlg")
    title = parsing.text.strip()
    link = URL + re.findall(r'href="/company/news/([^"]+)"', str(parsing))[0]
    template(path, title, link, link)


def nostroy_events():
    path = "nostroy_events.txt"
    URL = "https://nostroy.ru/company/anonsy-meropriyatiy/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('div', class_='preview-text')
    title = parsing.text.strip()
    link = URL + re.findall(r'href="/company/anonsy-meropriyatiy/([^"]+)"', str(parsing))[0]
    template(path, title, link, link)


def avtodor_news():
    path = "avtodor_news.txt"
    URL = "https://russianhighways.ru/press/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('a', class_="press-item-large")
    id = re.findall(r'href="/press/news/([^"]+)"', str(parsing))[0]
    link = URL + id
    title = parsing.find('span', class_="press-item-large__h").text.strip()
    template(path, title, link, id)


def rosdornii_digest():
    global vygr
    try:
        path = "rosdornii_digest.txt"
        dataset = file2set(path)
        URL = "https://rosdornii.ru/press-center/digest/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.findAll("p",
                               class_="left t-1 my-2 t-title с-text-primary l-inherit l-hover-primary l-hover-underline-none transition")
        parsed_link = re.findall(r'href="(\/.*?\/.*)">Дайджест новостей РФ \((\d\d\.\d\d\.\d\d\d\d)\).*', str(parsing))[0]
        parsed_link = "https://rosdornii.ru" + parsed_link[0]
        if parsed_link not in dataset:
            file_add(path, parsed_link)
            bot.send_message(channel_id, text=f"{parsed_link}")
            vygr = True
    except:
        logging.error(f"Произошла ошибка: {str(e)}")


def rosasfalt():
    path = "rosasfalt.txt"
    URL = "https://rosasfalt.org/about/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('p', class_="title")
    title = parsing.text.strip()
    id = re.findall(r'href="/about/news/([^"]+)"', str(parsing))[0]
    link = URL + id
    template(path, title, link, id)


def minstroy():
    path = "minstroy.txt"
    URL = "https://minstroyrf.gov.ru/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('div', class_="new-text")
    title = parsing.text.strip()
    id = re.findall(r'href="([^"]+)"', str(parsing))[0]
    link = URL + id
    template(path, title, link, id)


def tk418():
    path = "tk418.txt"
    URL = "https://tk418.ru/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('p', class_="news-item")
    title = parsing.text.strip()
    template(path, title, URL, title)


def gge():
    path = "gge.txt"
    URL = "https://gge.ru/press-center/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = str(soup.find('a', class_="press-item-inline"))
    link = URL + re.findall(r'href="/press-center/news/([^"]+)"', parsing)[0]
    title = soup.find('div', class_="press-item-inline__title").text.strip()
    template(path, title, link, title)


def main_loop():
    global vygr
    while True:
        rosavtodor()
        rosdornii_events()
        rosdornii_news()
        rosdornii_digest()
        nopriz_news()
        nopriz_events()
        proekt_ros_news()
        nostroy_news()
        nostroy_events()
        avtodor_news()
        rosasfalt()
        minstroy()
        tk418()
        gge()
        if vygr:
            logging.info('News successfully updated! 15 minute sleep.')
            vygr = False
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
