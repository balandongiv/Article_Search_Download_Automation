from lxml import etree
from bs4 import BeautifulSoup as soup
import re

'''
This is the offline version to scrape the freepik webpage
'''
url = r'html_freepik_search_result.html'

all_result = []
with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')
    # print(page_soup.prettify())
    dom = etree.HTML(str(page_soup))
    pagination_string = page_soup.find('span', {'class': 'pagination__pages'}).text
    number_of_pages = int(re.findall('\d+', pagination_string)[0])
    g_data = page_soup.find_all("figure", {"class": "showcase__item"})
    size_total_display = len(g_data)

    for number_of_display in range(0, size_total_display):
        data_id = g_data[number_of_display].find("a", {"class": "showcase__link"})['data-id']  # works
        data_href_link = g_data[number_of_display].find("a", {"class": "showcase__link"})['href']  # works

        image_url_long = g_data[number_of_display].find("a", {"class": "showcase__link"}).img['data-src']  # works
        image_url = re.split(r"size", image_url_long)[0][:-1]

        image_title = g_data[number_of_display].find("a", {"class": "showcase__link"}).img['alt']  # works

        report_status = dict(data_id=data_id, image_title=image_title,
                             image_url=image_url, data_href_link=data_href_link)

        all_result.append(report_status)


stop_me = 1
