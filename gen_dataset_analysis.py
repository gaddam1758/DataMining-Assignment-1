# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 21:34:10 2020

@author: ramak
"""


from datasets_generation import generate_dataset
from apriori import apriori
from fpGrowth import fp
from eclat import eclat

import time
import os
import matplotlib.pyplot as plt
import numpy as np

def run(file, s, categorical=False):
    a_t = 0
    e_t = 0
    f_t = 0
    t1 = time.time()
    apriori(file,s,categorical)
    a_t = time.time()-t1
        
    t1 = time.time()
    eclat(file,s,categorical)
    e_t = time.time()-t1
        
    t1 = time.time()
    fp(file,s,categorical)
    f_t = time.time()-t1
    return a_t,e_t, f_t  

def plot(y, X, labels, title, variable):
    plt.figure()
    for _y in y:
        plt.plot(X, _y)
        
    plt.title(title)
    
    plt.xlabel(variable, fontweight ='bold') 
    plt.ylabel('time taken', fontweight ='bold')  
    plt.legend(labels)
    plt.plot
    plt.savefig("figures/"+title+".png")



transactions = [20000, 50000, 70000,100000]

support = 0.05

items = 1000

avg_width = 10
labels = ['aprior','eclat', 'fp']

times = []
folder = 'gen_data/'
# for t in transactions:
#     filename = folder+"gen_dat_trans"+str(t)
    
#     generate_dataset(t, items,avg_width, filename)
    
#     times.append(list(run(filename,support)))


# t = np.array(times).T
# t = t.tolist()

# plot(t, transactions, labels, 'trans_vary',' no of transactions')

transactions = 70000 

avg_width = 10

items = [500, 800, 1000, 1500]

times = []
folder = 'gen_data/'
for t in items:
    filename = folder+"gen_dat_items"+str(t)
    
    generate_dataset(transactions, t,avg_width, filename)
    
    times.append(list(run(filename,support)))

t = np.array(times).T
t = t.tolist()
print(times)

plot(t, items, labels, 'items_vary',' no of items')


# transactions = 70000 

# avg_width = [10, 15, 20, 30]

# items = 1000

# times = []
# folder = 'gen_data/'
# for t in avg_width:
#     filename = folder+"gen_dat_items"+str(t)
    
#     generate_dataset(transactions,  items ,t, filename)
    
#     times.append(list(run(filename,support)))

# t = np.array(times).T
# t = t.tolist()
# print(times)

# print(avg_width)

# plot(t, avg_width, labels, 'avg_width_vary',' avg_width')


