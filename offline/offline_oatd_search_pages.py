

url = r'html_oatd_specific_page.html '

with open(url, 'r', encoding='utf-8') as f:
    page_soup = Soup(f, 'html.parser')