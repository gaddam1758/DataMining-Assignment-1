from apriori import apriori

from eclat import eclat

from fpGrowth import fp

import matplotlib.pyplot as plt

import os

import time 

import numpy as np
import matplotlib.pyplot as plt
from memory_profiler import memory_usage

Datasets = os.listdir('data')


times = []



support = 0.1
times = []
scale =100
categorical = False
for file in Datasets:
    t = []
    if file == 'groceries.csv':
      categorical = True
    else:
         categorical = False
    print("running on dataset", file)
    
    t1 = time.time()
    
    print("apriori")
    
    apriori("data/"+file,support, categorical)
    
    t.append(time.time()-t1)
    
    t1 = time.time()
    
    print("eclat")
    
    eclat("data/"+file,support, categorical)
    
    t.append(time.time()-t1)
    
    t1 = time.time()
    print("fp")
    
    fp("data/"+file, support, categorical)
    
    t.append(time.time()-t1)
    times.append(t)

##dataset profile


def cate_plot(data, labels):
    X = np.arange(len(data[0]))
    fig = plt.figure()
    ax = fig.add_axes([0,0,1,1])
    ax.bar(X + 0.00, data[0], color = 'b', width = 0.25)
    ax.bar(X + 0.25, data[1], color = 'g', width = 0.25)
    ax.bar(X + 0.50, data[2], color = 'r', width = 0.25)
    ax.set_ylabel('log10(time)')
    ax.set_title('Time taken by algirithm on various datasets')
    ax.set_xticks(X)
    ax.set_xticklabels(labels, rotation = 45)
    ax.legend(labels=['apriori', 'eclat', 'fp'])

import numpy as np
import math




X = Datasets

print(times)
t = np.log10(np.array(times)*scale).T.tolist()
print(t)

cate_plot(t, Datasets)
plt.savefig('figures/'+'time_dataset'+str(support)+".png",bbox_inches='tight')
plt.show()