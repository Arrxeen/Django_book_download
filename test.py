from bs4 import BeautifulSoup
import requests
import random

s = requests.get('https://litmir.club/bd/?b=939310')
soup = BeautifulSoup(s.text, 'html.parser')

  

first_chapter = soup.find('table',class_='lt49').find('a',class_='read').get('href')

print(first_chapter)