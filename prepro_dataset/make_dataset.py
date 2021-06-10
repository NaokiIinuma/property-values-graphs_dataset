import pandas as pd
import os
import glob
import shutil
from tqdm import tqdm
from PIL import Image


def convert_IMGF(out_dir,in_IMGF='gif',out_IMGF='png'):
    paths = glob.glob(os.path.join(out_dir,'*.'+in_IMGF))
    for path in tqdm(paths, desc='convert_IMGF'):
        img = Image.open(path)
        img.save(path.split('.')[0]+'.'+out_IMGF,out_IMGF)
        os.remove(path)

csv_dir='../dataCSV'
data_dir='../dataset/holdout'
RSC_dir='../RSC_data'
fig_path=glob.glob(os.path.join(RSC_dir,'*','*','*.gif'))

if os.path.exists(data_dir):
    shutil.rmtree(data_dir)
os.makedirs(data_dir)

imgF='gif'
for data_type in ['train','val','test']:
    path=os.path.join(csv_dir,data_type+'.csv')
    df=pd.read_csv(path)
    labels=set(df['label'])
    for label in labels:
        os.makedirs(os.path.join(data_dir,data_type,label))
    for paper_id,fig_id,label in zip(list(df['paper_id']),list(df['fig_id']),list(df['label'])):
        file_name = paper_id+'-'+fig_id+'.'+imgF
        path=RSC_dir+os.path.join('*',paper_id.upper(),file_name)
        hit_path=glob.glob(path)
        assert len(hit_path)==1, 'Multiple images were retrieved.'
        shutil.copyfile(hit_path[0],os.path.join(data_dir,data_type,label,file_name))
    label_dirs=glob.glob(os.path.join(data_dir,data_type,'*'))
    for label_dir in label_dirs:
        convert_IMGF(label_dir)