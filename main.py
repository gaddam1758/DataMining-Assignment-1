# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 10:36:20 2020

@author: ramak
"""



from apriori import frequent_itemsets_from_tranasactions

from fpGrowth import create_FPTree, get_frequent
from collections import defaultdict

f = open("T10I4D100K.dat", "r")

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

#frequent_itemsets_from_tranasactions(items, transactions, 0.05)

t = defaultdict(lambda : 0)

for k in transactions:
    t[k] += 1
    

tree, Table = create_FPTree(t,5000)
print("FP-tree Created")

frequent_itemset = []
get_frequent(tree,Table, 5000, set([]), frequent_itemset)

print(frequent_itemset)


