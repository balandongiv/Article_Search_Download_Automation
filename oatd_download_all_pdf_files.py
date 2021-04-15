import os
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as Soup
import urllib.request as urllib2
import urllib.parse
import re
from urllib.parse import urlparse

# # Eberhard Karls Repo
# url = "https://publikationen.uni-tuebingen.de/xmlui/handle/10900/92067"
# html_plus = 'https://publikationen.uni-tuebingen.de'

# TUDelft Repo
'''
'https://repository.tudelft.nl/islandora/object/uuid:ace78c36-d0a3-40d7-bb50-505bce956042?collection=research'
<a 
    title="Thesis_Sjoerd_Huisman_compressed.pdf (28.39 MB)" 
    href="/islandora/object/uuid:ace78c36-d0a3-40d7-bb50-505bce956042/datastream/OBJ/download">
    <i class="icon-asset-download">
    </i><span class="asset-title">PDF</span>
</a>

Very special case where the href does not contain any indicator about .pdf. So, we need to rely on the attr
title.
'''
url_one = 'https://repository.tudelft.nl/islandora/object/uuid:ace78c36-d0a3-40d7-bb50-505bce956042?collection=research'
html_plus = 'https://repository.tudelft.nl'

# HELDA
'''
<td>
    <a href="/bitstream/handle/10138/165912/gradu.pdf?sequence=2&amp;isAllowed=y" 
    title="gradu.pdf">gradu.pdf</a>
</td>

Special case where .pdf exist both in href and title attribute under the a tag
'''
url_two = 'https://helda.helsinki.fi/handle/10138/165912'
html_plus = 'https://helda.helsinki.fi'

# Universitiy of Bradford
'''
https://bradscholars.brad.ac.uk/handle/10454/5521
<div>
    <div>final full thesis ashardi abas.pdf (3.938Mb)</div>
    <a class="btn btn-default btn-block file-download-button" 
    href="/bitstream/handle/10454/5521/final%20full%20thesis%20ashardi%20abas.pdf?sequence=3&amp;isAllowed=y">Download</a>
</div>

Typical case where .pdf exist only href attr
'''
url_three = 'https://bradscholars.brad.ac.uk/handle/10454/5521'
html_plus = 'https://bradscholars.brad.ac.uk'

# University Digital Conservancy Home
'''
'https://conservancy.umn.edu/handle/11299/93138'

<div>
<a href="/bitstream/handle/11299/93138/Gu_Ye_June2010.pdf?sequence=1&amp;isAllowed=y">
    <i aria-hidden="true" class="glyphicon  glyphicon-file"></i> Gu_Ye_June2010.pdf (528.5Kb application/pdf)
</a>
</div>

Good case where .pdf exist both in href and text attribute under the a tag
'''
url_four = 'https://conservancy.umn.edu/handle/11299/93138'
html_plus = 'https://conservancy.umn.edu'

all_url_interest = [{"href": url_one, "paper_name": 'paper one'}, \
                    {"href": url_two, "paper_name": 'paper two'}, \
                    {"href": url_three, "paper_name": 'paper three'}, \
                    {"href": url_four, "paper_name": 'paper four'}]

# all_url_interest = [url_four]
# #If there is no such folder, the script will create one automatically
folder_location = r'C:download_file'
if not os.path.exists(folder_location): os.mkdir(folder_location)

filename = os.path.join(folder_location, 'tst')
x = 1


# page_soup = Soup(self.browser.page_source, 'html.parser')

def find_href(page_soup):
    list_of_url = []
    for pdf_text_within_href in page_soup.find_all("a"):
        # If .pdf is mentioned somewhere along the link. text and href is present, then assume
        # it can be used to download the pdf file
        try:
            if '.pdf' in pdf_text_within_href['href']:
                list_of_url.append(pdf_text_within_href['href'])
        except KeyError:
            continue

        try:
            if 'pdf' in pdf_text_within_href.text:
                list_of_url.append(pdf_text_within_href.text)
        except KeyError:
            continue

        # In some website, the  mentioned the .pdf file name in the attribute 'title'
        # instead along the a tag.
        try:
            if '.pdf' in pdf_text_within_href['title']:
                list_of_url.append(pdf_text_within_href['href'])
        except KeyError:
            continue

    return list_of_url


def download_all_pdf(url_unique, base_file_name):
    response = requests.get(url_unique)
    page_soup = Soup(response.text, "html.parser")
    list_of_url_x = find_href(page_soup)
    list_of_url = list(set(list_of_url_x))
    raw_lst = ['/', '?']
    new_htpp = []

    result = '{uri.scheme}://{uri.netloc}/'.format(uri=urllib.parse.urlsplit(url_unique))

    for mystring in list_of_url:
        if set(raw_lst) & set(mystring):
            # complete_https = result + mystring
            # print(complete_https)
            new_htpp.append(result + mystring)
    number_iti = 0
    for url_to_download_pdf in new_htpp:

        response = requests.get(url_to_download_pdf)
        if response.status_code == 200:
            if number_iti != 0:
                new_name = base_file_name + str(number_iti)

            else:
                new_name = base_file_name

            filename_comb = os.path.join(folder_location, f'{new_name}.pdf')
            number_iti = number_iti + 1

            with open(filename_comb, 'wb') as f:
                f.write(response.content)


number = 1
for my_url in all_url_interest:
    the_url = my_url.get('href')
    file_name_usedx = my_url.get('paper_name')
    print(number, ':', the_url)
    download_all_pdf(the_url, file_name_usedx)
    number = number + 1
