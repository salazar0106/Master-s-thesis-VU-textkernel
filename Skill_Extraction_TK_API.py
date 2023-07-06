#download the required skill service as per Textkernel documentation
#get_ipython().run_line_magic('pip', 'install tokenizer --trusted-host registry-01.p.nl01.textkernel.net --index-url http://registry-01.p.nl01.textkernel.net:8081/repository/pypi-du/simple')



import pandas as pd
import csv
#import numpy as np
import shlex
import subprocess
import string
import sys
csv.field_size_limit(sys.maxsize)
import warnings
warnings.filterwarnings("ignore")


def Skill_extraction():
    """
    This code extracts skills from university program and course descriptions using the Textkernel skill extraction service. It reads a CSV file containing cleaned data, including program and course descriptions. The extracted skills are added as new columns in the dataset and saved to a new CSV file.

    Performs degree name normalization by cleaning and clustering degree names using embeddings.
    Extracts skills from program and course descriptions using the Textkernel skill extraction service.
    Cleans the text data by removing unnecessary characters, URLs, emails, phone numbers, and punctuation.
    Saves the cleaned dataset with extracted skills to a new CSV file.
    Note: The code assumes the availability of the Textkernel skill extraction service and requires internet connectivity to interact with the API.
    """

    #read in cleaned data
    data=pd.read_csv('data.csv',encoding='utf-8',delimiter='|')  
    data.drop(['Unnamed: 0'],axis=1,inplace=True)
    data=data.dropna(subset=['clean_desc', 'clean_ProgDesc'], how='all')
    data = data.fillna('')
    data=data.reset_index(drop=True)

    #get skills for each set of texts in broad program description
    data['skills_prog']=''
    for i in range(len(data)):
        
        text=data.clean_ProgDesc[i]
        if type(text) != str: #ignore entry if text is blank/ not string
            #print(text)
            break

        for punctuation in string.punctuation:
            text = text.replace(punctuation, '')
        cmd = '''curl -X POST "http://kube-lb-b.t.nl02.textkernel.net/parsing/skills/v1/extract" -H "Content-Type: application/json" -d '{ "text": "'''+text+'''", "language": "en", "threshold": 0.5 }' '''
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        data.skills_prog[i]=str(stdout)

    #get skills for each set of texts in course description
    data['skills']=''
    for i in range(len(data)):
        
        text=data.clean_desc[i]
        if type(text) != str:
            #print(text)
            break
        for punctuation in string.punctuation:
            text = text.replace(punctuation, '')
        cmd = '''curl -X POST "http://kube-lb-b.t.nl02.textkernel.net/parsing/skills/v1/extract" -H "Content-Type: application/json" -d '{ "text": "'''+text+'''", "language": "en", "threshold": 0.5 }' '''
        args = shlex.split(cmd)
        process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        data.skills[i]=str(stdout)



    #data cleaning
    data=data.dropna(subset=['clean_desc', 'clean_ProgDesc'], how='all').reset_index(drop=True)
    data = data.fillna('')
    data=data[data["DegreeName"].str.contains("page not found",case=False) == False]
    data=data.reset_index(drop=True)

    data.to_csv('data_withskills2 - 1.csv',encoding='utf-8',index=False)

