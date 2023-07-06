from Univeristy_Data_Scrapper import scrape_data
from Text_Cleaning_Uni_Data import get_data_and_cleaned
from Degree_Name_Normalization import degree_name_normnalization
from Skill_Extraction_TK_API import Skill_extraction
from Baseline_Weightage_Frequency import frequency_weightage
from Graph_Cleaning_Filtering_to_Scope import filtering_degrees
from Annotation_Data_and_TFIDF import tfidf
from GPT_Prompting import prop
from Adding_Weightage_To_Graph import weighting
from Evaluation import eval

def main():
    # Step 1: Data collection and preprocessing
    dict_of_domains=[{"Title":"<title>(.+?)</title>", #regex for pulling the title of the page, which is the title of the program generally
                    "SearchPage":"https://en.uit.no/education", # course catalogue url
                    "Degreeregex":'tittel"><h2><a href="(.+?)"', # regex to pull individual degree urls
                    "Courseregex":'<a href="(https://(?:en.|)uit.no/utdanning/.*?/emne.+?)">', #regex  to pull individual courses URL in a program URL
                    "tracksregex":'<a href="(https://(?:en.|)uit.no/education/program.+?)">', ##regex  to pull individual specialization tracks URL in a program URL
                    "prog_desc":['(?s)<span>.*?Learning outcomes.*?</span>(.+?)<span>','(?s)<span>.*?Program description.*?</span>(.+?)<span>'],#regex  to pull broad program/specialization track description
                    "course_desc":'(?s)Course content.*?(.+?)Language',#regex  to pull individual course description in a program 
                    'CourseName':'<meta.*?description.*?content=(.+?)/>'}] #regex  to pull individual course name/title in a program 

    filename_out='ScrappedData/the arctic university of norway.json'

    print("Step : Data scraping")
    scrape_data(dict_of_domains,filename_out)

    print("Step : data cleaning")
    get_data_and_cleaned()

    # Step 2: Graph building and enrichment
    print("Step : Degree name normalization")
    degree_name_normnalization()

    print("Step : Skill extraction")
    Skill_extraction()

    print("Step : Baseline")
    frequency_weightage()

    print("Step : Filtering")
    filtering_degrees()

    print("Step : TFIDF")
    tfidf()

    print("Step : GPT prompting")
    prop()

    print("Step : Weightage of graph")
    weighting()

    # Step 3: Evaluation
    print("Step : Evaluation")
    eval()

if __name__ == "__main__":
    main()
