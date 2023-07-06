import pandas as pd
import warnings
warnings.filterwarnings("ignore")




def weighting():
    """
This code performs the following tasks:

1. Reading Data:
   - Reads the data from the 'textrank_annotes_2.csv' file.
   - Creates two additional columns ('ans1clean' and 'ans12clean') for storing cleaned versions of the generated answers.

2. Cleaning Generated Answers:
   - Cleans the 'ans1' and 'ans12' columns to have simple yes, no, or maybe values.
   - Updates the 'ans1clean' and 'ans12clean' columns with the cleaned values.

3. Weighting:
   - Initializes a new column 'weight_new' with the values from the 'weight_y_ignore' column.
   - Adjusts the weights based on the generated answers:
     - If 'ans1clean' is 'yes', the weight is doubled.
     - If 'ans12clean' is 'yes', the weight is doubled.
     - If 'ans1clean' is 'maybe', the weight remains unchanged.
     - If both 'ans1clean' and 'ans12clean' are 'no', the weight is set to 1.
     - If 'ans1clean' is 'no' and 'ans12clean' is 'maybe', the weight is halved.

4. Weighting based on TF-IDF and TextRank Scores:
   - Initializes new columns ('weight_new0', 'weight_new1', 'weight_new2', 'weight_new3', 'weight_new4') with values from 'weight_y_ignore'.
   - Adjusts the weights based on TF-IDF and TextRank scores:
     - 'weight_new0' remains unchanged based on 'ans1clean'.
     - 'weight_new1' is adjusted based on 'ans1clean' and TF-IDF scores.
     - 'weight_new2' is adjusted based on 'ans1clean' and TextRank scores.
     - 'weight_new3' is adjusted based on TextRank scores.
     - 'weight_new4' is adjusted based on TF-IDF scores.

5. Saving Results:
   - Saves the weighted data as 'weighted_data.csv'.

Note: The code assumes the presence of the input file ('textrank_annotes_2.csv') in the current directory. The weighted data is saved as 'weighted_data.csv'.
"""

    #read data in
    data=pd.read_csv('textrank_annotes_2.csv')
    data['ans1clean'] = data['ans1']
    data['ans12clean'] = data['ans12']

    #clean gpt3.5 prompting answer to simple yes, no, maybe
    data['ans1clean'] = data['ans1clean'].apply(lambda x: 'no' if x.lower().strip().startswith('no') else x)
    data['ans1clean'] = data['ans1clean'].apply(lambda x: 'maybe' if x.lower().strip().startswith('it') else x)
    data['ans1clean'] = data['ans1clean'].apply(lambda x: 'yes' if x.lower().strip().startswith('yes') else x)
    data['ans12clean'] = data['ans12clean'].apply(lambda x: 'no' if x.lower().strip().startswith('no') else x)
    data['ans12clean'] = data['ans12clean'].apply(lambda x: 'maybe' if x.lower().strip().startswith('maybe') else x)
    data['ans12clean'] = data['ans12clean'].apply(lambda x: 'yes' if x.lower().strip().startswith('yes') else x)


    data['weight_new']=data['weight_y_ignore']
    # change weight according to prompt ans
    for i in range(len(data)):
        if data.ans1clean[i]=='yes' :
            data.weight_new[i]=data.weight_new[i]*2
        if data.ans12clean[i]=='yes':
            data.weight_new[i]=data.weight_new[i]*2
        if data.ans1clean[i]=='maybe':
            data.weight_new[i]=data.weight_new[i]
        if data.ans1clean[i]=='no' and data.ans12clean[i]=='no':
            data.weight_new[i]=1
        if data.ans1clean[i]=='no' and data.ans12clean[i]=='maybe':
            data.weight_new[i]=data.weight_new[i]/2


    data['weight_new0']=data['weight_y_ignore']

    # change weight according to prompt ans
    for i in range(len(data)):
        if data.ans1clean[i]=='yes' :
            data.weight_new0[i]=data.weight_new0[i]*2
        if data.ans1clean[i]=='maybe':
            data.weight_new0[i]=data.weight_new0[i]
        if data.ans1clean[i]=='no':
            data.weight_new0[i]=1
        


    data['weight_new1']=data['weight_new0']

    # change weight according to tfidf score
    for i in range(len(data)):
        if data.tfidf[i]<0.1 :
            data.weight_new1[i]=data.weight_new1[i]/2
        if data.tfidf[i]>0.2:
            data.weight_new1[i]=data.weight_new1[i]*2
        

    # change weight according to textrank score
    data['weight_new2']=data['weight_new1']


    for i in range(len(data)):
        if data.textrank[i]<0.05 :
            data.weight_new2[i]=data.weight_new2[i]/2
        if data.textrank[i]>0.1:
            data.weight_new2[i]=data.weight_new2[i]*2
        



    data['weight_new3']=data['weight_new0']

    # change weight according to textrank score
    for i in range(len(data)):
        if data.textrank[i]<0.05 :
            data.weight_new3[i]=data.weight_new3[i]/2
        if data.textrank[i]>0.1:
            data.weight_new3[i]=data.weight_new3[i]*2
        


    data['weight_new4']=data['weight_new3']

    # change weight according to tfidf score
    for i in range(len(data)):
        if data.tfidf[i]<0.1 :
            data.weight_new4[i]=data.weight_new4[i]/2
        if data.tfidf[i]>0.2:
            data.weight_new4[i]=data.weight_new4[i]*2
    

    #save data
    data.to_csv("weighted_data.csv")
