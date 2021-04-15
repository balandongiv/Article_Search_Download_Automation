from itertools import zip_longest
import re
import pandas as pd
import numpy as np


def filter_by_type(list_to_test, type_of):
    return [n for n in list_to_test if isinstance(n, type_of)]


def flatten_dict(items, seqtypes=(list, tuple)):
    for i, x in enumerate(items):
        while i < len(items) and isinstance(items[i], seqtypes):
            items[i:i + 1] = items[i]
    return items


def merge_dict(dict1, dict2):
    return [dict(**d1, **d2) for d1, d2 in
            zip_longest(dict1, dict2, fillvalue={})]

    df.replace({r'[^\x00-\x7F]+': 'N-N'}, regex=True, inplace=True)
    df.replace({'N-N': 'X'}, regex=True, inplace=True)


def remove_non_ansi(df):
    df.replace({r'[^\x00-\x7F]+': 'N-N'}, regex=True, inplace=True)
    df.replace({'N-N': 'X'}, regex=True, inplace=True)
    return df


class EndNote:
    def __init__(self, my_dict, file_name=None):



        self.file_name = 'end_note_compat' if file_name is None else file_name
        self.my_dict = my_dict
        self.df = []


        self.conversion_prop()

    def conversion_prop(self):
        self.remove_non_essential()
        self.cleaning_author()
        self.create_df()
        self.df = remove_non_ansi(self.df)

        self.create_header()
        self.df.fillna('').to_csv(f'{self.file_name}.txt', sep='\t', index=False, header=False)
        self.save_as_text()

    def remove_non_essential(self):
        for item in self.my_dict:
            del item['data_resultnum']
            del item['paper_idx']

    def cleaning_author(self):
        regex = re.compile(r'[\n]')
        my_dict = self.my_dict
        for item in my_dict:
            paper_author = regex.sub("", item['paper_author']).replace('(...),', '').rstrip(".").split('.,')
            item['paper_author'] = '.// '.join(paper_author) + '.'

        self.my_dict = my_dict

    def create_header(self):
        df_column_name = pd.DataFrame(list(self.df)).T
        df_column_name.columns = list(self.df)
        empty_df = pd.DataFrame([[np.nan] * len(self.df.columns)], columns=self.df.columns).fillna('')

        df_new_append = empty_df.append(df_column_name.append(self.df, ignore_index=True), ignore_index=True)
        df_new_append.at[0, 'Title'] = '*Generic'

        self.df = df_new_append

    def save_as_text(self):

        with open(f'{self.file_name}.txt', 'r') as file:
            data = re.sub("([\t][\t][\t]+)", "", file.read())
        with open(f'{self.file_name}.txt', 'w') as file:
            file.write(data)

    def create_df(self):
        '''
        Create a df from the list, then change the keys name in compatible to received by Endnote
        :param new_combine:
        :return:
        '''
        df = pd.DataFrame.from_dict(self.my_dict)
        for column_name in list(df):

            if column_name != "author_names":
                df[column_name] = df[column_name].str.lstrip()
                df[column_name] = df[column_name].str.replace('NOT AVAILABLE', '-')

        month_filter = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
                        'August', 'September', 'October', 'November', 'December']

        '''
        Suprising, df rename is quite generic, eventhough the 
        header does not contain one or more of the name, it will issue no
        error.Instead, it will change whatever available
        '''
        df.rename(columns={'paper_title': 'Title', "paper_year": "Year",
                           "paper_publisher_link_paper": "URL",
                           "paper_href_scopus": "Database Provider",
                           "document_abstract": "Abstract",
                           "document_doi": "DOI", "document_publisher": "Publisher",
                           "document_type": "Reference Type", "document_volume": "Volume",
                           "document_issue": "Number", "document_year": "Date",
                           "document_number": "Pages", "paper_author": "Author",
                           "document_journal": "Secondary Title",
                           'abstract': "Abstract"}, inplace=True)

        self.df = df
