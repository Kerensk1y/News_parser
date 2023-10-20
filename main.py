import requests
import time
from bs4 import BeautifulSoup
import re
import telebot
from t0ken import *

bot = telebot.TeleBot(API_KEY)
print("run in progress...")


def file_set(file_path):
    dataset = set()
    try:
        with open(file_path, 'r') as file:
            for line in file:
                dataset.add(line.strip())
    except FileNotFoundError:
        # Если файла нет, просто создаем его и не делаем ничего с множеством
        with open(file_path, 'w'):
            pass
    return dataset


def file_add(file_path, data):
    with open(file_path, 'w') as file:
        file.write(f'{data}\n')


def rosavtodor():
    try:
        path = "rosavtodor.txt"
        dataset = file_set(path)
        URL = "https://rosavtodor.gov.ru"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsed = soup.find_all("div", class_='newsList')[0]
        link = parsed.findAll(class_="boxLink")
        link = URL + re.findall(r'href="(\/.*?)"', str(link))[0]
        if link not in dataset:
            dataset.add(link)
            file_add(path, link)
            title = parsed.find("p", class_="newsList__text").text.strip()
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def rosdornii_events():
    try:
        path = "rosdornii_events.txt"
        dataset = file_set(path)
        URL = "https://rosdornii.ru/press-center/event/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.findAll("h3",
                               class_="t-1 my-2 t-title с-text-primary l-inherit l-hover-primary l-hover-underline-none transition")[
            0].find('a')
        parsed = re.findall(r'href="\/press-center\/event\/(.*?\/.*)"', str(parsing))[0]
        if parsed not in dataset:
            dataset.add(parsed)
            file_add(path, parsed)
            link = URL + parsed
            title = parsing.text.strip()
            # достаю дату
            date = soup.find_all("p", class_="t--1 c-text-secondary mb-2")[0].text.strip()
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def rosdornii_news():
    try:
        path = "rosdornii_news.txt"
        dataset = file_set(path)
        URL = "https://rosdornii.ru/press-center/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.findAll("div", class_="iblock-list-item-text w-md-60 pl-md-4")[0]
        parsed_link = re.findall(r'href="(\/.*?\/.*)"', str(parsing))[0]
        if parsed_link not in dataset:
            dataset.add(parsed_link)
            file_add(path, parsed_link)
            title = parsing.find('a', hidefocus="true")
            if title:
                title = title.get_text(strip=True)
            link = "https://rosdornii.ru" + parsed_link
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def rosdornii_digest():
    try:
        path = "rosdornii_digest.txt"
        dataset = file_set(path)
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
    except:
        pass

def nopriz_news():
    try:
        path = "nopriz_news.txt"
        dataset = file_set(path)
        URL = "https://www.nopriz.ru/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('div', class_='title font_md').find('a')
        title = parsing.text.strip()
        link = URL + re.findall(r'href="\/news\/(.*)"', str(parsing))[0]
        if link not in dataset:
            file_add(path, link)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def nopriz_events():
    try:
        path = "nopriz_events.txt"
        dataset = file_set(path)
        URL = "https://www.nopriz.ru/events/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.findAll('div', class_='title font_md')[-1]
        title = parsing.text.strip()
        link = URL + re.findall(r'href="\/events\/(.*)"', str(parsing))[0]
        if link not in dataset:
            file_add(path, link)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def proekt_ros_news():
    try:
        path = "proekt_ros_news.txt"
        dataset = file_set(path)
        URL = "https://bkdrf.ru/News/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('a', class_='nb_link')
        title = parsing.text.strip()
        link = URL + re.findall(r'href="/News/([^"]+)"', str(parsing))[0]
        if link not in dataset:
            file_add(path, link)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def nostroy_news():
    try:
        path = "nostroy_news.txt"
        dataset = file_set(path)
        URL = "https://nostroy.ru/company/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('div', class_="m-info-item__title title font_mlg")
        title = parsing.text.strip()
        link = URL + re.findall(r'href="/company/news/([^"]+)"', str(parsing))[0]
        if link not in dataset:
            file_add(path, link)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def nostroy_events():
    try:
        path = "nostroy_events.txt"
        dataset = file_set(path)
        URL = "https://nostroy.ru/company/anonsy-meropriyatiy/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('div', class_='preview-text')
        title = parsing.text.strip()
        link = URL + re.findall(r'href="/company/anonsy-meropriyatiy/([^"]+)"', str(parsing))[0]
        if link not in dataset:
            file_add(path, link)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass


def avtodor_news():
    try:
        path = "avtodor_news.txt"
        dataset = file_set(path)
        URL = "https://russianhighways.ru/press/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('a', class_="press-item-large")
        id = re.findall(r'href="/press/news/([^"]+)"', str(parsing))[0]
        if id not in dataset:
            file_add(path, id)
            link = URL + id
            title = parsing.find('span', class_="press-item-large__h").text.strip()
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass


def rosasfalt():
    try:
        path = "rosasfalt.txt"
        dataset = file_set(path)
        URL = "https://rosasfalt.org/about/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('p', class_="title")
        title = parsing.text.strip()
        id = re.findall(r'href="/about/news/([^"]+)"', str(parsing))[0]
        if id not in dataset:
            file_add(path, id)
            link = URL + id
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def minstroy():
    try:
        path = "minstroy.txt"
        dataset = file_set(path)
        URL = "https://minstroyrf.gov.ru/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('div', class_="new-text")
        title = parsing.text.strip()
        id = re.findall(r'href="([^"]+)"', str(parsing))[0]
        if id not in dataset:
            file_add(path, id)
            link = URL + id
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def tk418():
    try:
        path = "tk418.txt"
        dataset = file_set(path)
        URL = "https://tk418.ru/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = soup.find('p', class_="news-item")
        title = parsing.text.strip()
        if title not in dataset:
            file_add(path, title)
            bot.send_message(channel_id, text=f"{title}\n{URL}")
    except:
        pass


def faufcc():
    try:
        path = "faufcc.txt"
        dataset = file_set(path)
        URL = "https://www.faufcc.ru/archive/key-news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = str(soup.find('div', class_="news-item-content-wrapper"))
        link = "https://www.faufcc.ru" + re.findall(r'href="([^"]+)"', parsing)[0]
        title = re.findall(r'href="[^"]+">(.*)<\/a>', parsing)[0]
        if title not in dataset:
            file_add(path, title)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def gge():
    try:
        path = "gge.txt"
        dataset = file_set(path)
        URL = "https://gge.ru/press-center/news/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        parsing = str(soup.find('a', class_="press-item-inline"))
        link = URL + re.findall(r'href="/press-center/news/([^"]+)"', parsing)[0]
        title = soup.find('div', class_="press-item-inline__title").text.strip()
        if title not in dataset:
            file_add(path, title)
            bot.send_message(channel_id, text=f'<a href="{link}">{title}</a>', parse_mode='html')
    except:
        pass

def main_loop():
    while True:
        try:
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
            faufcc()
            print("Сплю... Проснусь через 15 минут")
            time.sleep(15 * 60)
        except Exception as e:
            print(f"Произошла ошибка: {e}")
            time.sleep(60)  # Подождать 1 минуту перед повторной попыткой


def poll():
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка при запуске polling: {e}")
            time.sleep(5)  # Подождать 5 секунд перед повторной попыткой


if __name__ == '__main__':
    main_loop()
