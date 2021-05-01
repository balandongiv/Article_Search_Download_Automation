# from scidownl.scihub import SciHub, STD_INFO, STD_ERROR
from scidownl.scihub import *
from joblib import Parallel, delayed
import re

# fname_txt_from_endnote = 'vision_x_fail_download'


class get_ref_pdf:
    def __init__(self, fname):
        self.fname = fname
        # self.out=fname
        self.doi_ls = []
        self.njob = 1
        self.get_doi_ref()
        self.dowload_doi()
        print('success')






    def dowload_doi(self):
        for trial in [1,2,3]:
            print(f'attempt no {trial}')
            if self.njob==1:
                status = [self.par_retrieve(doi) for doi in self.doi_ls]
            else:
                print('used parallel')
                status = Parallel(n_jobs=3)(delayed(self.par_retrieve)(doi) for doi in self.doi_ls)


            self.doi_ls = [f'doi:{x}' for x in status if x != '0' and x != '-1']


    def get_doi_ref(self):
        DOIs = []
        with open(f'{self.fname}.txt', "r", encoding='utf-8') as file:
            data = file.read().splitlines()
            for x in data:
                try:
                    DOIs.append(x.split('doi')[1].split(':')[1])
                except IndexError:
                    vv = x.split(').')[1]
                    print(vv)
                    continue

        self.doi_ls = list(filter(None, [x.split('doi')[1].split(':')[1] for x in data]))

    def par_retrieve(self,doi):
        # Using a try catch to catch exceptions for avoiding code interruption
        # if something goes wrong in this for-loop.

        try:
            print("\n%sDoi: %s" % (STD_INFO, doi))
            SciHub(doi, self.fname).download(choose_scihub_url_index=-1)
            status = '0'
        except Exception as e:
            print("%sDownload error with doi: %s. Error message: %s" % (STD_ERROR, doi, e))
            # unsucccesful_download.append(doi)
            status = '-1' if not doi else doi

        return status

get_ref_pdf('autoreject_2')


print('complete')
