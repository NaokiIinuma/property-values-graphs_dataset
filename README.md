# Preparation
## Environment construction
1. Creat virtual environment and activate
```
conda create -n test python=3.6.12
conda activate test
```
2. Install bellow packages by conda
    
    pandas, tqdm, pillow, nltk, gensim, scikit-learn
```
conda install PACKAGE
```
3. Install scispacy by pip
```
pip install scispacy
pip install https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.4.0/en_core_sci_sm-0.4.0.tar.gz
```
## Obtain and install the paper data in xml format
Purchase the paper data of [Journal of Material Chemistry A](https://www.rsc.org/journals-books-databases/about-journals/journal-of-materials-chemistry-a/) (2015-2019).

Then, place the paper data under `RSC_data` so that the file structure is as follows.
```
└─RSC_data
    ├─2015
    ├─2016
    ├─2017
    ├─2018
    └─2019
        ├─PAPER_ID:1
        ├─PAPER_ID:2
        ...
        └─PAPER_ID:N
            ├─Figure images in the paper in tif or gif format.
            ├─Paper in pdf format.
            └─Paper in XML format.
```
# Run
```
bash prepro.sh
```
The above command will create labeled images under `dataset/holdout` and caption.json that maps the image file name to a caption under `dataset`.
