# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 19:25:54 2020

@author: ramak
"""

from apriori import apriori
from fpGrowth import fp
from eclat import eclat

import time
import os
import matplotlib.pyplot as plt

def plot(y, X, labels, title):
    plt.figure()
    for _y in y:
        plt.plot(X, _y)
        
    plt.title(title)
    
    plt.xlabel('minimum support', fontweight ='bold') 
    plt.ylabel('time taken', fontweight ='bold')  
    plt.legend(labels)
    plt.plot
    plt.savefig("figures/"+title+'.png')


def run(file, support, categorical):
    a_t = []
    e_t = []
    f_t = []
    
    for s in support:
        
        t1 = time.time()
        apriori(file,s,categorical)
        a_t.append(time.time()-t1)
        
        t1 = time.time()
        eclat(file,s,categorical)
        e_t.append(time.time()-t1)
        
        t1 = time.time()
        fp(file,s,categorical)
        f_t.append(time.time()-t1)
    return a_t,e_t, f_t  
        
    
Datasets = os.listdir('data')


## apriori comparison on various datasets

times = {}

support_T4 = [0.1,0.15,0.2,0.25]
support = [0.05, 0.1, 0.15, 0.2]
labels = ['aprior','eclat', 'fp']


categorical = False

for file in Datasets:
    
    if file == 'groceries.csv':
      categorical = True
    else:
         categorical = False
    
    if file =="T40I10D100K.dat":
        t = run("data/"+file, support_T4, categorical)
        times[file]=t
    else:
        t = run("data/"+file, support, categorical)
        times[file]=t
        
for t in times:
    if file =="T40I10D100K.dat":
        plot(times[t], support, labels, t)
    else:
        plot(times[t], support, labels, t)
        