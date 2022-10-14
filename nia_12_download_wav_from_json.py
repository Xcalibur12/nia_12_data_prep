import os
import sys
import codecs
import wget

"""
Usage: python nia_12_download_wav_from_json.py [lang].json
"""

input_json = sys.argv[1]
lang_name = input_json.rsplit('.',1)[0]

def mkdir_lang_folder(lang_name):
    lang_data_dir = "{}_data".format(lang_name)
    if not os.path.exists(lang_name):
        os.mkdir(lang_data_dir)
    return lang_data_dir

def download_wav(input_url, out_path):
    wget.download(input_url, out=out_path)

def save_text(text_name, text, out_path):
    w = codecs.open(os.path.join(out_path, text_name), 'w', encoding='utf-8')
    w.write(text)
    w.close()

def make_dataset(input_json, lang_data_dir):
    j_open = codecs.open(input_json, 'r', encoding='utf-8').readlines()[0][1:-1]
    data_chunks = j_open.split("},{")
    for chunk in data_chunks:
        info_list = chunk.split(',')
        for info in info_list:
            if 'audioUrl' in info:
                audio_url = info.split('":"')[-1][:-1]
            if 'sentence' in info:
                text = info.split('":')[-1].split('"')[1].strip()
        text_name = audio_url.split('/')[-1].split('.')[0] + '.txt'

        download_wav(audio_url, lang_data_dir)
        save_text(text_name, text, lang_data_dir)
        
lang_data_dir = mkdir_lang_folder(lang_name)
make_dataset(input_json, lang_data_dir)
