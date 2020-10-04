# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:59:43 2020

@author: ramak
"""
from collections import defaultdict 
from itertools import chain, combinations
from tqdm import tqdm

#%%
def _get_next_tidsets(F_k_1, k):
    
    C_k = {}
    
    ## Candidate generation step using F[k-1]*F[k-1]
    for itemset_1, tids_1 in F_k_1.items():
        for itemset_2, tids_2 in F_k_1.items():
            itemset_1 = set(itemset_1)
            itemset_2 = set(itemset_2)
            #print(itemset_1,itemset_2)
            difference_1 = list(itemset_1.difference(itemset_2))
            difference_2 = list(itemset_2.difference(itemset_1))
            
            if((len(difference_1)+len(difference_2))==2 and (int(difference_2[0])-int(difference_1[0]))>0):
                candidate = itemset_1.union(itemset_2)
                candidate = tuple(sorted(candidate, key = lambda v : int(v)))
                #print(candidate)
                s = list(set(tids_1).intersection(set(tids_2)))
                if len(s)>0:
                    C_k[candidate] = s
                
    
    ##Pruning step
    ## list of candidates to prune
    r_k = []
    
    for candidate in C_k:
        for subset in combinations(candidate,k-1):
            if not subset in F_k_1:
                r_k.append(candidate)
                break
    
    for candidate in r_k:
        #print(candidate)
        C_k.pop(candidate)
        
    return C_k

#%%
def get_tidsets(transactions, items):
    tidsets = defaultdict(lambda: [])
    
    for item in tqdm(items):
        for id, t in enumerate(transactions):
            set_1 = set(item)
            set_2 = set(t)
            if set_2.issuperset(set_1):
                tidsets[item].append(id)
                
    return tidsets

#%%
def _get_frequent(tidsets, support_count):
    
    F_k = {}
    n_tidsets = defaultdict(lambda: [])
    for itemset, value in tidsets.items():
        # print(itemset,len(value), support_count)
        if len(value)>= support_count:
            F_k[itemset]=len(value)
            n_tidsets[itemset]= value
    
    return F_k, n_tidsets
#%%
def frequent_itemsets(transactions, items, min_support):

    
    tidsets = get_tidsets(transactions, items)
    min_support_count = min_support* len(transactions)
    print("minimum support count is ", min_support_count)
    print("generating frequent itemsets")
    print("generating 1-itemsets")
    
    F = []
    k = 1 
#%%

    print(type(tidsets))
    while len(tidsets):
       F_k, tidsets= _get_frequent(tidsets, min_support_count)
       print("generating",k ,"-itemsets")
       k+=1
       tidsets = _get_next_tidsets(tidsets,k)
       print(F_k)
       F.append(F_k)
       



#%%
f = open("T10I4D100K.dat", "r")

transactions =[]


items = set()


while True:
    line = f.readline()
    
    if not line:
        break
    transactions.append(set(sorted(line.split(), key = lambda v: int(v))))
    
    for item in line.split():
        items.add((item,))
    

items = sorted(items, key = lambda v : int(v[0]))
frequent_itemsets(transactions, items, 0.05)