import pickle
import sys
import numpy as np
import gensim
from gensim import corpora, models, similarities
import operator
import csv

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

brandData=pickle.load(open('brandData.pickle','rb'))
[brandDict,indexBrand,brandIDName,brandIDCount]=brandData
corpus=pickle.load(open('corpus_1.pickle','rb'))
product_matrix=pickle.load(open('product_matrix.pickle','rb'))

print 'pickles loaded'
'''
i=0
list=[]
f=open('product_association.csv','wb')
product_association=csv.writer(f)
for i in range(len(brandDict)):
    #brandSno=int(raw_input('Enter brand sno:'))
    sortedDict=sorted(product_matrix[i].items(),key=operator.itemgetter(1),reverse=True)
    for item in sortedDict[:11]:
        if item[0]==i:
            continue
        row=((brandIDName[indexBrand[i]],brandIDName[indexBrand[item[0]]],item[1]))
        product_association.writerow(row)
    i+=1


'''


tfidf = models.TfidfModel(corpus)
tfidf_product= tfidf[corpus]

lsi=models.LsiModel(corpus,num_topics=400)
lsi_product=lsi[tfidf_product]

index = similarities.MatrixSimilarity(tfidf_product)
index.num_best = 10

i=0
list=[]
f=open('tfidf_csv.csv','wb')
tfidf_csv=csv.writer(f)
for i in range(len(brandDict)):
    #score=index[lsi[tfidf_product[i]]] #lsi
    score=index[tfidf_product[i]] #tfidf
    list1=[]
    print i
    for item in score:
        if item[0]==i:
            continue
        row=((brandIDName[indexBrand[i]],brandIDName[indexBrand[item[0]]],item[1]))
        tfidf_csv.writerow(row)
    
    i+=1

    