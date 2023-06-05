import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import ast
import re
# from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
# from markupsafe import escape, soft_str
from nltk.corpus import stopwords

# get Indonesian stopword 
list_stopwords = set(stopwords.words('indonesian'))

# fact = StemmerFactory()
# stemmer = fact.create_stemmer()

class Recommendation():
    def __init__(self,dataframe,user_input):
        self.tfidfvec = TfidfVectorizer()
        self.dataframe = self.prepare_dataframe(dataframe)
        self.user_input = user_input
                
    def prepare_dataframe(self,dataframe):
        self.dataframe = pd.read_json(dataframe,orient='records')
        self.dataframe['cosim'] = 0
        self.dataframe['tags'] = self.dataframe['tags'].apply(lambda x: ' '.join(ast.literal_eval(x)))
        self.dataframe['text'] = self.dataframe['title']+' '+self.dataframe['summary']+' '+self.dataframe['content'] + ' ' + self.dataframe['tags']
        # self.dataframe.drop(['title','summary','content','tags','imgUrl','link','viewers','likes','createdAt','author'],axis=1,inplace=True)
        self.dataframe['text'] = self.dataframe['text'].apply(lambda x: self.clean_text(x))
        return self.dataframe
    
    def clean_text(self,text):
        self.text = text.lower()
        self.text = self.text.strip()
        self.text = re.sub('[^a-z ]','',self.text)
        self.text = ' '.join([word for word in self.text.split(' ') if not word in list_stopwords])
        self.text = self.text.strip()
        return self.text
    
    def recomendations(self):
        self.vector = self.tfidfvec.fit_transform(self.dataframe['text']).toarray()
        self.user_input = self.clean_text(self.user_input)
        self.vector_user = self.tfidfvec.transform([self.user_input]).toarray()
        self.cos_sim = cosine_similarity(self.vector,self.vector_user)
        self.dataframe['cosim'] = self.cos_sim
        if np.max(self.dataframe['cosim'])<=0.001:
            return self.dataframe.sample(self.dataframe.shape[0]).drop(['text', 'cosim'],axis=1)
        return self.dataframe.sort_values('cosim',ascending=False).drop(['text', 'cosim'],axis=1)

        #     return self.dataframe.sample(self.dataframe.shape[0])[['id', 'title', 'imgUrl', 'author', 'link']]
        # return self.dataframe.sort_values('cosim',ascending=False)[['id', 'title', 'imgUrl', 'author', 'link']]