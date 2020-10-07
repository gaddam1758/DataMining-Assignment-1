# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 14:05:24 2020

@author: ramak
"""

import pandas as pd
import numpy as np
import io
from collections import defaultdict


def cate_to_num(filename):
    
    f = open(filename, "r")
    
    items = defaultdict( lambda : 0)
    count =1;
    transactions = []
    while True:
        line = f.readline()
        
        if not line:
            break
        
        line = line.rstrip('\n')
        transactions.append(line.split(','))
        for item in line.split(','):
            items[item] = 0
    
    for item in items:
        items[item]=count
        count+=1
    
    n_t =[]
    for t in transactions:
        trans=[]
        for k in t:
            trans.append(items[k])
        n_t.append(tuple(trans))
    
    return n_t, items
        

