from bs4 import BeautifulSoup
import requests
import random

s = requests.get('https://litmir.club/bd/?b=939310')
soup = BeautifulSoup(s.text, 'html.parser')

  

first_chapter = 'https://litmir.club/'+soup.find('div',class_='lt34').find('img').get('src')

print(first_chapter)