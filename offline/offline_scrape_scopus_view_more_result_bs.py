
from bs4 import BeautifulSoup as soup
import re

'''
This function help to extract all references cited by the main paper

'''

url = r'html_scopus_search_result_from_view_more.html'


with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')
    document_abstract = page_soup.select('#pageTitleHeader > span')[0].text
    total_references = int(document_abstract.split('references', 1)[0])
    document_idx=1
    paper_href_scopus = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(2) > a')[0]['href']
    paper_title = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(2) > a')[0].text
    paper_year = page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(4) > span')[0].text
    paper_publisher_link_paper = page_soup.select(f'#resultLinkRow{document_idx:d} > td > ul > li:nth-child(2) > '
                                                  f'span.divTextLink > a')[0]['href']

    paper_author = []

    for author_idx in range(1, 2):  # limit to first three author to speed up
        try:
            paper_author.append(page_soup.select(f'#resultDataRow{document_idx:d} > td:nth-child(3) > span > '
                                                 f'a:nth-child({author_idx:d})')[0].text)
        except IndexError:
            break

    document_status = dict(paper_title=paper_title, paper_year=paper_year,
                           paper_author=paper_author, paper_publisher_link_paper=paper_publisher_link_paper,
                           paper_href_scopus=paper_href_scopus)







