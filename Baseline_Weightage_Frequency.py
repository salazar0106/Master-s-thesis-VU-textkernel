import json
import pandas as pd
import ast


def frequency_weightage():
    '''
    This code performs frequency weightage analysis on university program and course descriptions that have been enriched with extracted skills. It calculates the weight of each skill based on its frequency within each program and saves the results as a graph dataset.
    - frequency_weightage(): Performs frequency weightage analysis on skills extracted from program and course descriptions.
   '''
    #read data into correct format
    data=pd.read_csv('data_withskills2.csv')  
    data['skills'] = data['skills'].apply(lambda x:json.loads(ast.literal_eval(x)))
    data['skills_prog'] = data['skills_prog'].apply(lambda x:json.loads(ast.literal_eval(x)))

    # read cluster data
    data_clust=pd.read_csv('degree_name_clusters.csv')  
    data_clust.columns=['DegreeName', 'clean', 'cluster']
    #join data
    d=data.merge(data_clust, on='DegreeName', how='inner', suffixes=('_1', '_2'))
    data=d

    # calculate baseline weight based on frequency of skills per program
    source=[]
    target=[]
    edge=[]
    for i in range(len(data)):

        try:
            
            if data.iloc[i].desc!='ALL' and  pd.isna(data.iloc[i].desc)==False:
                degname=data.iloc[i].DegreeName
                degnameclean=data.iloc[i].clean
                cluster1=data.iloc[i].cluster
                for j in range(len(data.iloc[i].skills['skills'])):
                    skill_name=data.iloc[i].skills['skills'][j]['description']
                    skill_perc=data.iloc[i].skills['skills'][j]['confidence']
                    skill_cat=data.iloc[i].skills['skills'][j]['category']

                    source.extend([cluster1])
                    target.extend([skill_name])
                    edge.extend([{'confidence':skill_perc,'category':skill_cat,'weight':1,'name':degname,'clean':degnameclean}])
            
        except:
            pass
        
    #convert data to correct format
    kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':edge})
    kg_df1 = kg_df['edge'].apply(pd.Series)
    kg_df = pd.concat([kg_df1, kg_df], axis = 1)

    #save data
    kg_df.to_csv('data_graph.csv',index=False)

