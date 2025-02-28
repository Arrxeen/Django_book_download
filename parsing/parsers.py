from bs4 import BeautifulSoup
import requests
from .models import Chapter
from time import sleep


def parse_chapter(tom, chapters):
        print(f"Починаємо парсити том {tom}, главу {chapters}")
        url = f"https://ranobehub.org/ranobe/510/{tom}/{chapters}"
        page = requests.get(url)
        if page.status_code != 200:
            tom += 1
            parse_chapter(tom, chapters)
        soup = BeautifulSoup(page.text, "html.parser")
        header = soup.find('h1', class_="ui header")
        title = header.text.strip()
        
        # Обчислення falseid з заголовку
        parts = title.split()
        falseid = parts[1].split('.')[0]

        # Збираємо текст глави
        paragraphs = soup.find_all('p')[:-4]
        content = "\n".join(p.text.strip() for p in paragraphs)

        # Створюємо об'єкт Chapter
        Chapter.objects.create(title=title, content=content, falls_id=falseid)
        print(f"Успішно спарсено: {title}")

