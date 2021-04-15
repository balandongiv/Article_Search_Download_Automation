from module_extract_scopus_ref import ScrapeScopus
import pickle
import csv
import re
import pandas as pd
from itertools import groupby
import numpy as np
from unidecode import unidecode

csv_file_name = 'endnote_csv_july_09_2nd_cisir'
save_pickle_name = 'oatd_complete_all_specific_page'
oatd_search_result_fname = 'oatd_specific_pages_12072020xX'


def compile_to_pandas():
    my_dict_x = pickle.load(open(f'{save_pickle_name}.pickle', "rb"))
    # my_dict_x=my_dict_x[1:20]  # [3:5] HAVE PROB
    df = pd.DataFrame.from_dict(my_dict_x)

    df.replace({r'[^\x00-\x7F]+': 'N-N'}, regex=True, inplace=True)
    df.replace({'N-N': 'X'}, regex=True, inplace=True)
    '''
    OPTIONAL, USE ONLY WHEN THERE IS PROBLEM IN THE FUTURE
    df=df.replace({r'(\W)*$': ""}, regex=True)
    df.replace(r'\.', '', regex=True)
    '''


    df.rename(columns={'paper_title': 'Title', "paper_author": "Author", \
                       "paper_datePublished": "Year", "paper_url": "URL", \
                       "paper_publisher": "Publisher", "paper_abstract": "Abstract", \
                       "href_to_oatd": "Database Provider", \
                       "paper_about": "Keywords"}, inplace=True)

    '''
    There are two possibilites in positioning the replace, they can be before of after of each other, but actual
    test case is absent now! Difficult to validate
    '''
    for idx, row in df.iterrows():
        text = df.loc[idx, 'URL']
        df.loc[idx, 'URL'] = text.replace('\r\n', '\n').replace('\n', ' \\\ ')

    df = df.replace('\n', '', regex=True)

    df_column_name = pd.DataFrame(list(df)).T
    df_column_name.columns = list(df)
    empty_df = pd.DataFrame([[np.nan] * len(df.columns)], columns=df.columns).fillna('')
    df_new_append = empty_df.append(df_column_name.append(df, ignore_index=True), ignore_index=True)
    df_new_append.at[0, 'Author'] = '*Generic'
    df_new_append.fillna('').to_csv(f'{oatd_search_result_fname}.txt', sep='\t', index=False, header=False)


    with open(f'{oatd_search_result_fname}.txt', 'r') as file:
        data = re.sub("([\t][\t][\t]+)", "", file.read())
    with open(f'{oatd_search_result_fname}.txt', 'w') as file:
        file.write(data)


print('compile result to pandas')
compile_to_pandas()
