
from cleantext import clean
import os
import re
import json
import pandas as pd
import sys 
import numpy
numpy.set_printoptions(threshold=sys.maxsize)


def clean_data(text):
    '''
    input: string - text: 
    
    This function takes in text in english to be cleaned - scrapped from univeristy websites. It removed anything between brackets
    it removes urls, emails and phone numbers. It removed punctuation line breaks. it fixes any unicode character issues 
    and changes everything to ASCII coding. 
    
    output: String - text:
    '''
    text=clean(text=text,fix_unicode=True,to_ascii=True,lower=False,no_line_breaks=True,no_urls=True,no_emails=True,
               no_phone_numbers=True,no_numbers=False,no_digits=False,no_currency_symbols=False,no_punct=True,
               replace_with_url="<URL>",replace_with_email="<EMAIL>",replace_with_phone_number="<PHONENO>",lang="en")
    text=re.sub("[\(\[\{}].*?[\)\]\}]", "",  text)
    text=re.sub("[;]", "",  text)
    return text

def get_data_and_cleaned():
    '''
        This function reads scraped data from JSON files in the "ScrappedData" directory and cleans the text data.
        It converts the cleaned data into a CSV file with each course of each program as an individual entry in the CSV.

        Input: None
        Output: None
    '''
    # clean all the text desc data from all universities in data folder, and turn into a single CSV
    raw_uni_data=[]
    for filename in os.listdir(os.getcwd()+"/ScrappedData"):
        if filename.endswith(".json"):
            #print(filename)
            with open(os.path.join(os.getcwd()+"/ScrappedData", filename), 'r') as f:
                data=json.load(f)
                raw_uni_data.extend(data)

    raw_uni_data=pd.DataFrame(raw_uni_data)
    # turn csv of jsons for each university, into csv of each course of each program, being an individual entry in CSV
    data=raw_uni_data.explode('Courses').reset_index(drop=True)
    data.Courses = data.Courses.fillna({i: {} for i in data.index})
    data1= pd.concat([data.drop('Courses', axis=1), pd.DataFrame(data['Courses'].tolist())], axis=1)
    data1['clean_desc'] = data1['desc'].apply(lambda x: clean_data(x))
    data1['clean_ProgDesc'] = data1['ProgDesc'].apply(lambda x: clean_data(x))

    #this is only for sample data, actual; data is given in folder above with the name data.csv
    data1.to_csv("data(1).csv", sep='|', encoding='utf-8')

