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
from preprocess import file2csv




def preprocess_query(input_str):
    
    sent_words = list(jieba.cut(input_str))
    document = " ".join(sent_words)
    
    return document
        


# to rank restaurant by query
def main_input_rank(input_str="牛肉麵", top_n=10):
    
    def get_item_name(id):
        return df.loc[df['id'] == id]['name'].tolist()[0]
    
    def get_item_descr(id):
        return df.loc[df['id'] == id]['description_orig'].tolist()[0]
        
    def get_item_url(id):
        return df.loc[df['id'] == id]['url'].tolist()[0]
    
    
    def recommend(input_str, top_n):
        url_list=[]
        print("Recommending top " + str(top_n) + " products based on query: " + input_str)
        print("="*160)
        for order, rec in enumerate(similar_items,1):
            url_list+=[get_item_url(rec[1])]
            print("Recommended%d: "%order + get_item_name(rec[1]) + " (score:" + str(np.around(rec[0],6)) + ")" + " /description: " + get_item_descr(rec[1]))
            print("-"*160)
        
        return url_list
    
    
    df = pd.read_csv('tripadvisor_data.csv',encoding = 'utf-8-sig')
    
    tf = TfidfVectorizer(analyzer='word', max_features=200 , ngram_range=(1, 1), min_df=0, max_df = 0.6,stop_words=["是","的","了"],token_pattern=r"(?u)\b\w+\b").fit(df['description'])
    
    tfidf_matrix = tf.fit_transform(df['description'])
    
    input_str_pre = preprocess_query(input_str)
    time_now = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_data')
    df_input = pd.DataFrame({'datetime':[time_now],'description':[input_str], 'description_preprocess':[input_str_pre]})
    print('the query info:\n',df_input)
    print('\n')
    
    
    tfidf_matrix_input = tf.transform(df_input['description_preprocess'])
    cosine_similarities = linear_kernel(tfidf_matrix_input, tfidf_matrix)

    
    similar_indices = cosine_similarities[0].argsort()[:-(top_n+1):-1] # top-n : the most similar
    similar_items = [(cosine_similarities[0][i], df['id'][i]) for i in similar_indices]
    
    
    return recommend(input_str = input_str, top_n=top_n)
    


if __name__ == "__main__":
    # file2csv() #step1: transform json to csv
    input_str = input("find your favorite restaurant! input query:  ") #step2: do query (specific query, e.g. 牛肉麵 or 燒烤 烤肉 or 火鍋吃到飽...)
    url_list = main_input_rank(input_str = input_str, top_n = 20)
    print(url_list)
    
    