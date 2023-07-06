# Master-s-thesis-VU-textkernel

# University Program and Course Data Extraction and Analysis

**Project Context**

The project focuses on leveraging Natural Language Processing (NLP) techniques to improve the quality of degree skill relationships in the context of talent management and recruitment processes. The aim is to create a knowledge graph that connects degrees, skills, and professions, enabling better matching of fresh graduates with job opportunities.

The project is conducted in collaboration with Textkernel (TK), a company that specializes in parsing and analyzing resumes and job descriptions. TK already has a well-curated knowledge graph that supports their resume parser, consisting of professions and skills with their interconnections. The project aims to extend this graph by incorporating degrees as a new node entity, associating relevant skills with each degree.

To achieve this, the project involves collecting and processing data from university course catalogues, extracting information about degree programs and the skills taught in each program. The collected data is then used to enrich the knowledge graph, creating connections between degrees, skills, and professions.

The project faces challenges such as the variability in format and structure of course catalogues, requiring meticulous preprocessing and extraction techniques. Additionally, the time and resource limitations of the project necessitate exploring alternative approaches, like semi-automated labeling, to overcome manual data collection and annotation challenges.

The research question guiding the project is: "Which methods can help improve the quality of degree skill relationships by leveraging university curricula and course descriptions?" The project follows a pipeline that includes data collection and annotation, graph building/enrichment, and evaluation stages.

By improving the matching of fresh graduates' skills with job opportunities, the project aims to enhance TK's candidate matching system, providing suggestions for courses to candidates who lack specific skills required for their desired jobs. This supports the professional growth of fresh graduates and strengthens organizations' workforce by attracting and retaining top talent.

The project contributes to the fields of HRM and NLP by demonstrating the potential of NLP techniques in talent management and recruitment processes. The successful implementation of the proposed system can pave the way for further research and applications in these areas.





This repository contains a set of scripts for extracting, cleaning, and analyzing data from university program and course descriptions. The scripts automate the process of scraping data from university websites, cleaning the text, extracting skills, clustering degree names, and evaluating the weights of skills based on TF-IDF and TextRank scores.

The following sections provide an overview of each script and its functionality.

## 1. Univeristy_Data_Scrapper.py

This script is used to scrape data from university study guide pages or course catalogues. It takes in a list of dictionaries, `dict_of_domains`, where each dictionary represents a university page that needs to be scraped. Each dictionary contains regex patterns and the URL of the page to scrape. The script uses regular expressions to extract specific information such as program titles, degree URLs, course URLs, specialization track URLs, program descriptions, and course descriptions. The extracted data is saved in JSON format.

## 2. Text_Cleaning_Uni_Data.py

This script reads the scraped data from JSON files, performs cleaning operations on the text, and saves the cleaned data in a CSV file. The `clean_data()` function applies various cleaning operations such as removing content between brackets, URLs, emails, and phone numbers, punctuation, line breaks, digits, and fixing Unicode character issues. The `get_data_and_cleaned()` function processes the scraped data and converts it into a cleaned CSV file.

## 3. Degree_Name_Normalization.py

This script performs clustering and normalization of degree names extracted from the cleaned data. It uses the SimCSE model and K-means clustering to cluster similar degree names together. The resulting clusters and normalized degree names are saved in a CSV file.

## 4. Skill_Extraction_TK_API.py

This script uses the Textkernel Skill Service API to extract skills from program and course descriptions. It reads the cleaned data from the CSV file, prepares the data, and extracts skills using the Skill Service API. The extracted skills are stored in a new column in the dataset, and the results are saved in a new CSV file.

## 5. Baseline_Weightage_Frequency.py

This script performs frequency weightage analysis on the enriched dataset containing program and course descriptions along with extracted skills. It calculates the weight of each skill based on its occurrence within each program. The analysis involves joining the data with a degree name cluster dataset, extracting relevant information from each row, and generating records for each skill within a program. The resulting dataset represents a graph structure with nodes representing clusters and skills, and edges representing the weight and additional attributes. The final graph dataset is saved for further analysis and visualization.

## 6. Graph_Cleaning_Filtering_to_Scope.py

This script filters out skills categorized as 'Soft Skill' and 'Language' from the graph dataset, which represents a network of skills associated with different degree programs. The filtered dataset is then processed to assign levels to the degree programs based on their names. The code iterates through each degree program, examines the degree name for specific keywords, and assigns a corresponding level to the program. The updated dataset with assigned degree levels is saved for further analysis.

## 7. Annotation_Data_and_TFIDF.py

This script performs TF-IDF analysis on a dataset that contains degree programs and their related skills. It preprocesses the data by cleaning the degree names and related skills, filters out unrelated skills, and clusters the degrees based on specific clusters. The script computes TF-IDF scores for each skill within a degree topic using the TF-IDF vectorizer from scikit-learn. It creates a test dataset by selecting specific clusters and saves the results for annotation purposes, along with the complete dataset with TF-IDF scores.

## 8. GPT_Prompting.py

This file takes a long time to run depending on your API access in openAPI. To run this, make an account in openAI, and add your API key to the code

This script uses GPT-3.5 to generate answers for a given dataset using both triple style prompts and natural language style prompts. The generated answers are stored in a dataframe. Additionally, it uses spaCy with the TextRank extension to calculate the TextRank scores for skills within each degree topic. The results are saved in a separate CSV file.

## 9. Adding_Weightage_To_Graph.py

This script applies weights to the data based on generated answers, TF-IDF scores, and TextRank scores. The weighted data is saved in a CSV file.

## 10. Evaluation.py

This script reads the weighted data, adjusts weights based on TF-IDF and TextRank scores, and evaluates precision at different levels for various weight combinations. The precision values are printed for each weight combination.

Please run these scripts in the specified order to perform the complete data extraction and analysis pipeline. Make sure to provide the necessary inputs and modify the scripts as required for your specific use case.