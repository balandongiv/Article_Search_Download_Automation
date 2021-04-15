from scopus import ScrapeScopus
import pickle
from my_tool import EndNote

'''
This should be the final version ya, work like a charm
27 July 2020
This version should supersede the file
scopus_to_endnote
'''
csv_file_name = 'endnote_csv_july_26'
save_pickle_name = 'to_extract_endnote_new_revision_july_26'
scopus_search_result_fname = 'scopus_search_result_26072020'

login_detail_email = 'balandongiv@gmail.com'
login_detail_passwod = '8487936iV@'


def use_search_term():
    search_term = 'fatigue camera drowsy'
    # Info_ = Info(search_term=search_term)
    ss = ScrapeScopus()
    all_url_list = ss.scrape_via_search_term(search_term=search_term)
    with open(f'{scopus_search_result_fname}.pickle', 'wb') as handle:
        pickle.dump(all_url_list, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print('complete')


def endnote_compatible():
    my_dict_x = pickle.load(open(f'{scopus_search_result_fname}.pickle', "rb"))
    EndNote(my_dict_x, file_name=scopus_search_result_fname)


def get_multiple_doi():
    '''
    https://stackoverflow.com/questions/27910/finding-a-doi-in-a-document-or-page
    '''

    all_info = []
    ss = ScrapeScopus()
    doi_list = ['10.1109/ACCESS.2018.2811723', '10.1016/j.aap.2016.12.002']
    for search_term in doi_list:

        all_url_list = ss.scrape_via_search_term(search_term=search_term, keyword='DOI')
        doi_extract = all_url_list[0]['document_doi']
        if search_term == doi_extract:
            url = all_url_list[0]['paper_href_scopus']
            all_result_x, document_reports = ss.scrape_scopus_article(url, paper_reference=True,
                                                                      related_document=True,
                                                                      cited_document=True)
        all_info.append(all_url_list)


use_search_term()
endnote_compatible()
# get_multiple_doi()
