from core.celery import app
from .parsers import parse_chapter
from time import sleep
import requests
from bs4 import BeautifulSoup
from .models import WebBook

@app.task
def book_find(url, user_id):
    from django.contrib.auth.models import User
    user = User.objects.get(id=user_id)
    
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    img_tag = soup.find('img', class_="__posterbox").get('data-src')
    title = soup.find('h1', class_="ui huge header").text.strip()
    first_chapter = soup.find('div', class_='mobile only').find('a').get('href')

    WebBook.objects.create(title=title, url=first_chapter, creater=user)

    

@app.task
def parse_chapter_task(tom, chapters):
    url = 'https://ranobehub.org/ranobe/510-lord-of-the-mysteries' 
    page = requests.get(url)
    soup = BeautifulSoup(page.text, "html.parser")
    number = soup.find('div',class_="book-meta-value book-stats").text.split()[0]
    for chapter in range(1, int(number)+1):
        sleep(1)
        chapterr = chapters - 1 + chapter
        parse_chapter(tom, chapterr)


# Compare this snippet from parsing/models.py: