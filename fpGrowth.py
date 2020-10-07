# -*- coding: utf-8 -*-
"""
Created on Sun Oct  4 09:18:54 2020

@author: ramak
"""

from collections import defaultdict
from tqdm import tqdm
from grocery_dat_cleaning import cate_to_num

class Node:
    
    def __init__(self, name, parent, count=1):
        self.name = name
        self.parent = parent
        self.support = count
        self.link = None
        self.children = {}
    
    def increase_support(self, count=1):
        self.support+=count

def insert(transaction, root, Table, count =1):
    if transaction[0] in root.children:
        root.children[transaction[0]].increase_support(count)
    
    else:
        root.children[transaction[0]] = Node(transaction[0], root, count)
        
        if Table[transaction[0]][1] ==None:
            Table[transaction[0]][1] = root.children[transaction[0]]
        else:
            update_link(Table[transaction[0]][1],root.children[transaction[0]])
    
    if len(transaction) > 1:
        insert(transaction[1::], root.children[transaction[0]],Table, count)

    
def update_link(Test_Node, Target_Node):
    while (Test_Node.link != None):
        Test_Node = Test_Node.link

    Test_Node.link = Target_Node
    
def get_items_support(transactions):
    items = defaultdict(lambda :0)
    for t, count in transactions.items():
        for item in t: 
            items[item]+=count
    
    return dict(sorted(items.items(), key = lambda v: v[1],reverse=True))
    

def sort_by_frequency(transactions, items):
    n_transactions = defaultdict(lambda:0)
    ##removing items with support less than minimum in transaction
    for t, count in transactions.items():
        n_t ={}
        for item in t:
           if item in items:
               n_t[item]=items.index(item)
                   
        n_t = dict(sorted(n_t.items(), key= lambda v: v[1]))
        n_transactions[tuple(n_t.keys())] += count
    

    
    return n_transactions
               

      
def create_FPTree(transactions, min_support_count):
    
    ##sorting items by frequency
    items = get_items_support(transactions)
    items_list = []
    Table = {}
    for item, support in items.items():
        if support >= min_support_count:
            items_list.append(item)
            Table[item]=[items[item],None]
    ##sorting transactions by frequency of itemsets
    transactions = sort_by_frequency(transactions, items_list)
    
    root = Node("root",None)
    for t in transactions:
        if len(t)>0:
            insert(t,root, Table, transactions[t])
    
    
   
    return root, Table

def _create_FPTree(transactions, min_support_count):
    
     ##sorting items by frequency
    items = get_items_support(transactions)
    items_list = []
    Table = {}
    for item, support in items.items():
        if support >= min_support_count:
            items_list.append(item)
            Table[item]=[items[item],None]
    ##sorting transactions by frequency of itemsets
    transactions = sort_by_frequency(transactions, items_list)
    
    root = Node("root",None)
    for t in transactions:
        if len(t)>0:
            insert(t,root, Table, transactions[t])
    
    
   
    return root, Table

def transveral(leaf_Node, prefixPath):
    if leaf_Node.parent != None:
        prefixPath.append(leaf_Node.name)
        transveral(leaf_Node.parent, prefixPath)
       

def find_prefix_path(basePat, TreeNode):
    Conditional_patterns_base = defaultdict(lambda: None)

    while TreeNode != None:
        prefixPath = []
        transveral(TreeNode, prefixPath)
        if prefixPath!=None and len(prefixPath) > 1:
            Conditional_patterns_base[frozenset(prefixPath[1:])] = TreeNode.support
        TreeNode = TreeNode.link

    return Conditional_patterns_base


def get_frequent(FPTree, HeaderTable, minSupport, prefix, frequent_itemset):
    bigL = [v[0] for v in sorted(HeaderTable.items(),key=lambda p: p[1][0])]
    for basePat in bigL:
        new_frequentset = prefix.copy()
        
        new_frequentset.add(basePat)


        frequent_itemset.append((new_frequentset))


        Conditional_pattern_bases = find_prefix_path(basePat, HeaderTable[basePat][1])

        Conditional_FPTree, Conditional_header = _create_FPTree(Conditional_pattern_bases,minSupport)
        
        if Conditional_header != None:
            get_frequent(Conditional_FPTree, Conditional_header, minSupport, new_frequentset, frequent_itemset)
            

def fp(filename, support, categorical = False):
    if not categorical:
        f = open(filename, "r")
    
        transactions =[]
        
        
        items = set()
        
        
        while True:
            line = f.readline()
            
            if not line:
                break
            transactions.append(tuple(sorted(line.split(), key = lambda v: int(v))))
            
            for item in line.split():
                items.add(item)
            
        
        items = sorted(items, key = lambda v : int(v))
        
        
        t = defaultdict(lambda : 0)
        
        for k in transactions:
            t[k] += 1
            
        support_count = len(transactions)*support
        tree, Table = create_FPTree(t, support_count)
        print("FP-tree Created")
        
        frequent_itemset = []
        get_frequent(tree,Table, support_count, set([]), frequent_itemset)
    
    else:
        
        transactions, items = cate_to_num(filename)
        t = defaultdict(lambda : 0)
        for k in transactions:
            t[tuple(k)] += 1
            
        support_count = len(transactions)*support
        tree, Table = create_FPTree(t, support_count)
        print("FP-tree Created")
        
        frequent_itemset = []
        get_frequent(tree,Table, support_count, set([]), frequent_itemset)
        itemsets = frequent_itemset
        ##convert to catergorical
        inv_map = {v: k for k, v in items.items()}
        n_itemsets = []
        

        for itemset in itemsets:
            k = []
            
            for item in itemset:
  
                k.append(inv_map[item])
            n_itemsets.append(k)   
        
        return n_itemsets
    
    
