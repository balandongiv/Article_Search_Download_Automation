
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as Soup
import re
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time
import requests

url = r'html_oatd_search_pages.html '

with open(url, 'r', encoding='utf-8') as f:
    page_soup = Soup(f, 'html.parser')

    publication_date_list = page_soup.find_all('p', {'class': 'links'})
    x=1

    # paper_author = page_soup.find(attrs={"itemprop": "author"}).text
    # paper_title = page_soup.find(attrs={"itemprop": "name"}).text
    # paper_url = page_soup.find(attrs={"itemprop": "url"}).text
    # paper_publisher = page_soup.find(attrs={"itemprop": "publisher"}).text
    # paper_abstract = page_soup.find(attrs={"itemprop": "description"}).text
    # paper_about = page_soup.find(attrs={"itemprop": "about"}).text
    # paper_datePublished = page_soup.find(attrs={"itemprop": "datePublished"}).text
    #
    # document_status = dict(paper_author=paper_author, paper_title=paper_title,
    #                        paper_url=paper_url, paper_publisher=paper_publisher,
    #                        paper_abstract=paper_abstract,paper_about=paper_about,
    #                        paper_datePublished=paper_datePublished)
    '''
    Temporary disable
        title = "This is typically the date on which the record first entered the local system"
        data_accession_class = page_soup.find(attrs={"title": title}).text
        x=1
        if data_accession_class != 1:
            paper_datePublished = page_soup.find(attrs={"itemprop": "datePublished"}).text
        else:
            publication_date_list = page_soup.find_all('td', {'itemprop': 'datePublished'})
            index_paper_date = 9
            for litag in publication_date_list:
                if index_paper_date == 0:
                    paper_datePublished = page_soup.find(attrs={"itemprop": "datePublished"}).text
                    paper_author = litag.text
                else:
                    paper_dateAccessioned = litag.textxt
    '''
