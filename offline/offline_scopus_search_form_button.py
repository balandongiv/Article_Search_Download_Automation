from bs4 import BeautifulSoup as soup


'''
 Note that, here, we only extract the result number 1. Meaning that, the document status
 only have the detail of
 Title: 	REM sleep in acutely traumatized individuals and interventions for
 Authors:  Repantis
 Year: 2020
'''
url = r'html_scopus_search_form_button.htm'
document_idx = 0
with open(url, 'r', encoding='utf-8') as f:
    page_soup = soup(f, 'html.parser')