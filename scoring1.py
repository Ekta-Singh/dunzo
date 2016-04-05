import pickle
import sys
import numpy as np
import operator
import gensim
from gensim import corpora, models, similarities


class getBrandSimilarity():
    def __init__(self):
        corpus=pickle.load(open('corpus_1.pickle','rb'))
        brandData=pickle.load(open('brandData.pickle','rb'))
        self.product_matrix=pickle.load(open('product_matrix.pickle','rb'))
        
        print 'All pickles loaded'
        
        [self.brandDict,self.indexBrand,self.brandIDName,self.brandIDCount]=brandData
       
        self.tfidf = models.TfidfModel(corpus)
        self.tfidf_product= self.tfidf[corpus]
        
        print 'tfidf created'

        self.lsi=models.LsiModel(corpus,num_topics=400)
        self.lsi_product=self.lsi[self.tfidf_product]
        
        print 'lsi created'
        
        self.index = similarities.MatrixSimilarity(self.lsi_product)
        self.index.num_best = 10
        
        print 'index created'
        
    def getBrandScoreLsi(self,brandID):
        brandSno=self.brandDict[brandID]
        lsi_query=self.lsi[self.tfidf_product[brandSno]]
        score=self.index[lsi_query]
        similaritylist=[]
        for item in score:
            similaritylist.append((self.brandIDName[self.indexBrand[item[0]]],item[1]))
        return similaritylist
    
    def getBrandsProductAssociation(self,brandID):
        brandSno=self.brandDict[brandID]
        similaritylist=[]
        sortedDict=sorted(self.product_matrix[brandSno].items(),key=operator.itemgetter(1),reverse=True)
        for item in sortedDict[:20]:
            similaritylist.append((self.brandIDName[self.indexBrand[item[0]]],item[1]))
        return similaritylist
    
    def getBrandScoreTfidf(self,brandID):
        brandSno=self.brandDict[brandID]
        score=self.index[self.tfidf_product[brandSno]]
        similaritylist=[]
        for item in score:
            similaritylist.append((self.brandIDName[self.indexBrand[item[0]]],item[1]))
        return similaritylist
    
if __name__=='__main__':
    bs=getBrandSimilarity()
    print bs.getBrandScoreLsi(23)
    print bs.getBrandsProductAssociation(23)   
    print bs.getBrandScoreTfidf(23)