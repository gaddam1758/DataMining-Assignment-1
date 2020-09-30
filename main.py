# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:36:20 2020

@author: ramak
"""

import pandas as pd
import typing
from apriori import frequent_itemsets_from_tranasactions

f = open("T10I4D100K.csv", "r")

transactions =[]


items = set()


while True:
    line = f.readline()
    
    if not line:
        break
    transactions.append(set(sorted(line.split(), key = lambda v: int(v))))
    
    for item in line.split():
        items.add(item)
    

items = sorted(items, key = lambda v : int(v))

frequent_itemsets_from_tranasactions(items, transactions, 0.005)

