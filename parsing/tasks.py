from core.celery import app
from .parsers import parse_chapter
from time import sleep
import requests
from bs4 import BeautifulSoup
from .models import WebBook
from django.core.cache import cache


@app.task
def book_find(url, user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    img_tag = 'https://litmir.club/'+soup.find('div',class_='lt34').find('img').get('src')
    title = soup.find('div', class_="lt35").text.strip()
    first_chapter = soup.find('table',class_='lt49').find('a',class_='read').get('href')
    sleep(1)

    WebBook.objects.create(title=title, url_first=first_chapter, urls_parents=url, creater=user, imga=img_tag)


@app.task
def parse_chapter_task(book_id, chapter):
    url = WebBook.objects.get(id=book_id).urls_parents
    url_first = 'https://litmir.club/' +WebBook.objects.get(id=book_id).url_first
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    number = soup.find('td',class_='bd_desc2').find('span',class_='desc2',itemprop ="numberOfPages").text.strip()
    for pg in range(1, 3):
        sleep(1)
        parse_chapter(book_id, chapter)
        chapter += 1
