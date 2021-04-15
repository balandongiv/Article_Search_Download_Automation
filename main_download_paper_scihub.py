# from scidownl.scihub import SciHub, STD_INFO, STD_ERROR
from scidownl.scihub import *

# DOI = "10.1021/ol9910114"
# out = 'paper'
# sci = SciHub(DOI, out).download(choose_scihub_url_index=3)
# DOIs_x = ['10.1038/s41598-018-36976-y',
#         '10.1111/gcb.12455',
#         '10.1371/journal.pone.0097223',
#         '10.1093/conphys/cox005']
DOIs=[]
with open('autoreject_2.txt', "r",encoding='utf-8') as file:
    data = file.read().splitlines()
    for x in data:
        try:
            DOIs.append(x.split('doi')[1].split(':')[1])
        except IndexError:
            vv=x.split(').')[1]
            print(vv)
            continue

    # DOIs=[x.split('doi')[1].split(':')[1] for x in data]
    t=1

out = 'paper'
for doi in DOIs:
    # Using a try catch to catch exceptions for avoiding code interruption
    # if something goes wrong in this for-loop.
    try:
        print("\n%sDoi: %s" %(STD_INFO, doi))
        SciHub(doi, out).download(choose_scihub_url_index=3)
    except Exception as e:
        print("%sDownload error with doi: %s. Error message: %s" %(STD_ERROR, doi, e))
print('complete')