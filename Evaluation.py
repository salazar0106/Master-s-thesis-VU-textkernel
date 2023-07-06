import pandas as pd
import warnings
warnings.filterwarnings("ignore")




def eval():
    """
This code performs the following tasks:

1. Reading Data:
   - Reads the weighted data from the 'weighted_data.csv' file.

2. Evaluating Data:
   - Initializes two additional columns ('weight_tfidf_' and 'weight_textrank_') with values from 'weight_y_ignore'.
   - Adjusts the weights based on TF-IDF and TextRank scores:
     - 'weight_tfidf_' is adjusted based on TF-IDF scores.
     - 'weight_textrank_' is adjusted based on TextRank scores.

3. evaluate_data() Function:
   - Calculates precision at different levels for a given column.
   - Groups the data by 'degree_topic' and sorts it in descending order of the specified column.
   - Iterates over each 'degree_topic' and calculates precision at different levels based on the 'is_degree_related_to_skill' column and the index.
   - Returns the precision values at different levels.

4. Evaluating Different Weight Combinations:
   - Evaluates precision for different weight combinations using the evaluate_data() function:
     - 'weight_tfidf_': TF-IDF + frequency weight.
     - 'tfidf': TF-IDF weight.
     - 'textrank': TextRank weight.
     - 'weight_textrank_': TextRank + frequency weight.
     - 'weight_new0': Prompts + frequency weight.
     - 'weight_new1': Prompts + frequency + TF-IDF weight.
     - 'weight_new2': Prompts + frequency + TF-IDF + TextRank weight.
     - 'weight_new3': Prompts + frequency + TextRank weight.
     - 'weight_new4': Prompts + frequency + TextRank + TF-IDF weight.

Note: The code assumes the presence of the input file ('weighted_data.csv') in the current directory.
"""

    #read data
    data=pd.read_csv('weighted_data.csv') 
    data['weight_tfidf_']=data['weight_y_ignore']
    data['weight_textrank_']=data['weight_y_ignore']

    # change weight according to tfidf score
    for i in range(len(data)):
        if data.tfidf[i]<0.1 :
            data.weight_tfidf_[i]=data.weight_tfidf_[i]/2
        if data.tfidf[i]>0.2:
            data.weight_tfidf_[i]=data.weight_tfidf_[i]*2


    # change weight according to textrank score
    for i in range(len(data)):
        if data.textrank[i]<0.05 :
            data.weight_textrank_[i]=data.weight_textrank_[i]/2
        if data.textrank[i]>0.1:
            data.weight_textrank_[i]=data.weight_textrank_[i]*2
    

    def evaluate_data(grouped_df,column):
        '''
        input dataframe: data: weights and values of different scores, prompts, degree names and clusters and skill names
        column: string: name of the column that should be taken as final weight for evaluation of graph
        output: df7,df10,df20,df30,df40: all int, each show precision at 7,10,20,etc for the dataframe for a particular column to be used as the final weight
        '''
        grouped_df=grouped_df.sort_values(by=['degree_topic',column],ascending=False,ignore_index=True )
        w=set(grouped_df.degree_topic)
        fin=[]
        for item in w:
            temp=grouped_df[grouped_df.degree_topic==item].reset_index(drop=True)
            temp=temp.reset_index()
            if len(fin)==0:
                fin=temp
            else:
                fin=fin.append(temp)

        fin=fin.reset_index(drop=True)
        #arranging by weight
        grouped_df7 = fin[fin["level_0"]<7].groupby(['degree_topic']).agg({'is_degree_related_to_skill': 'sum'})
        grouped_df10 = fin[fin["level_0"]<10].groupby(['degree_topic']).agg({'is_degree_related_to_skill': 'sum'})
        grouped_df20 = fin[fin["level_0"]<20].groupby(['degree_topic']).agg({'is_degree_related_to_skill': 'sum'})
        grouped_df30 = fin[fin["level_0"]<30].groupby(['degree_topic']).agg({'is_degree_related_to_skill': 'sum'})
        grouped_df40 = fin[fin["level_0"]<40].groupby(['degree_topic']).agg({'is_degree_related_to_skill': 'sum'})
        
        # finding precision
        df7=sum(grouped_df7.is_degree_related_to_skill)/len(fin[fin["level_0"]<7])
        df10=sum(grouped_df10.is_degree_related_to_skill)/len(fin[fin["level_0"]<10])
        df20=sum(grouped_df20.is_degree_related_to_skill)/len(fin[fin["level_0"]<20])
        df30=sum(grouped_df30.is_degree_related_to_skill)/len(fin[fin["level_0"]<30])
        df40=sum(grouped_df40.is_degree_related_to_skill)/len(fin[fin["level_0"]<40])
        #print(df7,df10,df20,df30,df40)
        return (df7,df10,df20,df30,df40)

    print("Precision at top 7 skills, top 10, top 20, 30, 40 :")
    
    print(evaluate_data(data,'weight_tfidf_'),'TFIDF+freq')
    #evaluate_data(data,'weight_tfidf_')

    print(evaluate_data(data,'tfidf'),'TFIDF')
    #evaluate_data(data,'tfidf')

    print(evaluate_data(data,'textrank'),'textrank')
    #evaluate_data(data,'textrank')
    print(evaluate_data(data,'weight_textrank_'),'textrank+freq')
    #evaluate_data(data,'weight_textrank_')

    # both gpt3 prompts +freq
    print(evaluate_data(data,'weight_new0'),'prompts +freq')

    #prompts+freq+tfidf
    print(evaluate_data(data,'weight_new1'),'prompts+freq+tfidf')

    #prompts+freq+tfidf+textrank
    print(evaluate_data(data,'weight_new2'),'prompts+freq+tfidf+textrank')

    #prompts+freq+textrank
    print(evaluate_data(data,'weight_new3'),'prompts+freq+textrank')

    #prompts+freq+textrank+tfidf
    print(evaluate_data(data,'weight_new4'),'prompts+freq+textrank+tfidf')
