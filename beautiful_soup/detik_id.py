import time
import requests
import re
from urllib.parse import *
from bs4 import BeautifulSoup

#Input URL
url = input('Input Bukalapak Review URL :')
print(url)
print("Getting URL...")
time.sleep(1)

#Get HTML From URL
print("Requesting to URL")
r = requests.get(url)
time.sleep(1)

#Analyze with BeautifulSoup Library
print("Analize with BeautifulSoup")
soup = BeautifulSoup(r.text, 'html.parser')
time.sleep(1)

comment_list= []
# page = soup.find('div', attrs={'class': 'detail_text'}).text
# print(page)

page = soup.find('div', attrs={'class': 'detail_text'})

for child in page.find_all("div"):
    child.decompose()
for script in page.find_all("script"):
    script.decompose()
for video in page.find_all('a', attrs={'class': 'embed video20detik'}):
    video.decompose()
# print(page.get_text())
regexx = re.sub(r"\s+", " ", page.get_text())
print(regexx)