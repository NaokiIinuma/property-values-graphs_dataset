import glob
from get_FigCaption import extract_xml
from tqdm import tqdm
import pickle

RSC_dir='../RSC_data'
paths=glob.glob(RSC_dir+'/*/C*')
paper_data_all=dict()
for i,path in enumerate(tqdm(paths)):
    paper_data = extract_xml(path)
    paper_data_all[path[1:]]=paper_data

with open('paper_data.pkl','wb') as f:
    pickle.dump(paper_data_all,f)