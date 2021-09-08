import time
import requests
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
#Condition if the URL have page
if soup.find('li', attrs={'class': 'c-pagination__item'}):
    # get pagging data
    print("Getting pagging data")
    page = soup.find_all('li', attrs={'class': 'c-pagination__item'})
    time.sleep(1)

    page_count = 0
    for a in page:
        page_soup = BeautifulSoup(str(a), 'html.parser')
        if not page_soup.find('a', attrs={'class': 'c-pagination__btn'}):
            page_count += 1
            if "?page" in url:
                url_parse = urlparse(url=url)
                query = parse_qs(url_parse.query)
                if int(query["page"][0]) == page_count:
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    result = soup.find_all('li', attrs={'class': 'c-list-ui__item js-review-item'})
                    for data in result:
                        author = data.find('span',
                                           attrs={'class': 'u-txt--small u-display-inline-block u-mrgn-right--1'}).text
                        date = data.find('span', attrs={
                            'class': 'u-txt--small u-display-inline-block qa-product-review-date'}).text
                        title = data.find('a', attrs={'class': 'u-txt--bold u-fg--black u-txt--no-decoration'}).text
                        comment = data.find('p', attrs={
                            'class': 'u-mrgn-bottom--2 u-txt--break-word u-fg--black qa-product-review-content'}).text
                        comment_data = {
                            "author": author.replace("Oleh ", ""),
                            "date": date.split(',')[0],
                            "comment_title": title,
                            "comment_desc": comment
                        }
                        comment_list.append(comment_data)
                else:
                    url = url.replace("page="+ str(query["page"][0]),"page="+str(page_count))
                    r = requests.get(url)
                    soup = BeautifulSoup(r.text, 'html.parser')
                    result = soup.find_all('li', attrs={'class': 'c-list-ui__item js-review-item'})
                    for data in result:
                        author = data.find('span',
                                           attrs={'class': 'u-txt--small u-display-inline-block u-mrgn-right--1'}).text
                        date = data.find('span', attrs={
                            'class': 'u-txt--small u-display-inline-block qa-product-review-date'}).text
                        title = data.find('a', attrs={'class': 'u-txt--bold u-fg--black u-txt--no-decoration'}).text
                        comment = data.find('p', attrs={
                            'class': 'u-mrgn-bottom--2 u-txt--break-word u-fg--black qa-product-review-content'}).text
                        comment_data = {
                            "author": author.replace("Oleh ", ""),
                            "date": date.split(',')[0],
                            "comment_title": title,
                            "comment_desc": comment
                        }
                        comment_list.append(comment_data)
            else:
                url = url + "?page=" + str(page_count)
                r = requests.get(url)
                soup = BeautifulSoup(r.text, 'html.parser')
                result = soup.find_all('li', attrs={'class': 'c-list-ui__item js-review-item'})
                for data in result:
                    author = data.find('span', attrs={'class': 'u-txt--small u-display-inline-block u-mrgn-right--1'}).text
                    date = data.find('span', attrs={'class': 'u-txt--small u-display-inline-block qa-product-review-date'}).text
                    title = data.find('a', attrs={'class': 'u-txt--bold u-fg--black u-txt--no-decoration'}).text
                    comment = data.find('p', attrs={'class': 'u-mrgn-bottom--2 u-txt--break-word u-fg--black qa-product-review-content'}).text
                    comment_data = {
                        "author": author.replace("Oleh ", ""),
                        "date": date.split(',')[0],
                        "comment_title": title,
                        "comment_desc": comment
                    }
                    comment_list.append(comment_data)
    print(comment_list)

    # print(page_count)
    #Create the result
    # print("Getting the result")
    result = soup.find_all('li', attrs={'class': 'c-list-ui__item js-review-item'})
    time.sleep(1)

    # print("Here is the result")
    # print(page)
    # print(len(result))
#
else:
    result = soup.find_all('li', attrs={'class': 'c-list-ui__item js-review-item'})
    for data in result:
        author = data.find('span', attrs={'class': 'u-txt--small u-display-inline-block u-mrgn-right--1'}).text
        date = data.find('span', attrs={'class': 'u-txt--small u-display-inline-block qa-product-review-date'}).text
        title = data.find('p', attrs={'class': 'u-mrgn-bottom--0 u-mrgn-top--2 u-txt--bold u-fg--black'}).text
        comment = data.find('p', attrs={'class': 'u-mrgn-bottom--2 u-txt--break-word u-fg--black qa-product-review-content'}).text
        comment_data = {
            "author": author.replace("Oleh ", ""),
            "date": date.split(',')[0],
            "comment_title": title,
            "comment_desc": comment
        }
        comment_list.append(comment_data)
    print(comment_list)