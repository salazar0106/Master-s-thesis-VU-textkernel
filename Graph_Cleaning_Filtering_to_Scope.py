import pandas as pd
import sys 
import numpy as np
np.set_printoptions(threshold=sys.maxsize)
import warnings
warnings.filterwarnings("ignore")


def filtering_degrees():
    """
    This code filters and assigns levels to the degree programs based on the degree names in the graph dataset. It performs the following tasks:
     Filters out soft skill and language category skills from the graph dataset and assigns levels to the degree programs based on what level degree it is, and saves it to the dataframe.
    """
    #read data dand filter out soft skill and language category skills
    data=pd.read_csv('data_graph.csv')
    data=data[data.category!='Soft Skill']
    data=data[data.category!='Language'].reset_index(drop=True)
    #print(data.head())
    data['level']=''

    data1=data

    #find level of degree based on degree name
    for i in range(len(data1)):
        if data1.level[i]=='':
            name=data1.name[i].lower()

            if 'master' in name:
                data1.level[i]='Master'

            elif 'bachelor' in name:
                data1.level[i]='Bachelor'

            elif 'minor' in name:
                data1.level[i]='minor'

            elif 'major' in name:
                data1.level[i]='major'

            elif 'honours' in name:
                data1.level[i]='honours'

            elif 'ph.d' in name:
                data1.level[i]='PhD'
            
            elif 'phd' in name:
                data1.level[i]='PhD'

            elif 'exchange' in name:
                data1.level[i]='exchange'

            elif 'certification' in name:
                data1.level[i]='certification'
            
            elif 'diploma' in name:
                data1.level[i]='diploma'
            
            elif 'program' in name:
                data1.level[i]='program'

            else:
                data1.level[i]=''


    #save data
    data1.to_csv('data_graph_level2.csv',index=False)




