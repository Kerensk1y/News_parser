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
    path = "rosavtodor.txt"
    dataset = file_set(path)
    URL = "https://rosavtodor.gov.ru"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsed = str(soup.find_all("a", class_='boxLink')[0])
    if parsed not in dataset:
        dataset.add(parsed)
        file_add(path, parsed)
        post = soup.find("div", class_="newsMain-item size1")
        title = post.find("p", class_="subTitle").text.strip()
        description = post.find("div", class_="text").text.strip()
        url = soup.find_all('a', class_='boxLink')[0]
        link = URL + re.findall(r'href="(\/.*?)"', str(url))[0]
        bot.send_message(channel_id, text=f"{link}\n{title}\n{description}")


def rosdornii_events():
    path = "rosdornii_events.txt"
    dataset = file_set(path)
    URL = "https://rosdornii.ru/press-center/event/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.findAll("div", class_="NewsCalNews")[-1]
    parsed = re.findall(r'href="(\/.*?\/.*)"', str(parsing))
    if parsed[0] not in dataset:
        dataset.add(parsed[0])
        file_add(path, parsed[0])
        title = parsing.find("a", class_="t--1 mb-2 sf-link sf-link-theme c-text-primary").text.strip()
        url = parsing.find("a", class_="t--1 mb-2 sf-link sf-link-theme c-text-primary")
        link = "https://rosdornii.ru" + url.get("href")
        # достаю дату
        date = soup.find_all("a", class_="events btn-primary")[-1]
        dates = re.findall(r'date=(\d\d\.\d\d\.\d\d\d\d)', str(date))
        if dates:
            date = dates[0]
        bot.send_message(channel_id, text=f"{link}\n{title}\n{date}")


def rosdornii_news():
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
        parsed_link = "https://rosdornii.ru" + parsed_link
        bot.send_message(channel_id, text=f"{parsed_link}\n{title}")


def rosdornii_digest():
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


def nopriz_events():
    path = "nopriz_events.txt"
    dataset = file_set(path)
    URL = "https://www.nopriz.ru/news/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    parsing = soup.find('div', class_='title font_md').find('a')
    title = parsing.text.strip()
    link = URL + re.findall(r'href="\/news\/(.*)"', str(parsing))[0]
    if link not in dataset:
        file_add(path, link)
        print(link, title)
        bot.send_message(channel_id, text=f"{link}\n{title}")


while True:
    rosavtodor()
    rosdornii_events()
    rosdornii_news()
    rosdornii_digest()
    nopriz_events()
    print("Сплю... Проснусь через полчаса")
    time.sleep(1800)

bot.polling()
