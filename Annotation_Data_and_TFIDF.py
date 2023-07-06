import re
import pandas as pd 
import numpy as np
import warnings
warnings.filterwarnings("ignore")


def tfidf():
    """
    This code performs TF-IDF (Term Frequency-Inverse Document Frequency) analysis on a dataset of degree programs and related skills. It carries out the following tasks:
    - tfidf(): Reads the input data, preprocesses it, performs TF-IDF analysis, and saves the results.
    """


    #read in data
    data=pd.read_csv('data_graph_level2.csv')  

    '''#data=data.drop_duplicates().reset_index(drop=True)

    token_lists = data.name
    sentences = [''.join(text_list) for text_list in token_lists]
    #sentences=set(sentences)

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


    percentile_list = pd.DataFrame(
        {'degree': sentences,
        'clean':clean_sent
        })
    '''

    #join all data into one csv file to build annotation data set arranged by desc frequency of skills within a program
    grouped_df = data.groupby(['clean', 'target','level']).agg({'weight': 'sum'})
    grouped_df = grouped_df.reset_index()
    data2=pd.merge(data, grouped_df,  how='left', left_on=['clean','target','level'], right_on = ['clean','target','level'])
    data2=data2.sort_values(by=['source','clean','weight_y'],ascending=False,ignore_index=True )
    data2=data2.drop('confidence', axis=1)
    data2=data2.drop_duplicates().reset_index(drop=True)

    #some basic data cleaning to remove skills picked up from noisy data like teaching methods/ html
    # filter data to only master's / bachelores level
    data2.to_csv('annotes_data_all.csv',index=False)
    data3=data2.loc[:,[ 'clean','level', 'target', 'category','source','weight_y','name']]
    data3.columns=[ 'degree_topic','degree_level', 'related_skill', 'is_degree_related_to_skill','cluster_ignore','weight_y_ignore','source_ignore']
    data3['is_degree_related_to_skill']=''
    data4 =np.where((data3['degree_level']=="Bachelor") | (data3['degree_level']== "Master") )
    data4=data3.loc[data4].reset_index(drop=True)
    data5 =np.where( (data4['related_skill'] != "Research Skills") &(data4['related_skill'] != "Teaching") &
                (data4['related_skill'] != "Presentations") &(data4['related_skill'] != "Rubric") &
                (data4['related_skill'] != "Carrying out Assessments") &(data4['related_skill'] != "Heart Rate") &
                    (data4['related_skill'] != "Final Grades") &(data4['related_skill'] != "Telecommunications") &
                    (data4['related_skill'] != "Writing of Reports") &(data4['related_skill'] != "Literature") &(data4['related_skill'] != "Help Desk") &
                (data4['related_skill'] != "Web Pages") &(data4['related_skill'] != "Social Media") )
    data5=data4.loc[data5].reset_index(drop=True)
    cluster=list(set(data5.cluster_ignore))

    y=[]
    for x in cluster:
        z=list(set(data5[data5.cluster_ignore==x].degree_topic))
        k=(min(z, key=len))
        y.extend([{'cluster':x,'names':z,'topic':k}])
        
    cluster_names = pd.DataFrame(y)
    data6=pd.merge(data5, cluster_names,  how='left', left_on=['cluster_ignore'], right_on = ['cluster'])
    data6=data6.iloc[:,[9,1,2,3,4,6]].drop_duplicates().reset_index(drop=True)
    data7=[]
    for x in cluster_names.topic:
        
        z=pd.DataFrame(data6.loc[data6.topic==x])
        z=z.drop_duplicates(subset=['related_skill'])
        if len(data7)==0:
            data7=z.reset_index(drop=True)
        else :
            data7 = data7.append(z, ignore_index=True)
        
    data7['degree_topic']=data7['topic']
    data7=data7.iloc[:,0:7]

    # clean skill names
    df=[]
    for x in set(data7.degree_topic):
        z=data7.loc[data7.degree_topic==x]
        z.related_skill=z['related_skill'].apply(lambda x: re.sub('[^0-9a-zA-Z]', '_', x))
        z.related_skill=z['related_skill'].apply(lambda x: '_'.join(x.strip().split()))
        w=' '.join(z.related_skill)
        df.extend([{'degree':x,'skills':w}])
        

    from sklearn.feature_extraction.text import TfidfVectorizer
    # tfidf of skills added as a column
    df = pd.DataFrame(df)
    #print(df.head())
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_separate = tfidf_vectorizer.fit_transform(df["skills"])

    df_tfidf = pd.DataFrame(
        tfidf_separate.toarray(), columns=tfidf_vectorizer.get_feature_names_out(), index=df.index
    )

    df_tfidf['degree']=df['degree']

    data7['tfidf']=''
    for i in range(len(data7)):
        related_skill=re.sub('[^0-9a-zA-Z]', '_', data7.related_skill[i])
        related_skill= '_'.join(related_skill.lower().strip().split())
        data7.tfidf[i]=float(df_tfidf[df_tfidf.degree==data7.degree_topic[i]][related_skill])

    # dev data set clusters
    w={'Archaeology Research',
    'Architecture',
    'Artificial Intelligence',
    'Arts Literature Media',
    'Bio Pharmaceutical Sciences',
    'Biology',
    'Business Studies',
    'Cyber Security',
    'Ecology',
    'Economics',
    'Education Child Studies',
    'English Language Culture',
    'International Studies',
    'Law',
    'Marketing',
    'Mathematics',
    'Medicine',
    'Music Communication Technology',
    'Physics program',
    'Psychology'}

    #test data set clusters
    w2={'Chemical Engineering',
    'Astronomy',
    'History Ancient History',
    'Public Health',
    'Archaeology World Archaeology',
    'Linguistics',
    'International Relations Culture Politics',
    'Finance',
    'Bio Pharmaceutical Sciences Industrial Pharmacy',
    'Geosciences',
    'Civil engineering',
    'History',
    'Robotics',
    'Chemistry',
    'Digital Humanities',
    'Law the Sea',
    'Mathematical Statistics',
    'Computational Science',
    'Renewable Energy Systems',
    'Sustainable Management Technology'}

    # pull test set clusters
    data8=data7[data7['degree_topic'].isin(w2)]

    #save for annotation as a csv per cluster of degrees
    for x in data8.degree_topic:
        z=pd.DataFrame(data8.loc[data8.degree_topic==x])#.drop_duplicates().reset_index(drop=True)
        z.to_csv('DataToAnnote/annotes_data1_'+x+'.csv',index=False)

    #complete dataset  
    data7.to_csv('tfidf_data.csv',index=False)

    # test dataset full
    data8.to_csv('tfidf_annote_data_test.csv',index=False)

