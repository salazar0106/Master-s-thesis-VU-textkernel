#import csv
import pandas as pd
#import numpy as np
import warnings
import re
from sklearn.cluster import KMeans
warnings.filterwarnings("ignore")
from simcse import SimCSE

def degree_name_normnalization():
    '''
    This function performs degree name normalization using clustering techniques.
    It reads a CSV file containing degree names, cleans the names, converts them into word embeddings,
    and performs clustering using K-means algorithm. The resulting degree names along with their cleaned names
    and cluster labels are saved in a CSV file.

    Input: None
    Output: None
    '''

    model = SimCSE("princeton-nlp/sup-simcse-bert-base-uncased")
    data=pd.read_csv('data.csv',sep='|')  
    token_lists = data.DegreeName
    sentences = [''.join(text_list) for text_list in token_lists]

    #cleaning degree names
    sentences=list(sentences)
    clean_sent=[]
    for x in sentences:
        x=re.sub("([\(\[]).*?([\)\]])", ">", x)
        x= re.sub(r'\W+', ' ', x)
        for w in ['Catalogue des formations','bachelor','Programme','Oslo','Universiteit',' of ',' Cycle ','Minor','minor','Master','master','Prospectus','Honours','Bachelor','University','Leiden','UiT','EPFL' ,' in ' ,' and ']:
            x=x.replace(w, ' ')
        x=re.sub(r'\b\w{1,2}\b', '', x)
        x=x.strip()
        x=" ".join(x.split())
        clean_sent.extend([x])

    #converting text to word embeddings
    embeddings = model.encode(clean_sent)
    #Wclustering degree names
    kmeans = KMeans(290)
    documents = kmeans.fit(embeddings)

    percentile_list = pd.DataFrame(
        {'degree': sentences,
        'clean':clean_sent,
        'cluster': documents.labels_
        })


    percentile_list.to_csv("degree_name_clusters.csv",index=False)

'''
# run this to see how the K was chosen for clustering

from collections import Counter
c = Counter(percentile_list.cluster)
w=Counter(c.values())
w=sorted(w.items())
ind = []
fre = []
for item in w:
    ind.append(item[0])
    fre.append(item[1])
    
    
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score
from sklearn.metrics import calinski_harabasz_score

sil = []
dbscore = []
calscore = []
kmax = 450

for k in range(2, kmax+1):
    kmeans = KMeans(n_clusters = k).fit(embeddings)
    labels = kmeans.labels_
    sil.append(silhouette_score(embeddings, labels, metric = 'euclidean'))
    dbscore.append(davies_bouldin_score(embeddings, labels))
    calscore.append(calinski_harabasz_score(embeddings, labels))



import matplotlib.pyplot as plt
plt.plot(range(2, kmax+1), sil)
plt.xlabel('k')
plt.ylabel('score')
plt.show()



plt.plot(range(2, kmax+1), dbscore)
plt.xlabel('k')
plt.ylabel('score')
plt.show()



plt.plot(range(2, kmax+1), calscore)
plt.xlabel('k')
plt.ylabel('score')
plt.show()



sil = []
kmax = 300

for k in range(280, kmax+1):
    kmeans = KMeans(n_clusters = k).fit(embeddings)
    labels = kmeans.labels_
    sil.append(silhouette_score(embeddings, labels, metric = 'euclidean'))



plt.plot(range(280, kmax+1), sil)
plt.xlabel('k')
plt.ylabel('score')
plt.show()





'''