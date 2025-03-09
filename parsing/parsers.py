from bs4 import BeautifulSoup
import requests
from .models import Chapter, WebBook
from time import sleep



def parse_chapter(book_id, pg):
    print(f"Починаємо парсити chapter {pg}")
    a = []
    url = 'https://litmir.club/' + WebBook.objects.get(id=book_id).url_first 
    title = f"Глава {pg}"
    if pg > 1:
        url = f"{url}&p={pg}"

    page = requests.get(url)
    if page.status_code != 200:
        print(f"Помилка {page.status_code}")
        
    sleep(1)
    soup = BeautifulSoup(page.text, "html.parser")

    paragraphs = soup.find('div', class_='page_text')

    for data in paragraphs:
        if data.find_all_next('p'):
            a.append(data.text)
    # Отримуємо об'єкт WebBook
    book = WebBook.objects.get(id=book_id)

    # Створюємо об'єкт Chapter
    Chapter.objects.create(title=title, content=a, book=book)
    print(f"Успішно спарсено: {title}")

