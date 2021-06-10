import argparse
import glob
import os
import json
import pickle
from tqdm import tqdm
import pandas as pd

def fig2caption_sents(paper_data_path,img_filenames):
    structured_data=dict()
    with open(paper_data_path,'rb') as f:
        paper_data=pickle.load(f)
    for paper_id, data in tqdm(paper_data.items(),desc='fig2caption_sents'):
        Fig_ALL=data['Fig_ALL']
        for fig in Fig_ALL:
            file_name=fig['xsrc'].split('.')[0]
            if file_name not in img_filenames:
                continue
            caption=fig['caption']
            structured_data[file_name]=caption
    return structured_data
 
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Code to preprocess for caption')
    parser.add_argument('--paper_data_path', default='../prepro_RSC/paper_data.pkl',help='')
    parser.add_argument('--csv_dir', default='../dataCSV',type=str)
    args = parser.parse_args()
    
    csv_paths=glob.glob(os.path.join(args.csv_dir,'*.csv'))
    img_filenames=list()
    for csv_path in csv_paths:
        df=pd.read_csv(csv_path)
        for paper_id,fig_id,label in zip(list(df['paper_id']),list(df['fig_id']),list(df['label'])):
            file_name = paper_id+'-'+fig_id
            
            img_filenames.append(file_name)
    structured_data = fig2caption_sents(args.paper_data_path,img_filenames)
    
    with open('../dataset/caption.json','w') as f:
        json.dump(structured_data,f)
