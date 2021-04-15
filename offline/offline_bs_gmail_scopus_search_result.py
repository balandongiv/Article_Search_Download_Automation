
from bs4 import BeautifulSoup as soup


'''
Using Python and BeautifulSoup (saved webpage source codes into a local file)
https://stackoverflow.com/a/21577649/6446053
'''

url = r'html_gmail_scopus_search.html '
page = open(url)
page_soup = soup(page.read(), 'html.parser')
print(page_soup.prettify())

document_idx = 0
str_terminator='View all new results in Scopus'
paper_author = []
author_idx = 1
get_str_scopus_redirect = None
while get_str_scopus_redirect != str_terminator:
    try:
        get_str_scopus_redirect = page_soup.select(f'body > table.dataTable > tbody > tr:nth-child({author_idx:d}) > td > a')[0].text
        author_idx = author_idx + 1
    except IndexError:
        get_str_scopus_redirect = 1

papers_href_scopus = page_soup.select(f'body > table.dataTable > tbody > tr:nth-child({author_idx-1:d}) > td > a')[0]['href']





