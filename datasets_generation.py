# -*- coding: utf-8 -*-
"""
Created on Mon Oct  5 09:25:02 2020

@author: ramak
"""
import random
from collections import defaultdict
import numpy as np 

def generate_dataset(no_trans, no_items, avg_width, filename):
    if avg_width*no_trans > no_trans* no_items:
        return "not possible"
    
    
    transactions = defaultdict(lambda: [])
    i = 0
    while i <avg_width*no_trans:
        row = random.randrange(no_trans)
        col = random.randrange(no_items)
        
        if col in transactions[row]:
            continue
        
        else:
            transactions[row].append(col)
            i+=1
    
    
    f = open(filename, 'w')
    
    for t in transactions.values():
        for item in t:
            f.write(str(item)+" ")
        
        f.write("\n")
    


    
       
        