# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:28:13 2020

@author: ramak
"""



from eclat import eclat
import os

from grocery_dat_cleaning import cate_to_num



Datasets = os.listdir('data')
Datasets = Datasets


support = 0.05


for file in Datasets:
    
    no_item = 0
    no_trans = 0
    avg_width = 0
        
    if file == 'groceries.csv':
      categorical = True
    else:
         categorical = False
   
    if not categorical:
        f = open("data/"+file, "r")
    
        transactions =[]
    
    
        items = set()
        
        
        count = 0
        while True:
            line = f.readline()
        
            if not line:
                break
            transactions.append(tuple(sorted(line.split(), key = lambda v: int(v))))
            for item in line.split():
                items.add(item)
                count+=1
        
        no_item = len(items)
        no_trans = len(transactions)
        avg_width = count/no_trans
        
    else :
        trans, items = cate_to_num(file)
        
        count =0
        for t in trans:
            count+=len(t)
        
        no_item = len(items)
        no_trans = len(trans)
        avg_width = count/no_trans
        
    freq = eclat("data/"+file,support, categorical)
    
    siz_max_freq = 0
    for f in freq:
        if len(f)>siz_max_freq:
            siz_max_freq = len(f)
    
    max_freq = 0
    
    for f in freq :
        if len(f ) == siz_max_freq:
            max_freq+=1
    
    print("---------------------------")
    print(file+" dataset"+ " info")
    
    print("no of transaction are ", no_trans)
    
    print("no of items are ", no_item)
    
    print("average width of transaction is ", avg_width)
    
    
    print("below values are obtained on support of 5% on eclat algo")
    
    print("maximum size of  frequent itemset is ", siz_max_freq)
    
    print("size of maximum frequent itemsets is ", max_freq)
    
    print("---------------------------")
   
    
   