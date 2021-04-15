import pickle

import requests
from bs4 import BeautifulSoup as Soup
import re
import codecs
def get_each_page(page_soup):
    try:
        paper_author = page_soup.find(attrs={"itemprop": "author"}).text
    except AttributeError:
        paper_author='No Available'

    try:
        paper_title = page_soup.find(attrs={"itemprop": "name"}).text
    except AttributeError:
        paper_title ='No Available'

    try:
        paper_url = page_soup.find(attrs={"itemprop": "url"}).text
    except AttributeError:
        paper_url='No Available'

    try:
        paper_publisher = page_soup.find(attrs={"itemprop": "publisher"}).text
    except AttributeError:
        paper_publisher='No Available'

    try:
        paper_abstract = page_soup.find(attrs={"itemprop": "description"}).text
    except AttributeError:
        paper_abstract='No Available'

    try:
        paper_about = page_soup.find(attrs={"itemprop": "about"}).text
    except AttributeError:
        paper_about='No Available'

    try:
        paper_date_published = page_soup.find(attrs={"itemprop": "datePublished"}).text
    except AttributeError:
        paper_date_published='No Available'

    document_statusx = dict(paper_author=paper_author, paper_title=paper_title,
                            paper_url=paper_url, paper_publisher=paper_publisher,
                            paper_abstract=paper_abstract, paper_about=paper_about,
                            paper_datePublished=paper_date_published)
    return document_statusx


def flatten(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i + 1] = items[i]
    return items

with open('oatd_href_search_pages.pickle', 'rb') as handle:
    all_result = pickle.load(handle)

test_list = flatten(all_result[:])
all_website_scrape=[]
base_add='https://oatd.org/oatd/'
for url_to_pass in test_list:
    # what_this=
    url_to_passx=base_add+url_to_pass
    page = requests.get(url_to_passx)
    if page.status_code==200:
        page_soup = Soup(page.text, 'html.parser')
        # result_scrape=get_each_page(page_soup)
        all_website_scrape.append(get_each_page(page_soup))
        x=1

