from lxml import etree
from bs4 import BeautifulSoup as soup
import re

'''
This is the offline version to scrape the freepik webpage
'''
url = r'html_scopus_search_result_from_view_more.html'

all_result = []
with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')



    page_end_page = page_soup.find(attrs={"name": "endPage"})['value']

    page_current_page = page_soup.find(attrs={"name": "currentPage"})['value']

    for div_tag in page_soup.find_all('div', {'class': 'col-md-6 center-block text-center'}):
        for litag in div_tag.find_all('li'):
            print(litag.text)


