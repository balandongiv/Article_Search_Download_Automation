# from module_extract_scopus_ref import ScrapeScopus
from module_extract_scopus_ref import ScrapeScopus
import pickle

specific_second_paper_fname = 'specific_second_paper_fname'
scopus_search_result_fname = 'scopus_search_result_09072020'


def specific_second_paper():
    '''
    The following line exemplified how we can extract the specific reference page along with
    citing paper which exist in the multi search result of the scopus
    Last tested successfully on 7 July 2020

    '''
    to_url_one = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-84920188336&citeCnt=1&origin=resultslist&sort=cp-f&src=r&citingId=2-s2.0-85078145235&imp=t&sid=3740bc265f2d4ddf9fcdca7262b0991a&sot=rec&sdt=citedreferences&sl=19&s=CITEID%2885078145235%29&relpos=5&citeCnt=2152&searchTerm='
    # to_url_one = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-85078145235&origin=resultslist&sort=plf-f&src=s&st1=functional+connectivity+dynamic+eeg&nlo=&nlr=&nls=&sid=aea800185c3b86b309614317c35f01eb&sot=b&sdt=cl&cluster=scopubyr%2c%222020%22%2ct&sl=50&s=TITLE-ABS-KEY%28functional+connectivity+dynamic+eeg%29&relpos=0&citeCnt=0&searchTerm='
    to_url_two = 'https://www.scopus.com/record/display.uri?eid=2-s2.0-0025157159&citeCnt=1&origin=resultslist&sort=cp-f&src=r&nlo=&nlr=&nls=&citingId=2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264%2c2-s2.0-0035895264&imp=t&sid=5ec876ad336dcfd337d4c8e363922c09&sot=rec&sdt=citedreferences&sl=18&s=CITEID%280035895264%29&relpos=19&citeCnt=109&searchTerm='
    url_list = [to_url_one, to_url_two]
    ssc = ScrapeScopus(url_list)
    compiled_reports = ssc.loop_url
    save_as_pickle(compiled_reports, specific_second_paper_fname)


def scopus_search_result(search_pages):
    '''
    The following line exemplified how we can extract the multi search result of the scopus
    Last tested successfully on 7 July 2020

    '''
    if search_pages == 4:
        # 4 finding pages
        to_url = 'https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=functional+connectivity+dynamic+eeg&nlo=&nlr=&nls=&sid=aea800185c3b86b309614317c35f01eb&sot=b&sdt=cl&cluster=scopubyr%2c%222020%22%2ct&sl=50&s=TITLE-ABS-KEY%28functional+connectivity+dynamic+eeg%29&origin=resultslist&zone=leftSideBar&editSaveSearch=&txGid=245562f04224d1d510cd4baf035acdc8'
    else:
        # 100 finding pages
        to_url = 'https://www.scopus.com/results/results.uri?numberOfFields=0&src=s&clickedLink=&edit=&editSaveSearch=&origin=searchbasic&authorTab=&affiliationTab=&advancedTab=&scint=1&menu=search&tablin=&searchterm1=eeg&field1=TITLE_ABS_KEY&dateType=Publication_Date_Type&yearFrom=Before+1960&yearTo=Present&loadDate=7&documenttype=All&accessTypes=All&resetFormLink=&st1=eeg&st2=&sot=b&sdt=b&sl=18&s=TITLE-ABS-KEY%28eeg%29&sid=0f89a80c1e6e3899b912f7a6e5a2b440&searchId=0f89a80c1e6e3899b912f7a6e5a2b440&txGid=ea811351228dc8eeb9aca419ffc236c9&sort=plf-f&originationType=b&rr='

    ssc = ScrapeScopus([to_url])
    compiled_reports = ssc.loop_url_second

    save_as_pickle(compiled_reports, scopus_search_result_fname)


def save_as_pickle(compiled_reports, save_file_name):
    with open(f'{save_file_name}.pickle', 'wb') as handle:
        pickle.dump(compiled_reports, handle, protocol=pickle.HIGHEST_PROTOCOL)
        print('complete saving')


# specific_second_paper()

# can choose either total pages of 4 or 100
pages_number = 4
scopus_search_result(pages_number)
x = 1
