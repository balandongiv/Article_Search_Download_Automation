import pickle
from oatd import ScrapeOatd

x=1
# current_user = getuser()


# new_dict = dict(test_xx='test', other_la='other la')
# new_dict.update(new_add='Geeks')
# x = 1
# url = 'https://oatd.org/oatd/search?q=eeg&form=basic'
url = 'https://oatd.org/oatd/search?q=eeg&form=basic&pubdate.facet=1991'  # 88 result , 3 pages
oatd = ScrapeOatd()
all_result = oatd.scrape_oatd(url)
print('complete scrape search result')
all_website_scrape = oatd.loop_get_specific(all_result)
print('complete scrape specific page')

x = 1

with open('oatd_complete_all_specific_page.pickle', 'wb') as handle:
    pickle.dump(all_website_scrape, handle, protocol=pickle.HIGHEST_PROTOCOL)
    print('complete saving')

# html_oatd_specific_page
# r = requests.get('https://oatd.org/oatd/record?record=handle\:11012\%2F16478&q=eeg')
# page_soup = Soup(r.text, 'html.parser')