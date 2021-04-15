from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementClickInterceptedException, \
    InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from bs4 import BeautifulSoup as Soup
import re
from my_tool import filter_by_type, flatten_dict, merge_dict
import getpass
# from itertools import zip_longest

class ScrapeScopus:

    def __init__(self, time_wait=None):

        self.time_wait = 20 if time_wait is None else time_wait
        chrome_options = webdriver.ChromeOptions()
        current_user = getpass.getuser()
        # current_user = 'rpb'
        chrome_options.add_argument(
            r"--user-data-dir=C:\Users\{}\AppData\Local\Google\Chrome\User Data".format(current_user))
        # chrome_options.add_argument("--headless")
        # chrome_options.add_argument("--window-size=1920x1080")
        self.browser = webdriver.Chrome(
            executable_path=r"C:Browsers\chromedriver.exe",
            options=chrome_options)

        ##########################################
        self.main_url = 'https://www.scopus.com'
        self.search_term = []
        self.xpath = []

        self.paper_reference = False
        self.related_document = False
        self.cited_document = False

        self.menu = {'all_field': {'title': 'All field', 'xpath': '//*[@id="ui-id-2"]'},
                     'abstract': {'title': 'Article title, Abstract, Keywords', 'xpath': '//*[@id="documents-tab-panel"]/div/micro-ui/scopus-document-search-form/form/div[1]/div/div[1]/els-select/div/label/select/option[2]'},
                     'title': {'title': 'Article title', 'xpath': '//*[@id="ui-id-7"]'},
                     'doi': {'title': 'DOI', 'xpath': '//*[@id="ui-id-21"]'},
                     'title_abs_kew_auth': {'title': 'Article title, Abstract, Keywords, Authors',
                                            'xpath': '//*[@id="ui-id-24"]'},
                     'authors': {'title': 'Authors', 'xpath': '//*[@id="ui-id-4"]'},
                     'first_author': {'title': 'First author', 'xpath': '//*[@id="ui-id-5"]'}}

        self.url_list = {'base_url': 'https://www.scopus.com/search/form.uri?display=basic',
                         'other_url': 'test'}

    def get_title_theme(self, text_to_find_c):
        text_to_find = text_to_find_c.lower()
        res = len(text_to_find.split())

        for k, v in self.menu.items():
            title_theme = v['title'].lower()
            if title_theme in text_to_find:
                if res == 1:
                    xpath_title = v['xpath']
                    break
                elif res > 1 and title_theme.startswith(text_to_find.split()[0]) \
                        and title_theme.endswith(text_to_find.split()[-1]):
                    xpath_title = v['xpath']
                    break

        return xpath_title

    @staticmethod
    def get_available_page(page_soup_search_result):
        list_page_visible = []
        for div_tag in page_soup_search_result.find_all('div', {'class': 'col-md-6 center-block text-center'}):
            for litag in div_tag.find_all('li'):
                str_litag = litag.text
                try:
                    list_page_visible.append(int(str_litag))
                except ValueError:
                    list_page_visible.append('NA')
        return list_page_visible

    def key_search_term(self):

        try:
            ## Clear the search area
            WebDriverWait(self.browser, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="txtBoxSearch"]/button'))).click()
        except (NoSuchElementException, TimeoutException) as e:
            pass

        WebDriverWait(self.browser, self.time_wait).until(
            EC.element_to_be_clickable((By.XPATH, self.xpath['arrow_down_search']['xpath']))).click()
        WebDriverWait(self.browser, self.time_wait).until(
            EC.element_to_be_clickable((By.XPATH, self.xpath['search_type_choice']['xpath']))).click()

        inputElement = self.browser.find_element_by_xpath(self.xpath['search_term']['xpath'])
        inputElement.send_keys(self.search_term)
        inputElement.send_keys(Keys.ENTER)

    def pagination(self):

        WebDriverWait(self.browser, self.time_wait).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="resultsPerPage-button"]/span[1]'))).click()
        WebDriverWait(self.browser, self.time_wait).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="ui-id-4"]'))).click()

    def move_next_page(self, page_soup_search_result):

        page_current_page_old = int(page_soup_search_result.find(attrs={"name": "currentPage"})['value'])
        list_page_visible = self.get_available_page(page_soup_search_result)
        shift_no_page = 3

        page_current_page_new = page_current_page_old + 1
        index_location = list_page_visible.index(page_current_page_new)
        current_page_no = shift_no_page + index_location
        some_termination_condition = []
        attempt_to_refresh = 0
        refresh_error = []
        while some_termination_condition != 1:
            try:
                WebDriverWait(self.browser, 8).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, f'#resultsFooter > '
                                                                       f'div.col-md-6.center-block.text-center > '
                                                                       f'ul > li:nth-child({current_page_no:d}) > '
                                                                       f'a '))).click()
                self.click_abstract()
                page_soup_search_result = Soup(self.browser.page_source, 'html.parser')

                # Check current page if similar to our intended page
                try:
                    page_current_page = int(page_soup_search_result.find(attrs={"name": "currentPage"})['value'])

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
                            self.browser.back()

                except TypeError:
                    if attempt_to_refresh == 2:
                        refresh_error = 'Custom_refresh_error'
                        some_termination_condition = 1
                        page_current_page = 1000000
                    else:
                        attempt_to_refresh = attempt_to_refresh + 1
                        self.browser.back()

            except (
                    NoSuchElementException, TimeoutException, IndexError, ElementClickInterceptedException,
                    TypeError) as e:
                # continue
                if attempt_to_refresh == 2:
                    refresh_error = 'Custom_refresh_error'
                    page_current_page = 1000000
                    continue
                else:
                    attempt_to_refresh = attempt_to_refresh + 1
                    self.browser.back()

                    refresh_error = 'Custom_refresh_error'
                    page_current_page = 1000000

        return page_soup_search_result, page_current_page, refresh_error

    @staticmethod
    def extract_default_info(page_soup):
        '''
        Used to extract from the individual page
        '''

        try:
            results_doc_journal = page_soup.find_all("a", {"title": "Go to the information page for this source"})
            if not results_doc_journal:
                try:
                    document_journal = page_soup.find("span", {"id": "noSourceTitleLink"}).text
                except:
                    document_journal = 'NOT AVAILABLE'
            else:
                for result in results_doc_journal:
                    document_journal = result.find('span', attrs={'class': 'anchorText'}).text  # result not results
        except (NoSuchElementException, IndexError, UnboundLocalError) as e:
            document_journal = 'NOT AVAILABLE'

        try:
            document_abstract = page_soup.select('#abstractSection > p')[0].text
        except (NoSuchElementException, IndexError) as e:
            document_abstract = 'NOT AVAILABLE'

        try:
            document_doi = page_soup.select('#recordDOI')[0].text
        except (NoSuchElementException, IndexError) as e:
            document_doi = 'NOT AVAILABLE'

        try:
            document_publisher = re.split(r"Publisher:", page_soup.select('#documentInfo > li:nth-child(4)')[0].text)[1]
        except (NoSuchElementException, IndexError) as e:
            document_publisher = 'NOT AVAILABLE'

        try:
            document_type = re.split(r"Document Type:", page_soup.select('#documentInfo > li:nth-child(3)')[0].text)[1]
        except (NoSuchElementException, IndexError) as e:
            document_type = 'NOT AVAILABLE'

        try:
            document_volume_issue_year = page_soup.select('#articleTitleInfo > span.list-group-item')[1].text
        except (NoSuchElementException, IndexError) as e:
            document_volume_issue_year = 'NOT AVAILABLE'

        if document_volume_issue_year.find('Volume') != -1:
            document_volume = document_volume_issue_year.split('Volume')[1].split(',')[0]
        else:
            document_volume = 'NA'

        if document_volume_issue_year.find('Issue') != -1:
            document_issue = document_volume_issue_year.split('Issue')[1].split(',')[0]
        else:
            document_issue = 'NA'

        if document_volume_issue_year.find('Pages') != -1:
            document_number = document_volume_issue_year.split('Pages')[1].split(',')[0]
        else:
            document_number = 'NA'

        try:
            document_year = document_volume_issue_year.split('Issue')[1].split(',')[1]
        except (NoSuchElementException, IndexError) as e:
            split_str = document_volume_issue_year.split(',')
            try:
                document_year = split_str[2]
            except (NoSuchElementException, IndexError) as e:
                document_year = 'NOT AVAILABLE'

        try:
            author_names = []
            page_soup_section = page_soup.find("section", {"id": "authorlist"}).find_all("span",
                                                                                         {"class": "anchorText"})
            for author_lt in page_soup_section:
                author_names.append(author_lt.text.split('.')[0])
        except (NoSuchElementException, AttributeError) as e:
            author_names = 'NOT AVAILABLE'

        document_report = dict(document_abstract=document_abstract, document_doi=document_doi,
                               document_publisher=document_publisher, document_type=document_type,
                               document_volume=document_volume, document_issue=document_issue,
                               document_year=document_year, document_number=document_number, author_names=author_names,
                               document_journal=document_journal)

        return document_report

    def hopefully_fast(self, page_soup):

        def loop_tr_tag(div_tag):
            '''
            List comprehension such as will result in empty data in some instance, bcos of that, we have to use
            normal nested loop presentation
            paper_doi = [litagx.get('data-doi') for litag in div_tag.find_all('th', {'scope': 'row'})
                                     for litagx in litag.find_all('div', {'class': 'checkbox'})]

            paper_author = [all_td_X.text for all_td_X in all_td.find_all('span')]
            '''

            paper_doi = [litagx.get('data-doi') for litag in div_tag.find_all('th', {'scope': 'row'})
                         for litagx in litag.find_all('div', {'class': 'checkbox'})]

            data_resultnum = int(div_tag.get('data-resultnum'))
            paper_author = [];
            paper_href_scopus = [];
            paper_title = [];
            paper_year = [];
            paper_publisher_link_paper = []

            for all_td in div_tag.find_all('td'):
                [paper_author.append(all_td_X.text) for all_td_X in all_td.find_all('span')]

                [(paper_href_scopus.append(litag['href']), paper_title.append(litag.text)) for litag in
                 all_td.find_all('a', {'class': 'ddmDocTitle'})]

                [paper_year.append(litag.text) for litag in all_td.find_all('span', {'class': 'ddmPubYr'})]

                [paper_publisher_link_paper.append(self.main_url + litag['href']) for litag
                 in all_td.find_all('a', {'class': 'ddmDocSource'})]

            return dict(paper_title='NA' if not paper_title else paper_title[0],
                        paper_year='NA' if not paper_year else paper_year[0],
                        paper_author='NA' if not paper_author else paper_author[0],
                        paper_publisher_link_paper='NA' if not paper_publisher_link_paper else
                        paper_publisher_link_paper[0],
                        paper_href_scopus='NA' if not paper_href_scopus else paper_href_scopus[0],
                        data_resultnum=data_resultnum,
                        document_doi='empty block' if not paper_doi else paper_doi[0])

        all_report = [loop_tr_tag(div_tag) for div_tag in page_soup.find_all('tr', {'class': 'searchArea'})]

        return all_report

    @staticmethod
    def get_abstract_ver(page_soup):
        # abstrct_report = []

        def append_info(div_tagx):
            paper_idx = [int(re.search(r'\d+', div_tagx.get('id')).group())]
            document_abstract = [txt.text for txt in div_tagx.find_all('span', {'class': 'txt'})]
            paper_idx = 'empty block' if not paper_idx else paper_idx[0]
            document_abstract = 'empty block' if not document_abstract else document_abstract[0]

            return dict(paper_idx=paper_idx, abstract=document_abstract)

        abstrct_report = [append_info(div_tag) for div_tag in
                          page_soup.find_all('tr', {'class': 'panel-collapse collapse displayNone'})]

        return abstrct_report

    def click_abstract(self):
        termination_cond = [];
        idx = 1
        while termination_cond != 1:
            try:
                WebDriverWait(self.browser, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, f'//*[@id="previewAbstractLinkText{idx}"]/a/span[2]'))).click()
                WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, f'#previewAbstract{idx} > span'))).get_attribute('href')

                termination_cond = 1
            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                idx = idx + 1

            if idx > 201:
                raise Exception("I cannot find no abstract after 200 tries")

    def scrape_scopus_multi_search(self):
        self.pagination()
        self.click_abstract()
        page_soup_search_result = Soup(self.browser.page_source, 'html.parser')  # To parse the search result
        last_page = max(filter_by_type(self.get_available_page(page_soup_search_result), int))
        current_page_no_actual = int(page_soup_search_result.find(attrs={"name": "currentPage"})['value'])

        all_result_x = []
        some_termination_condition = []

        while some_termination_condition != 1:
            all_reportv = self.hopefully_fast(page_soup_search_result)
            abstrct_reportx = self.get_abstract_ver(page_soup_search_result)

            if len(abstrct_reportx) == len(all_reportv):
                all_result_x.append(merge_dict(all_reportv, abstrct_reportx))
            else:
                raise Exception("Sorry, length not the same")

            try:
                if current_page_no_actual != last_page:
                    page_soup_search_result, current_page_no_actual, refresh_error = self.move_next_page(
                        page_soup_search_result)
                    if refresh_error == 'Custom_refresh_error':
                        some_termination_condition = 1
                else:
                    break

            except (NoSuchElementException, TimeoutException, ElementClickInterceptedException) as e:
                page_soup_page_verification = Soup(self.browser.page_source, 'html.parser')
                page_current_page_verification = int(
                    page_soup_page_verification.find(attrs={"name": "currentPage"})['value'])

                if page_current_page_verification == last_page:
                    some_termination_condition = 1
                    continue

        return all_result_x

    def get_article_ref(self):
        href_article_references = []
        try:
            href_article_references = WebDriverWait(self.browser, self.time_wait).until(
                EC.visibility_of_element_located(
                    (By.CSS_SELECTOR, '#referenceSrhResults'))).get_attribute('href')
        except (NoSuchElementException, TimeoutException, IndexError) as e:
            return href_article_references

        return href_article_references

    def get_article_related_doc(self):
        href_related_papers = []
        try:
            href_related_papers = WebDriverWait(self.browser, self.time_wait).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, 'div.recordPageBoxes:nth-child(2) > a:nth-child(1)'))).get_attribute('href')
        except (NoSuchElementException, TimeoutException, IndexError) as e:
            return href_related_papers

        return href_related_papers

    def get_cited_by_doc(self):
        href_cited_by_papers = []
        try:
            href_cited_by_papers = WebDriverWait(self.browser, self.time_wait).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR,
                 '#recordPageBoxes > div > div.displayBlock.paddingBottom1 > div.recordPageBoxes.docViewAll >         '
                 '                                     a'))).get_attribute('href')
        except (NoSuchElementException, TimeoutException, IndexError) as e:
            return href_cited_by_papers

        return href_cited_by_papers

    def get_secondary_info(self):

        href_article_references = self.get_article_ref() if self.paper_reference is True else []
        href_related_papers = self.get_article_related_doc() if self.related_document is True else []
        href_cited_by_doc = self.get_cited_by_doc() if self.cited_document is True else []

        article_references = None;
        related_papers = None;
        cited_by_doc = None

        if href_article_references:
            self.browser.get(href_article_references)
            article_references = self.scrape_scopus_multi_search()

        if href_related_papers:
            self.browser.get(href_related_papers)
            related_papers = self.scrape_scopus_multi_search()

        if href_cited_by_doc:
            self.browser.get(href_cited_by_doc)
            cited_by_doc = self.scrape_scopus_multi_search()

        return dict(article_references='NA' if article_references is None else article_references[0],
                    related_papers='NA' if related_papers is None else related_papers[0],
                    cited_by_doc='NA' if cited_by_doc is None else cited_by_doc[0])

    def scrape_scopus_article(self, to_url, paper_reference=None, related_document=None, cited_document=None):

        self.paper_reference = False if paper_reference is None else paper_reference
        self.related_document = False if related_document is None else related_document
        self.cited_document = False if cited_document is None else cited_document
        try:
            self.browser.get(to_url)
            WebDriverWait(self.browser, self.time_wait).until(EC.visibility_of_element_located(
                (By.CSS_SELECTOR, '#gh-branding'))).get_attribute('href')  # Just to make sure page load properly

            page_soup = Soup(self.browser.page_source, 'html.parser')
            document_reports = self.extract_default_info(page_soup)

            if self.paper_reference is not None or \
                    self.related_document is not None or \
                    self.cited_document is not None:
                all_result_x = self.get_secondary_info()

        except InvalidArgumentException:
            all_result_x = []
            document_reports = []

        return all_result_x, document_reports

    def scrape_via_search_term(self, keyword=None, search_term=None):

        if search_term is None:
            raise Exception("No search term provided")
        else:
            self.search_term = search_term

        text_to_find_c = keyword if keyword is not None else 'Article title, Abstract, Keywords'

        self.xpath = {'search_term': {'xpath': '//els-input/div/label/input"]',
                                      'help': 'Input text Label: Document Search'},
                      'search_type_choice': {'xpath': self.get_title_theme(text_to_find_c),
                                             'help': 'search_type_choice index location: Document Search ',
                                             'text_key_search': text_to_find_c.lower()},
                      'arrow_down_search': {'xpath': '//*[@id="documents-tab-panel"]/div/micro-ui/scopus-document-search-form/form/div[1]/div/div[1]/els-select/div',
                                            'help': 'Arrow down for the search_type_choice index location: Document '
                                                    'Search '}}

        url = self.url_list['base_url']
        self.browser.get(url)
        self.key_search_term()
        return flatten_dict(self.scrape_scopus_multi_search()[:])

    def login_landing_page(self):

        login_url = 'https://www.scopus.com/signin.uri?origin=NO%20ORIGIN%20DEFINED&zone=TopNavBar'
        base_url = 'https://www.scopus.com/home.uri'
        self.browser.get(base_url)
        self.browser.get(login_url)
        # current_url=self.browser.current_url()
        login_detail = []

        login_detail_email = 'balandongiv@gmail.com'
        login_detail_passwod = '8487936iV@'

        user_id = WebDriverWait(self.browser, self.time_wait).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#bdd-email')))
        user_id.send_keys(login_detail_email)

        button_element = WebDriverWait(self.browser, self.time_wait).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#bdd-elsPrimaryBtn')))
        button_element.click()

        user_pw = WebDriverWait(self.browser, self.time_wait).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#bdd-password')))
        user_pw.send_keys(login_detail_passwod)

        button_element = WebDriverWait(self.browser, self.time_wait).until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#bdd-elsPrimaryBtn')))
        button_element.click()
