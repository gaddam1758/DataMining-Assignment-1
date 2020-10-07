# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:59:43 2020

@author: ramak
"""
from collections import defaultdict 
from itertools import chain, combinations
from tqdm import tqdm
from grocery_dat_cleaning import cate_to_num

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
            if((len(difference_1)==1 and len(difference_2))==1):
                candidate = itemset_1.union(itemset_2)
                candidate = tuple(sorted(candidate, key = lambda v : int(v)))
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

# #%%
# def get_tidsets(transactions, items):
#     tidsets = defaultdict(lambda: [])
    
    
#         for id, t in enumerate(transactions):
#             set_1 = set(item)
#             set_2 = set(t)
#             if set_2.issuperset(set_1):
#                 tidsets[item].append(id)
                
#     return tidsets

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
def frequent_itemsets(tidsets, items, min_support_count):

    print("minimum support count is ", min_support_count)
    print("generating frequent itemsets")
#   print("generating 1-itemsets")
    
    F = []
    k = 1
#%%
    while len(tidsets):
       F_k, tidsets= _get_frequent(tidsets, min_support_count)
       print("generating",k ,"-itemsets")
       k+=1
       tidsets = _get_next_tidsets(tidsets,k)
       F.append(F_k)
       #print(F_k)
       
    total = []
    for f in F:
        total =total+list(f)
    return total     



#%%
def eclat(filename, support, categorical = False):
    
    if not categorical:
        f = open(filename, "r")
    
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
        
        tidsets = defaultdict(lambda: [])
        
        
        for id, t in enumerate(transactions):
            for item in t:
                tidsets[(item,)].append(id)
            
        min_support_count = support* len(transactions)
        return frequent_itemsets(tidsets, items, min_support_count)
    
    else:
        transactions, items = cate_to_num(filename)
        
        tidsets = defaultdict(lambda: [])
        
        
        for id, t in enumerate(transactions):
            for item in t:
                tidsets[(item,)].append(id)
            
        min_support_count = support* len(transactions)
        
        itemsets = frequent_itemsets(tidsets, list(items.values()), min_support_count)

        ##convert to catergorical
        inv_map = {v: k for k, v in items.items()}
        n_itemsets = []
        

        for itemset in itemsets:
            k = []
            
            for item in itemset:
  
                k.append(inv_map[item])
            n_itemsets.append(k)   
        
        return n_itemsets