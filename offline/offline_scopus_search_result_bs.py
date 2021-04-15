from bs4 import BeautifulSoup as soup
import re
from itertools import zip_longest
'''
 Note that, here, we only extract the result number 1. Meaning that, the document status
 only have the detail of
 Title: 	REM sleep in acutely traumatized individuals and interventions for
 Authors:  Repantis
 Year: 2020
'''
# url = r'html_scopus_search_result.html'
url = r'html_scopus_search_result_with_abstract.html'
# Ideal case,
# first_list = [{'val': 1, 'item': 'item1'}, {'val': 2, 'item': 'item2'}, {'val': 3, 'item': 'item3'}]
# sec_list = [{'idx': 1, 'other': '1'}, {'idx': 2, 'other': '2'}, {'idx': 3, 'other': '3'}]
# expect_output = [{'val': 1,'item': 'item1', 'idx': 1, 'other': '1'}, \
#                  {'val': 2,'item': 'item2', 'idx': 2, 'other': '2'}, \
#                  {'val': 3,'item': 'item3', 'idx': 3, 'other': '3'}]
#
# new_result=[]
# for first_list_x,sec_list_x in zip(first_list,sec_list):
#     new_result.append({**first_list_x, **sec_list_x})
#
# expect_output = [{'val': 1,'item': 'item1', 'idx': 1, 'other': '1'}, \
#                  {'val': 2,'item': 'item2', 'idx': 2, 'other': '2'}, \
#                  {'val': 3,'item': 'item3'}]
# # Extreme case,
# first_list = [{'val': 1, 'item': 'item1'}, {'val': 2, 'item': 'item2'}, {'val': 3, 'item': 'item3'}]
# sec_list = [{'idx': 1, 'other': '1'}, {'idx': 2, 'other': '2'}]
#
# new_result=[]
# for first_list_x,sec_list_x in zip(first_list,sec_list):
#     new_result.append({**first_list_x, **sec_list_x})
# x = 1


def approach_slow(page_soup):
    paper_href_scopus = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(2) > a')[0]['href']
    paper_title = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(2) > a')[0].text
    paper_year = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(4) > span')[0].text
    paper_publisher_link_paper = page_soup.select(f'#resultLinkRow{document_idx:d} > td > ul > li:nth-child(2) > '
                                                  f'span.divTextLink > a')[0]['href']
    paper_author = []
    author_idx = 1
    response = None
    while response != 1:
        try:
            paper_author.append(page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(3) > span > '
                                                 f'a:nth-child({author_idx:d})')[0].text)
            author_idx = author_idx + 1
        except IndexError:
            response = 1

    document_status = dict(paper_title=paper_title, paper_year=paper_year,
                           paper_author=paper_author, paper_publisher_link_paper=paper_publisher_link_paper,
                           paper_href_scopus=paper_href_scopus)


def hopefully_fast(page_soup):
    def loop_tr_tag(div_tag):
        paper_doi=[]
        for litag in div_tag.find_all('th', {'scope': 'row'}):
            for litagx in litag.find_all('div', {'class': 'checkbox'}):
                cc=litagx.get('data-doi')
                paper_doi.append(cc)
        paper_author = []
        paper_href_scopus = []
        paper_title = []
        paper_year = []
        paper_publisher_link_paper = []
        data_resultnum = int(div_tag.get('data-resultnum'))
        for all_td in div_tag.find_all('td'):
            for all_td_X in all_td.find_all('span'):
                paper_author.append(all_td_X.text)

            for litag in all_td.find_all('a', {'class': 'ddmDocTitle'}):
                paper_href_scopus.append(litag['href'])
                paper_title.append(litag.text)
            for litag in all_td.find_all('span', {'class': 'ddmPubYr'}):
                # for litagx in litag.find_all('span', {'class': 'ddmPubYr'}):
                paper_year.append(litag.text)

            for litag in all_td.find_all('a', {'class': 'ddmDocSource'}):
                paper_publisher_link_paper.append(litag['href'])

        # paper_authorx = paper_author[0] if paper_author != [] else 'empty block'
        # paper_href_scopusx = paper_href_scopus[0] if paper_href_scopus != [] else 'empty block'
        # paper_titlex = paper_title[0] if paper_title != [] else 'empty block'
        # paper_yearx = paper_year[0] if paper_year != [] else 'empty block'
        # paper_publisher_link_paperx = paper_publisher_link_paper[0] if paper_publisher_link_paper != [] else 'empty block'

        paper_authorx = 'empty block' if not paper_author else paper_author[0]
        paper_href_scopusx = 'empty block' if not paper_href_scopus else paper_href_scopus[0]
        paper_titlex = 'empty block' if not paper_title else paper_title[0]
        paper_yearx = 'empty block' if not paper_year else paper_year[0]
        paper_publisher_link_paperx = 'empty block' if not paper_publisher_link_paper else paper_publisher_link_paper[0]
        paper_doix = 'empty block' if not paper_doi else paper_doi[0]
        document_status = dict(paper_title=paper_titlex, paper_year=paper_yearx, paper_author=paper_authorx, \
                               paper_publisher_link_paper=paper_publisher_link_paperx,
                               paper_href_scopus=paper_href_scopusx,data_resultnum=data_resultnum,paper_doi=paper_doix)
        #
        return document_status

    all_report = []
    for div_tag in page_soup.find_all('tr', {'class': 'searchArea'}):
        new_doc = loop_tr_tag(div_tag)
        all_report.append(new_doc)

    return all_report


def get_abstract(page_soup):
    abstrct_report = []

    def append_info(div_tagx):
        paper_idx = []
        abstract = []
        string1 = div_tagx.get('id')
        paper_idx.append(int(re.search(r'\d+', string1).group()))

        for txt in div_tagx.find_all('span', {'class': 'txt'}):
            abstract.append(txt.text)

        paper_idx = 'empty block' if not paper_idx else paper_idx[0]
        abstract = 'empty block' if not abstract else abstract[0]

        # document_status = dict(paper_idx=paper_idx, abstract=abstract)
        return dict(paper_idx=paper_idx, abstract=abstract)

    for div_tag in page_soup.find_all('tr', {'class': 'panel-collapse collapse displayNone'}):
        new_doc = append_info(div_tag)
        abstrct_report.append(new_doc)

    return abstrct_report


with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')
    # approach_slow(page_soup)  # so slow oo ni cara
    all_reportv = hopefully_fast(page_soup)
    abstrct_reportx = get_abstract(page_soup)

    # combined_report = []
    # for first_list_x, sec_list_x in zip(all_reportv, abstrct_reportx):
    #     combined_report.append({**first_list_x, **sec_list_x})
    combined_report=[dict(**d1, **d2) for d1, d2 in zip_longest(all_reportv, abstrct_reportx, fillvalue={})]
    x = 1
