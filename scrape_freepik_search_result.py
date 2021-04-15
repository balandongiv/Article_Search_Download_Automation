import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
from bs4 import BeautifulSoup as soup
import re
from scrapy.selector import Selector
import pickle
import requests

from urllib.request import Request, urlopen

'''
This is work in progress, while the offline version already ok, but yet to test this online version
'''
# https://www.dataquest.io/blog/web-scraping-tutorial-python/
url = "https://www.freepik.com/search?dates=any&format=search&page=1&query=medical&selection=1&sort=popular"

req = Request(url, headers={'User-Agent': 'Mozilla/5.9'})
webpage = urlopen(req).read()
page_soup = soup(webpage, 'html.parser')
# page = requests.get()
#
# Soup = BeautifulSoup(page.content, 'html.parser')
print(page_soup.prettify())
file_name_with_path = 'freepik_web.html'

with open(file_name_with_path, mode="w", encoding="utf8") as code:
    code.write(str(page_soup.prettify()))

# Saving the objects:

# f = open('my_complete_scopus.pckl', 'wb')
# pickle.dump(all_result, f)
# f.close()
