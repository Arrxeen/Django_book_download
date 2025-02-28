from django.core.management.base import BaseCommand
from ...models import Chapter
from ...parsers import parse_chapter
import requests
from bs4 import BeautifulSoup
from time import sleep

class Command(BaseCommand):
    help = 'Парсинг глави з вказаної URL-адреси'
    def handle(self, *args, **options):
        url = 'https://ranobehub.org/ranobe/510-lord-of-the-mysteries'
        tom = 1
        
        page = requests.get(url)

        soup = BeautifulSoup(page.text, "html.parser")

        number = soup.find('div',class_="book-meta-value book-stats").text.split()[0]
        number = self.number
        tom = 1
        chapter = 212
        ono = 0
        try:
            for chapter in range(1, int(number)+1):
                sleep(1)
                chapterr = 486+chapter - ono
                print(chapterr)
                print(f"Парсимо главу {chapterr} з тому {tom}")
                data = parse_chapter(tom, chapterr)
                if "error" in data:
                    self.stdout.write(self.style.ERROR(f"Помилка: {data['error']}"))
                    tom += 1
                    ono += 1

                else:

                    Chapter.objects.create(title=data['title'], content=data['content'], falls_id=data['falseid'])
                    self.stdout.write(self.style.SUCCESS(f"Успішно спарсено: {data['title']}"))
        except:
            tom += 1
        
