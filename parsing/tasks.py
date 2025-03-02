from core.celery import app
from .parsers import parse_chapter
from time import sleep
import requests
from bs4 import BeautifulSoup
from .models import WebBook, Chapter


@app.task
def book_find(url, user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    img_tag = soup.find('img', class_="lt32").get('src')
    title = soup.find('div', class_="lt35").text.strip()
    first_chapter = soup.find('table',class_='lt49').find('a',class_='read').get('href')

    WebBook.objects.create(title=title, url_first=first_chapter, urls_parents=url, creater=user)


@app.task
def parse_chapter_task(book_id):
    url = WebBook.objects.get(id=book_id).urls_parents
    url_first = 'https://litmir.club/' +WebBook.objects.get(id=book_id).url_first
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    number = soup.find('td',class_='bd_desc2').find('span',class_='desc2',itemprop ="numberOfPages").text.strip()
    pg = 1
    for pg in range(1, 3):
        sleep(1)
        parse_chapter(book_id, pg)
        pg += 1
