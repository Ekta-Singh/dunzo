__author__="Ekta.Singh"

import pandas as pd
import numpy as np
import sys
import pickle
from decimal import *
getcontext().prec = 3
from sklearn.preprocessing import normalize

'Import raw file'
raw_data=pd.read_table('brands_filtered.txt')

## Removing shopping instances with less than 2 product in set
temp_1=pd.DataFrame(raw_data.groupby('shopping_profile_id').size()).reset_index()
temp_1=temp_1.rename(columns={0:'shopping_size'})
raw_data_1=pd.merge(raw_data,temp_1,how='left',on='shopping_profile_id')
raw_data_2=raw_data_1[raw_data_1['shopping_size']>1]

## Removing brands with overall occurance less than 2 
#dict1=raw_data_2.brand_id.value_counts().to_dict()
#x=[brand_id for brand_id,value in dict1.iteritems() if value ==1]
#raw_data_3=raw_data_2[-raw_data_2.brand_id.isin(x)]

raw_data_3=raw_data_2

'Creating brandID to sno, sno to brandID, brandID to name, sno to count dictionaries'
i=0
brandDict={}
indexBrand={}
brandIDCount={}
for value, count in dict(raw_data_3.brand_id.value_counts()).iteritems():
    brandDict[value]=i
    brandIDCount[i]=count
    indexBrand[i]=value
    i+=1

brandIDName=pd.Series(raw_data.name.values,index=raw_data.brand_id).to_dict() #id to name
averageBrandCount=float(sum([count for sno,count in brandIDCount.iteritems()])/len(brandIDCount)) #average of all brand occurences

brandData=[brandDict,indexBrand,brandIDName,brandIDCount]

with open('brandData.pickle','wb') as p:
    pickle.dump(brandData,p)

    
'Getting all the brands corresponding to shopping instance in one row'
raw_data_4=raw_data_3.groupby(['shopping_profile_id']).agg({'brand_id':lambda x:list(x)})

'Creating product co-occurence dictionary for scoring'

#product_matrix=np.zeros((len(brandDict),len(brandDict)))

product_matrix=[dict() for x in range(len(brandDict))]
s=0
for index, row in raw_data_4.iterrows():
    s+=1
    #if s>4:
     #   break
    print s
    for brand1 in row['brand_id']:
        for brand2 in row['brand_id']:
            if  brandDict[brand2] in product_matrix[brandDict[brand1]]:
                product_matrix[brandDict[brand1]][brandDict[brand2]]+=Decimal(1)*10000/Decimal(brandIDCount[brandDict[brand2]])  # scaling basd on frequency of the brand
               
            else:
                product_matrix[brandDict[brand1]][brandDict[brand2]]=Decimal(1)/Decimal(brandIDCount[brandDict[brand2]])
               

#normalized_product_matrix_t=normalize(product_matrix, axis=0, norm='l1')
#normalized_product_matrix=normalize(normalized_product_matrix_t, axis=1, norm='l1')


'Corpus for tfidf scoring'
corpus=[]
for brand1 in product_matrix:
    temp=[]
    for brand2,value in brand1.iteritems():
        temp.append((brand2,value))
    corpus.append(temp)
    
with open('product_matrix.pickle','wb') as p:
    pickle.dump(product_matrix,p)
    
with open('corpus_1.pickle','wb') as p:
    pickle.dump(corpus,p)