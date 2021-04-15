import pickle

import requests
from bs4 import BeautifulSoup as Soup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

'''
Access the website or pdf link directly
        result_div_tag = page_soup.find_all('div', {'class': 'result'})
        all_href_append = []
        for try_search in result_div_tag:
            what_this=try_search.find('p', {'class': 'links'})
            all_href_append.append(what_this.text)
'''


def flatten(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i + 1] = items[i]
    return items


class ScrapeOatd:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()

        # Load current user default profile
        # current_user=get_username()
        # current_user = getuser()
        current_user = 'rpb'
        chrome_options.add_argument(
            r"--user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(current_user))
        self.browser = webdriver.Chrome(
            executable_path=r"C:Browsers\chromedriver.exe",
            options=chrome_options)

    @staticmethod
    def get_each_page(page_soup):

        def get_att(attr):
            try:
                attr_output = page_soup.find(attrs=attr).text
            except AttributeError:
                attr_output = 'No Available'
            return attr_output

        # try:
        #     paper_author = page_soup.find(attrs={"itemprop": "author"}).text
        # except AttributeError:
        #     paper_author = 'No Available'
        paper_author = get_att({"itemprop": "author"})

        # try:
        #     paper_title = page_soup.find(attrs={"itemprop": "name"}).text
        # except AttributeError:
        #     paper_title = 'No Available'
        paper_title = get_att({"itemprop": "name"})

        # try:
        #     paper_url = page_soup.find(attrs={"itemprop": "url"}).text
        # except AttributeError:
        #     paper_url = 'No Available'
        paper_url = get_att({"itemprop": "url"})

        # try:
        #     paper_publisher = page_soup.find(attrs={"itemprop": "publisher"}).text
        # except AttributeError:
        #     paper_publisher = 'No Available'

        paper_publisher = get_att({"itemprop": "publisher"})

        # try:
        #     paper_abstract = page_soup.find(attrs={"itemprop": "description"}).text
        # except AttributeError:
        #     paper_abstract = 'No Available'

        paper_abstract = get_att({"itemprop": "description"})

        # try:
        #     paper_about = page_soup.find(attrs={"itemprop": "about"}).text
        # except AttributeError:
        #     paper_about = 'No Available'

        paper_about= get_att({"itemprop": "about"})

        # try:
        #     paper_date_published = page_soup.find(attrs={"itemprop": "datePublished"}).text
        # except AttributeError:
        #     paper_date_published = 'No Available'

        paper_date_published = get_att({"itemprop": "datePublished"})
        document_statusx = dict(paper_author=paper_author, paper_title=paper_title,
                                paper_url=paper_url, paper_publisher=paper_publisher,
                                paper_abstract=paper_abstract, paper_about=paper_about,
                                paper_datePublished=paper_date_published)
        return document_statusx

    @staticmethod
    def scrape_search_result_per_page(page_soup):
        result_div_tag = page_soup.find_all('p', {'class': 'shareIcon'})
        all_href_append = []
        for extract_href in result_div_tag:
            what_this = extract_href.find('a')
            if what_this.text == 'Record Details':
                all_href_append.append(what_this['href'])
        return all_href_append

    @staticmethod
    def get_available_page(page_soup_search_result):
        list_page_visible = []
        for div_tag in page_soup_search_result.find_all('p', {'class': 'paging'}):
            for litag in div_tag.find_all('a'):
                str_litag = litag.text
                try:
                    list_page_visible.append(int(str_litag))
                except ValueError:
                    list_page_visible.append('NA')
        return list_page_visible

    @staticmethod
    def filter_by_type(list_to_test, type_of):
        return [n for n in list_to_test if isinstance(n, type_of)]

    def move_next_page(self, page_soup_search_result):

        page_current_page_old_str = page_soup_search_result.find('span', attrs={'class': 'this-page'}).text
        page_current_page_old = int(''.join(filter(str.isalnum, page_current_page_old_str)))

        list_page_visible = self.get_available_page(page_soup_search_result)
        shift_no_page = 3

        page_current_page_new = page_current_page_old + 1
        index_location = list_page_visible.index(page_current_page_new)  # not tested as of Sunday
        current_page_no = shift_no_page + index_location

        some_termination_condition = []
        attempt_to_refresh = 0
        refresh_error = []

        while some_termination_condition != 1:
            try:
                WebDriverWait(self.browser, 8).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, f'#results > p:nth-child(3) > a:nth-child({current_page_no:d})'))).click()

            except (
                    NoSuchElementException, TimeoutException, IndexError, ElementClickInterceptedException,
                    TypeError) as e:
                WebDriverWait(self.browser, 8).until(
                    EC.visibility_of_element_located(
                        (By.CSS_SELECTOR, f'#results > p:nth-child(4) > a:nth-child({current_page_no:d})'))).click()

                # Check current page if similar to our intended page
            try:
                page_soup_search_result = Soup(self.browser.page_source, 'html.parser')
                page_current_page_old_str = page_soup_search_result.find('span', attrs={'class': 'this-page'}).text
                page_current_page = int(''.join(filter(str.isalnum, page_current_page_old_str)))
                #
                if page_current_page == page_current_page_new:
                    some_termination_condition = 1
                    # print('yes, intended page')
                else:
                    # print('repeat the procedure until the requirement is satisfied')
                    if attempt_to_refresh == 2:
                        refresh_error = 'Custom_refresh_error'
                        some_termination_condition = 1
                    else:
                        attempt_to_refresh = attempt_to_refresh + 1
                        # self.browser.back()
            #
            except TypeError:
                pass

        return page_soup_search_result, page_current_page, refresh_error

    def scrape_oatd(self, to_url):
        self.browser.get(to_url)
        page_soup_search_result = Soup(self.browser.page_source, 'html.parser')

        last_page = max(self.filter_by_type(self.get_available_page(page_soup_search_result), int))
        result_per_page = 30
        current_page_no_actua_str = page_soup_search_result.find('span', attrs={'class': 'this-page'}).text
        current_page_no_actual = int(''.join(filter(str.isalnum, current_page_no_actua_str)))

        some_termination_condition = []
        all_result_x = []

        while some_termination_condition != 1:
            try:
                # for document_index in range(1, result_per_page):
                # all_href_per_page = self.scrape_search_result_per_page(page_soup) # Working
                document_status_x = self.scrape_search_result_per_page(page_soup_search_result)
                all_result_x.append(document_status_x)

                # Click go to next page
                try:
                    if current_page_no_actual != last_page:
                        page_soup_search_result, current_page_no_actual, refresh_error = self.move_next_page(
                            page_soup_search_result)
                    else:

                        page_soup_page_verification = Soup(self.browser.page_source, 'html.parser')

                        page_current_page_verification_str = page_soup_search_result.find('span',
                                                                                          attrs={
                                                                                              'class': 'this-page'}).text
                        page_current_page_verification = int(
                            ''.join(filter(str.isalnum, page_current_page_verification_str)))

                        if page_current_page_verification == last_page:
                            some_termination_condition = 1
                            current_page_no_actual = page_current_page_verification
                            continue

                except IndexError:
                    continue
            except IndexError:
                some_termination_condition = 1

        return all_result_x

    def loop_get_specific(self, all_result):
        test_list = flatten(all_result[:])
        all_website_scrape = []
        base_add = 'https://oatd.org/oatd/'
        for url_to_pass in test_list:
            # what_this=
            url_to_pass_complete = base_add + url_to_pass
            page = requests.get(url_to_pass_complete)
            if page.status_code == 200:
                page_soup = Soup(page.text, 'html.parser')
                result_scrape = self.get_each_page(page_soup)
                result_scrape.update(href_to_oatd=url_to_pass_complete)
                all_website_scrape.append(result_scrape)
        return all_website_scrape


# new_dict = dict(test_xx='test', other_la='other la')
# new_dict.update(new_add='Geeks')
# x = 1
# url = 'https://oatd.org/oatd/search?q=eeg&form=basic'
url = 'https://oatd.org/oatd/search?q=eeg&form=basic&pubdate.facet=1991'  # 88 result , 3 pages
oatd = ScrapeOatd()
all_result = oatd.scrape_oatd(url)
print('complete scrape search result')
all_website_scrape = oatd.loop_get_specific(all_result)
print('complete scrape specific page')

x = 1

with open('oatd_complete_all_specific_page.pickle', 'wb') as handle:
    pickle.dump(all_website_scrape, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('complete saving')

# html_oatd_specific_page
# r = requests.get('https://oatd.org/oatd/record?record=handle\:11012\%2F16478&q=eeg')
# page_soup = Soup(r.text, 'html.parser')
