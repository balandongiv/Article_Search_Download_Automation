
from bs4 import BeautifulSoup as soup
import re

'''
This function help to extract specific scopus paper

'''

url = r'html_scopus_paper_specific_page_rpb.html'

with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')

    document_cited_by_paper = page_soup.find('a', attrs={'title': 'View all citing documents'})['href']
    results_doc_journal = page_soup.find_all("a", {"title": "Go to the information page for this source"})
    for result in results_doc_journal:
        document_journal = result.find('span', attrs={'class': 'anchorText'}).text  # result not results


    author_names=[]
    page_soup_section=page_soup.find("section", {"id": "authorlist"}).find_all("span", {"class": "anchorText"})
    for author_lt in page_soup_section:
        # after_split=author_lt.text.split('.')[0]
        author_names.append(author_lt.text.split('.')[0])
    x=1
    document_abstract = page_soup.select('#abstractSection > p')[0].text
    document_doi=page_soup.select('#recordDOI')[0].text
    document_publisher = re.split(r"Publisher:", page_soup.select('#documentInfo > li:nth-child(4)')[0].text)[1]
    document_type = re.split(r"Document Type:", page_soup.select('#documentInfo > li:nth-child(3)')[0].text)[1]
    document_volume_issue_year = page_soup.select('#articleTitleInfo > span.list-group-item')[1].text
    split_str = document_volume_issue_year.split(',')
    document_volume=split_str[0].split('Volume')[1]
    document_issue = split_str[1].split('Issue')[1]
    document_year = split_str[2]
    document_number = split_str[3].split('Article number')[1]




