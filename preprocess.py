# coding=utf-8
# https://github.com/nikitaa30/Content-based-Recommender-System/blob/master/recommender_system.py
import pandas as pd
import numpy as np
import json
import jieba
from os import listdir
from os.path import join, basename, dirname
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel, cosine_similarity
import time
import datetime


def read_data():
    data = []
    with open('tripadvisor_restaurant_formatted.json', 'r',encoding="utf-8") as f:
        data = json.load(f)
    return data
    
    
def file2csv():

    data = read_data()
    
    id_list = []
    url_list = []
    name_list = []
    description_orig_list = []
    description_final_list = []
    
    total_doc = len(data)
    
    count = 0
    for _id, restaurant_data in enumerate(data,1):
        count += 1
        print(f'progress:{count}/{total_doc}={np.around(count/total_doc*100,2)}%')
        
        id_list += [_id]
        url_list += [restaurant_data['url']]
        name_list += [restaurant_data['name']]
        
        str1 = restaurant_data['name'] + '，' #21工房天然手工涼麵（酒泉店，
        
        
        str2 = ""
        criteria = 20
        for review in restaurant_data['reviews']:
            if len(review['quote']) < criteria:
                str2 += (review['quote'] + '，') # 老字號西餐館, CP值超低, 好吃...
            else:
                pass
        
        
        str3 = restaurant_data['rating']['overall']+ '，' #4.0，
        str4 = ' '.join(str(e) for e in restaurant_data['characteristics']) + '，' #菜系 日式料理 亞洲料理 餐點 午餐, 晚餐，
        text = str1+str2+str3+str4
        description_orig_list += [text]
        
        sent_words = list(jieba.cut(text))
        document = " ".join(sent_words)
        description_final_list += [document]
        
        
        
    pd.DataFrame({'id':id_list, 'name':name_list, 'url':url_list, 'description_orig':description_orig_list, 'description':description_final_list}).to_csv('tripadvisor_data.csv',index = False, encoding='utf-8-sig')    
    
    

if __name__ == "__main__":
    file2csv()
