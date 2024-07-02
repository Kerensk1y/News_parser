import re
import logging
from bs4 import BeautifulSoup
import requests

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

    return "Дайджест новостей", parsed_link, parsed_link


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

def minstrans_preview(soup, url):
    parsing = soup.find('a', class_ = "news-text fc-blue")
    title = parsing.text.strip()
    link = url + re.findall(r'(/\d+)$', re.findall(r'href="([^"]*)"', str(parsing))[0])[0]
    id = re.findall(r'/(\d+)$', re.findall(r'href="([^"]*)"', str(parsing))[0])[0]
    return title, link, id