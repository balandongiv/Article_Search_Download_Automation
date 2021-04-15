import imaplib
import email
from email.header import decode_header
import webbrowser
import os
import re
from bs4 import BeautifulSoup as soup
import re
from scrapy.selector import Selector
import pickle

x = 1

outer_scopus_ref = []
all_result = []
username = "balandongiv@gmail.com"
password = "2526469?????"

# create an IMAP4 class with SSL
imap = imaplib.IMAP4_SSL("imap.gmail.com")
# authenticate
imap.login(username, password)
status, messages = imap.select("ScopusWOS")
# number of top emails to fetch
# N = 500
N = 2
# total number of emails
messages = int(messages[0])
# N = messages
index_for_loop = 1


# def extract_data(paper_index_x, all_result_x, paper_keyword):
#     paper_href = Selector(text=body).xpath(
#         f'//html/body/table[1]/tbody/tr[{paper_index_x:d}]/td[2]/a/@href').get()
#
#     if paper_href is not None:
#         paper_title = Selector(text=body).xpath(
#             f'//html/body/table[1]/tbody/tr[{paper_index_x:d}]/td[2]/a/text()').get()
#         paper_author = Selector(text=body).xpath(
#             f'//html/body/table[1]/tbody/tr[{paper_index_x:d}]/td[3]/text()').get()
#         paper_year = Selector(text=body).xpath(
#             f'//html/body/table[1]/tbody/tr[{paper_index_x:d}]/td[4]/text()').get()
#
#         report_status = dict(paper_title=paper_title, paper_author=paper_author,
#                              paper_year=paper_year, paper_href=paper_href,
#                              paper_keyword=paper_keyword)
#         all_result_x.append(report_status)
#     return all_result_x


# def outer_if(all_result_y, body_y):
#     # if it's HTML, create a new HTML file and open it in browser
#     long_string = Selector(text=body_y).xpath('//html/body/p').get()
#     number_of_paper = int(re.findall('\d+', re.split(r"has found", long_string)[1:][0])[0])
#     try:
#         paper_keyword = re.search('"(.+?)"', long_string).group(1)
#     except AttributeError:
#         paper_keyword = ''  # apply your error handling
#
#     for paper_index in range(1, number_of_paper + 1):
#         all_result_y = extract_data(paper_index, all_result_y, paper_keyword)
#     x = 1
#     outer_scopus_ref = []
#
#     return all_result_y


def get_href_from_email(body_x):
    page_soup = soup(body_x, 'html.parser')
    # print(page_soup.prettify())
    str_terminator = 'View all new results in Scopus'
    author_idx = 1
    get_str_scopus_redirect = None
    while get_str_scopus_redirect != str_terminator:
        try:
            get_str_scopus_redirect = \
                page_soup.select(f'body > table.dataTable > tbody > tr:nth-child({author_idx:d}) > td > a')[0].text
            author_idx = author_idx + 1
        except IndexError:
            get_str_scopus_redirect = 1

    papers_href_scopus_def = \
    page_soup.select(f"body > table.dataTable > tbody > tr:nth-child({author_idx - 1:d}) > td > a")[0]['href']
    return papers_href_scopus_def


all_result = []
for i in range(messages, messages - N, -1):
    # fetch the email message by ID
    res, msg = imap.fetch(str(i), "(RFC822)")
    for response in msg:
        if isinstance(response, tuple):
            # parse a bytes email into a message object
            msg = email.message_from_bytes(response[1])
            # extract content type of email
            content_type = msg.get_content_type()
            # get the email body
            try:
                body = msg.get_payload(decode=True).decode()
                # open('test_gmail.html', "w").write(body)
                if content_type == "text/html":
                    papers_href_scopus = get_href_from_email(body)
                    all_result.append(papers_href_scopus)
            except:
                print("An exception occurred")
                pass  # or you could use 'continue'

            gg = 1
    yy = 1
    if index_for_loop % 50 == 0:
        print(f"the number email currently printed is {index_for_loop:d} out of {N:d}")
    index_for_loop = index_for_loop + 1

# Saving the objects:
x=2
f = open('my_complete_scopus.pckl', 'wb')
pickle.dump(all_result, f)
f.close()

# with open('all_information_paper.pkl', 'w') as f:  # Python 3: open(..., 'wb')
#     pickle.dump([all_result], f)

imap.close()
imap.logout()
