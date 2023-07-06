
import os
import openai
import os
import pandas as pd
import warnings
import time
import json
warnings.filterwarnings("ignore")


def prop():
    """
This code performs the following tasks:

1. Reading and Formatting Data:
   - Reads the annotated test dataset from 'tfidf_annote_data_test.csv' file.
   - Formats the dataset for readability and selects relevant columns.

2. Collecting Annotated Test Data:
   - Collects annotated test data from Excel files located in the 'testannotes' directory.
   - Appends the annotated data to the 'annote_data' dataframe.

3. Joining Dataset with Annotations:
   - Joins the 'annote_data' dataframe with the original data ('data1') based on specific columns.
   - Adds two new columns ('ans1' and 'ans12') to store the generated answers from GPT-3.5.

4. Prompting GPT-3.5 for Triple Style Prompt:
   - Iterates over each row in the dataframe and prompts GPT-3.5 for an answer using a triple style prompt.
   - The prompt includes the degree level, degree topic, and related skill.
   - The generated answer is stored in the 'ans1' column.

5. Prompting GPT-3.5 for Natural Language Style Prompt:
   - Iterates over each row in the dataframe and prompts GPT-3.5 for an answer using a natural language style prompt.
   - The prompt includes the degree level, degree topic, and related skill.
   - The generated answer is stored in the 'ans12' column.

6. Saving Results:
   - Saves the annotated dataset with generated answers as 'davinci_annotes_2.csv'.

7. TextRank Analysis:
   - Uses the spaCy library with the TextRank extension to calculate the TextRank scores of skills per degree.
   - Groups the data by degree topic and calculates the TextRank score for each skill within a topic.
   - Saves the dataset with TextRank scores as 'textrank_annotes_2.csv'.

Note: The code assumes the presence of the input files ('tfidf_annote_data_test.csv') in the current directory and the annotated files in the 'testannotes' directory. The results are saved as 'davinci_annotes_2.csv' and 'textrank_annotes_2.csv'.
"""

    #openai.api_key = os.getenv("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") # my key, dont use
    openai.api_key = "" # replace with openai key

    #read in data dn format for readability
    data=pd.read_csv('tfidf_annote_data_test.csv')  
    data1=data.iloc[:,[6,1,2,5,7]]

    # collect annotated test set
    annote_data=[]
    for filename in os.listdir(os.getcwd()+"\\testannotes"): # adjust path accordingly
        if filename.endswith(".xlsx"):
            #print(filename)
            data=pd.read_excel(os.path.join(os.getcwd()+"\\testannotes", filename))
            data=data.sort_values(by=['degree_topic','tfidf'],ascending=False,ignore_index=True )
            if len(annote_data)==0:
                annote_data=data
            else:
                annote_data=annote_data.append(data)

    #join dataset with annotations
    annote_data=annote_data.reset_index()
    annote_data=annote_data.sort_values(by=['degree_topic','tfidf'],ascending=False,ignore_index=True )
    d=annote_data.merge(data1, left_on=['degree_topic','degree_level','source_ignore','related_skill'], right_on=['degree_topic','degree_level','source_ignore','related_skill'])
    d['ans1']=''
    d['ans12']=''


    # prompting of GPT3.5 for triple style prompt
    exception=0
    while exception==0:
        try:
            for i in range(len(d)):
                if i%100==0:
                    #print(i)
                    pass
                if d.ans1[i]=='':
                    prompt="Q: "+d.degree_level[i]+" "+d.degree_topic[i]+" degree teaches "+d.related_skill[i]+": yes or no?\nA:"
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                    )
                    ans=json.loads(str(response))['choices'][0]['text']
                    d.ans1[i]=ans
            exception=1
        except:
            exception =0
            print('timeout')
            time.sleep(60)
        

    # prompting of GPT3.5 for natural language style prompt
    exception=0
    while exception==0:
        try:
            for i in range(len(d)):
                if i%100==0:
                    pass
                    #print(i)
                if d.ans12[i]=='':
                    prompt="Q: "+d.degree_level[i]+" level "+d.degree_topic[i]+" degree programs typically teaches "+d.related_skill[i]+"[yes, no, maybe]?\nA:"
                    response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=prompt,
                    temperature=0,
                    max_tokens=60,
                    top_p=1.0,
                    frequency_penalty=0.0,
                    presence_penalty=0.0
                    )
                    ans=json.loads(str(response))['choices'][0]['text']
                    d.ans12[i]=ans
            exception=1
        except:
            exception =0
            print('timeout')
            time.sleep(60)
        

    #save file
    d.to_csv("davinci_annotes_2.csv",index=False)



    data=pd.read_csv('davinci_annotes_2.csv') 


    import spacy
    #import pytextrank
    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("textrank")

    #find textrank score of skills per degree 
    w=set(data.degree_topic)
    fin=[]
    for item in w:
        temp=data[data.degree_topic==item].reset_index(drop=True)
        text='. '.join(temp.related_skill)
        doc = nlp(text)
        temp['textrank']=''
        for phrase in doc._.phrases:
            #print(temp[temp.related_skill==phrase.text]['textrank'])
            temp.loc[temp.related_skill==phrase.text,'textrank']=phrase.rank
        if len(fin)==0:
            fin=temp
        else:
            fin=fin.append(temp)
        
    #save data
    fin.to_csv("textrank_annotes_2.csv",index=False)




