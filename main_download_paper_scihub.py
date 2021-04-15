# from scidownl.scihub import SciHub, STD_INFO, STD_ERROR
from scidownl.scihub import *
from joblib import Parallel, delayed

# from scidownl.update_link import *

# Use crawling method to update available Scihub links.
# update_link(mod='c')
# # Use brute force search method to update available Scihub links.
# update_link(mod='b')

# DOI = "10.1021/ol9910114"
# out = 'paper'
# sci = SciHub(DOI, out).download(choose_scihub_url_index=3)
# DOIs_x = ['10.1038/s41598-018-36976-y',
#         '10.1111/gcb.12455',
#         '10.1371/journal.pone.0097223',
#         '10.1093/conphys/cox005']


# status = ['-1', '2', '3', '0']
# opt=[f'xt:{x}' for x in status if x != '0' and x !='-1']
#
# opt=[f'doi:{x}' for x in status if x != '0' and x !='-1']
# with open("file.txt", "w") as output:
#     output.write(str(opt))
DOIs = []
# fname_txt_from_endnote='autoreject_2'
fname_txt_from_endnote = 'vision_camera'
with open(f'{fname_txt_from_endnote}.txt', "r", encoding='utf-8') as file:
    data = file.read().splitlines()
    for x in data:
        try:
            DOIs.append(x.split('doi')[1].split(':')[1])
        except IndexError:
            vv = x.split(').')[1]
            print(vv)
            continue

    # DOIs=[x.split('doi')[1].split(':')[1] for x in data]
    t = 1

# DOIs = DOIs[1:3]
out = 'paper_vision'
unsucccesful_download = []


def par_retrieve(doi):
    # Using a try catch to catch exceptions for avoiding code interruption
    # if something goes wrong in this for-loop.
    try:
        print("\n%sDoi: %s" % (STD_INFO, doi))
        SciHub(doi, out).download(choose_scihub_url_index=-1)
        status = '0'
    except Exception as e:
        print("%sDownload error with doi: %s. Error message: %s" % (STD_ERROR, doi, e))
        # unsucccesful_download.append(doi)
        status = '-1' if not doi else doi

    return status


# status = [par_retrieve(doi) for doi in DOIs]
status = Parallel(n_jobs=-1)(delayed(par_retrieve)(doi) for doi in DOIs)
opt=[f'doi:{x}' for x in status if x != '0' and x !='-1']
with open(f"{fname_txt_from_endnote}_fail_download.txt", "w") as output:
    output.write(str(opt))

print('complete')
