
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup as Soup
import getpass
from my_tool import flatten_dict, filter_by_type


class ScrapeOatd:
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()

        # Load current user default profile
        current_user = getpass.getuser()
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

        paper_author = get_att({"itemprop": "author"})

        paper_title = get_att({"itemprop": "name"})

        paper_url = get_att({"itemprop": "url"})

        paper_publisher = get_att({"itemprop": "publisher"})

        paper_abstract = get_att({"itemprop": "description"})

        paper_about = get_att({"itemprop": "about"})

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
                else:
                    if attempt_to_refresh == 2:
                        refresh_error = 'Custom_refresh_error'
                        some_termination_condition = 1
                    else:
                        attempt_to_refresh = attempt_to_refresh + 1
            except TypeError:
                pass

        return page_soup_search_result, page_current_page, refresh_error

    def scrape_oatd(self, to_url):
        self.browser.get(to_url)
        page_soup_search_result = Soup(self.browser.page_source, 'html.parser')

        last_page = max(filter_by_type(self.get_available_page(page_soup_search_result), int))
        current_page_no_actua_str = page_soup_search_result.find('span', attrs={'class': 'this-page'}).text
        current_page_no_actual = int(''.join(filter(str.isalnum, current_page_no_actua_str)))

        some_termination_condition = []
        all_result_x = []

        while some_termination_condition != 1:
            try:
                document_status_x = self.scrape_search_result_per_page(page_soup_search_result)
                all_result_x.append(document_status_x)

                # Click go to next page
                try:
                    if current_page_no_actual != last_page:
                        page_soup_search_result, current_page_no_actual, refresh_error = self.move_next_page(
                            page_soup_search_result)
                    else:

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
        test_list = flatten_dict(all_result[:])
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
