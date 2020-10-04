# -*- coding: utf-8 -*-
"""
Created on Mon Sep 28 11:48:15 2020

@author: ramak
"""
import collections
import typing
from dataclasses import field, dataclass
from collections import defaultdict 
from itertools import chain, combinations
         


class hash_node:
    
   def __init__(self, leaf_size=0):
        self.children = {}           
        self.Leaf_status = True      
        self.bucket = {}       
        
        for i in range(leaf_size):
            self.children[i] =hash_node()
            
            
class hash_tree:
    hash_key : int 
    leaf_size : int
    root = None
    
    def __init__(self, values, hash_key = 3, leaf_size = 3, level = 0):
        self.hash_key = hash_key
        self.leaf_size = leaf_size
        self.root = hash_node(leaf_size)
        self.root.Leaf_status = False
        for v in values:
            self.insert( self.root, list(v))
        
    def insert(self, node, value, level =0):
        
        if not node.Leaf_status :
                key = int(value[level])%(self.hash_key)
                self.insert(node.children[key], value, level+1)
        
        else:
            
            if(len(node.bucket)==self.leaf_size and (level == len(value) or level == len(value)-1)): ##leaf node is reached and length of itemset is reached for hashing
                node.bucket[tuple(value)] = 0
                return
            
            elif(len(node.bucket) == self.leaf_size):
                level+=1
                node.Leaf_status = False
                for i in range(self.leaf_size):
                    node.children[i]=hash_node()
                    
                key = int(value[level])%(self.hash_key)
                self.insert(node.children[key], value, level)
                for item in node.bucket:
                    item = list(item)
                    key = int(item[level])%(self.hash_key)
                    self.insert( node.children[key], value, level)
                return
            
            else:
                node.bucket[tuple(value)] = 0
                return
            
    
    def exists(self,value, node,level = 0 ):
        
        if not node.Leaf_status:
            key = int(value[level])%(self.hash_key)
            return self.exists(value, node.children[key], level+1)
        
        else:
            if value in node.bucket:
                node.bucket[value]+=1
                return True
            
        
        
def get_support_hashing(transactions, itemsets, k):
    support  = defaultdict(lambda: 0)

    support_tree = hash_tree(itemsets)
    
    count = 0
    for id, t in enumerate(transactions):
        for subset in combinations(t, k) :
            subset = tuple(sorted(subset, key = lambda v : int(v)))
            if support_tree.exists(subset, support_tree.root):
              support[subset]+=1
    return support

            
def get_support(transactions, itemsets):
    
    support  = defaultdict(lambda: 0)
    count = 0
    for id, t in enumerate(transactions):
        for itemset in itemsets:
            if t.issuperset(itemset):
                support[itemset]+=1
                count+=1
    return support

 
def get_frequent_itemsets(transactions, itemsets,  min_support_count, k):
    
    support_counts = get_support_hashing(transactions, itemsets, k)
    F_k = {}
    for itemset in itemsets:
        if(support_counts[itemset]>= min_support_count):
            F_k[itemset] = support_counts[itemset]
    return F_k


def get_apriori_candidate_itemsets(F_k_1, k):
    
    C_k = set()
    
    ## Candidate generation step using F[k-1]*F[k-1]
    for itemset_1 in F_k_1:
        for itemset_2 in F_k_1:
            itemset_1 = set(itemset_1)
            itemset_2 = set(itemset_2)
            #print(itemset_1,itemset_2)
            difference_1 = list(itemset_1.difference(itemset_2))
            difference_2 = list(itemset_2.difference(itemset_1))
            
            if((len(difference_1)==1 and len(difference_2))==1) :
               #and (int(difference_2[0])-int(difference_1[0]))>0):
                candidate = itemset_1.union(itemset_2)
                candidate = sorted(candidate, key = lambda v : int(v))
                #print(candidate)
                C_k.add(tuple(candidate))
    
    ##Pruning step
    ## list of candidates to prune
    r_k = set()
    
    #print(F_k_1)
    
    for candidate in C_k:
        for subset in combinations(candidate,k-1):
            if not subset in F_k_1:
                r_k.add(candidate)
                break
    
    
    for candidate in r_k:
        #print(candidate)
        C_k.remove(candidate)
        
    return list(C_k)
        
        
    
def frequent_itemsets_from_tranasactions(
        items: typing.Set,
        transactions: typing.List[set],
        min_support: float
        ):
    
    min_support_count = min_support* len(transactions)
    print("minimum support count is ", min_support_count)
    print("generating frequent itemsets")
    print("generating 1-itemsets")
    
    
    ##STEP-1 generating 1-itemsets
    C =  {}  ##candidate itemsets list of list of sets
    F = []  ##list of frequent itemsets
    F.append(None)
    frequent_itemsets = []
    
    ##generating C1
    c_temp = []
    
    for item in items:
        c_temp.append((item,))    
        
    C[1]= c_temp
    ##generating F1
     
    F_1 = get_frequent_itemsets(transactions, C[1], min_support_count, 1)
    print(len(F_1), F_1)
    F.append(F_1)
    ##STEP-2 loop
    
    k = 2
    while len(F[k-1]):
        print("generating",k ,"-itemsets")
        C[k] = get_apriori_candidate_itemsets(F[k-1], k)
        F_k = get_frequent_itemsets(transactions,C[k], min_support_count, k)
        F.append(F_k)
        k+=1
    return F
        
    