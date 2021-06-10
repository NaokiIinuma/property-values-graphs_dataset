cd prepro_RSC
python exe_get_FigCaption.py
cd ../prepro_dataset
python make_dataset.py
cd ../prepro_caption
python prepro_captionCSV.py
cd ..