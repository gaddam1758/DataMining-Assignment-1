# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 22:59:43 2020

@author: ramak
"""
from collections import defaultdict 



def get_apriori_candidate_itemsets(F_k_1, k):
    
    C_k = []
    
    ## Candidate generation step using F[k-1]*F[k-1]
    for itemset_1 in F_k_1:
        for itemset_2 in F_k_1:
            itemset_1 = set(itemset_1)
            itemset_2 = set(itemset_2)
            #print(itemset_1,itemset_2)
            difference_1 = list(itemset_1.difference(itemset_2))
            difference_2 = list(itemset_2.difference(itemset_1))
            
            if((len(difference_1)+len(difference_2))==2 and (int(difference_2[0])-int(difference_1[0]))>0):
                candidate = itemset_1.union(itemset_2)
                candidate = sorted(candidate, key = lambda v : int(v))
                #print(candidate)
                C_k.append(tuple(candidate))
    
    ##Pruning step
    ## list of candidates to prune
    r_k = []
    
    #print(F_k_1)
    
    for candidate in C_k:
        for subset in combinations(candidate,k-1):
            if not subset in F_k_1:
                r_k.append(candidate)
                break
    
    
    for candidate in r_k:
        #print(candidate)
        C_k.remove(candidate)
        
    return C_k


def get_tidsets(transactions, items):
    tidsets = defaultdict(lambda: [])
    for item in items:
        for t in transactions:
            set_1 = set(item)
            set_2 = set(t)
            if set_2.issuperset(set_1):
                tidsets[item].append(t)

def frequent_itemsets(transactions, items):
    tidsets = get_tidsets(transactions, items)
    