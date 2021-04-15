from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException,StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as soup
import re
from selenium.webdriver.support.ui import Select
from lxml import etree
import re
import time

'''
To try at cisir PC
today friday
successfully tested on 02 July 2020
'''


class scrape_freepick_cl:
    def __init__(self):
        print("Start the setup")
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
    def scrapt_each_attribute(number_of_display, g_data):
        data_id = g_data[number_of_display].find("a", {"class": "showcase__link"})['data-id']  # works
        data_href_link = g_data[number_of_display].find("a", {"class": "showcase__link"})['href']  # works

        image_url_long = g_data[number_of_display].find("a", {"class": "showcase__link"}).img['data-src']  # works
        image_url = re.split(r"size", image_url_long)[0][:-1]

        image_title = g_data[number_of_display].find("a", {"class": "showcase__link"}).img['alt']  # works

        return dict(data_id=data_id, image_title=image_title,
                    image_url=image_url, data_href_link=data_href_link)

    def tab_number_kill(self):
        ## https://stackoverflow.com/a/54241574/6446053
        print("Check for number of tabs exist in Browser")
        print('Number of tab on Chrome Browser', len(self.browser.window_handles))
        self.browser.switch_to.window(self.browser.window_handles[1])
        self.browser.close()
        self.browser.switch_to.window(self.browser.window_handles[0])
        print('Number of tab on Chrome Browser', len(self.browser.window_handles))

    def scrape_scopus(self, url):
        all_result = []
        self.browser.get(url)
        html = self.browser.page_source
        page_soup = soup(html, 'html.parser')

        # dom = etree.HTML(str(page_soup))
        pagination_string = page_soup.find('span', {'class': 'pagination__pages'}).text
        # number_of_pages = int(re.findall('\d+', pagination_string)[0])

        number_of_pages=int(pagination_string.replace(',', ''))
        g_data = page_soup.find_all("figure", {"class": "showcase__item"})
        size_total_display = len(g_data)

        some_termination_condition = []
        print('start scraping the browser')
        current_page_no = 1

        while some_termination_condition != 1:
            try:
                for number_of_display in range(0, size_total_display):
                    try:
                        report_status = self.scrapt_each_attribute(number_of_display, g_data)
                        all_result.append(report_status)
                    except IndexError:
                        continue

                try:
                    try:
                        WebDriverWait(self.browser, 20).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, "a.pagination__next"))).click()
                    except StaleElementReferenceException:
                        time.sleep(4)  # Delay for 5 seconds.
                        WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "a.pagination__next"))).click()

                    if len(self.browser.window_handles) > 1:
                        self.tab_number_kill()

                    html = self.browser.page_source
                    page_soup_search_result = soup(html, 'html.parser')
                    g_data = page_soup_search_result.find_all("figure", {"class": "showcase__item"})


                except (NoSuchElementException, TimeoutException) as e:
                    if current_page_no == number_of_pages:
                        some_termination_condition = 1
                        continue

            except IndexError:
                some_termination_condition = 1

            if current_page_no % 5 == 0:
                print(f"complete page {current_page_no:d} out of {number_of_pages:d}")

            current_page_no = current_page_no + 1

        return all_result


to_url = 'https://www.freepik.com/search?dates=any&format=search&page=1&query=medical&sort=popular'
ssc = scrape_freepick_cl()
ssc.scrape_scopus(to_url)
# all_result_xx,document_reports = ssc.scrape_scopus(to_url)
x = 1
