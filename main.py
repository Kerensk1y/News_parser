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
    with open(file_path, 'a') as file:
        file.write(f'{data}\n')


def rosavtodor(message):
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
        print(link, title, description)
        bot.send_message(channel_id, text=f"{link}\n{title}\n{description}")


'''
def rosdornii():
    path = "rosdornii.txt"
    dataset = file_set(path)
    URL = "https://rosdornii.ru/press-center/event/"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    base = soup.findAll("div", class_="NewsCalNews")
    parsed = base[-1]
    # создаю базу url'ей со страницы
    base = re.findall(r'href="(\/.*?\/.*)"', str(base))
    # достаю инфу из последнего поста
    title = parsed.find("a", class_="t--1 mb-2 sf-link sf-link-theme c-text-primary").text.strip()
    url = parsed.find("a", class_="t--1 mb-2 sf-link sf-link-theme c-text-primary")
    url = "https://rosdornii.ru" + url.get("href")
    # достаю дату
    date = soup.find_all("a", class_="events btn-primary")[-1]
    dates = re.findall(r'date=(\d\d\.\d\d\.\d\d\d\d)', str(date))
    if dates:
        date = dates[0]

    return date, url, title

'''


@bot.message_handler(commands=['start'])
def commands(message):
    while True:
        rosavtodor(message)
        time.sleep(1800)


bot.polling()
