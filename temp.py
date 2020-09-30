# -*- coding: utf-8 -*-
"""
Created on Wed Sep 30 19:56:56 2020

@author: ramak
"""

from itertools import chain, combinations


def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    
    s = list(iterable)
    a = []
    for r in range(1,len(s)):
        for k in combinations(s,r):
            a.append(k)
    
    return a 

s = {0, 1, 2, 3}

print(powerset(s))