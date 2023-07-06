import requests
import re
import json


# Dict_of_domains is a list of dictionaries. Each dictionary is a university page that needs to be scrapped. This means a studie guide page/ course catagologue
# an example for https://en.uit.no/education page has been shown below. each page has custome HTML that needs to be caliberated manually. 
# if there are multiple pages in the search of the university catalogue, they need to be added as seperate dicts in the list
# A txt file is provided for the regex used for each university for the thesis data in the folder outside. only static pages can be scrapped this way

dict_of_domains=[{"Title":"<title>(.+?)</title>", #regex for pulling the title of the page, which is the title of the program generally
                  "SearchPage":"https://en.uit.no/education", # course catalogue url
                  "Degreeregex":'tittel"><h2><a href="(.+?)"', # regex to pull individual degree urls
                 "Courseregex":'<a href="(https://(?:en.|)uit.no/utdanning/.*?/emne.+?)">', #regex  to pull individual courses URL in a program URL
                 "tracksregex":'<a href="(https://(?:en.|)uit.no/education/program.+?)">', ##regex  to pull individual specialization tracks URL in a program URL
                 "prog_desc":['(?s)<span>.*?Learning outcomes.*?</span>(.+?)<span>','(?s)<span>.*?Program description.*?</span>(.+?)<span>'],#regex  to pull broad program/specialization track description
                 "course_desc":'(?s)Course content.*?(.+?)Language',#regex  to pull individual course description in a program 
                 'CourseName':'<meta.*?description.*?content=(.+?)/>'}] #regex  to pull individual course name/title in a program 

filename_out='ScrappedData/the arctic university of norway.json'
def scrape_data(dict_of_domains,filename_out):
    '''
    input:dict_of_domains:list of dictionaries: regex in format shown above for each uni website

    output:filename_out:string: saves file with scarpped data at location given in filename_out
    '''
    # code to use the regex and iteratively pull all the text from the university page into a json list
    data=[]
    for uni in dict_of_domains: #for loop incase there are multiple pages in the uni search page
        reqy = requests.get(uni["SearchPage"]) # api request for data to search page
        text = reqy.text
        courses=[{"name":'','Desc':''}]
        
        for cp in re.findall(uni["Degreeregex"], text): # find all the degree urls
            dict_of_college={"DegreeURL":'',
                    "DegreeName":'',
                    "ProgDesc":'',
                    "Level":'',
                    "Courses":[],}
            cpreq = requests.get(cp) # get the text from each degree url
            cpreq = cpreq.text
            #print("=========")
            course=re.findall(uni["Title"], cpreq)[0] # title program
            Course_list=[]
            tracks_list=[]
            for pst in re.findall(uni["Courseregex"] ,    cpreq): # course urls
                Course_list.extend([pst])
            if len(Course_list)==0:
                for pst in re.findall(uni["tracksregex"] ,    cpreq):#specialization track urls
                    tracks_list.extend([pst])
            text2=''
            for patt in uni["prog_desc"]: # program desc text 
                progdes=re.findall(patt, cpreq)
                text2=text2+" ".join(progdes)
            ProgDesc=[]
            for x in re.findall('(?s)<p>(.+?)</p>', text2): # clean program text of html/white space
                ProgDesc.extend([re.sub('<[^>]+>', '', x)])
            # save data
            dict_of_college['DegreeURL']=cp
            dict_of_college['DegreeName']=course
            dict_of_college['ProgDesc']=' '.join(ProgDesc)
            if len(tracks_list)==0 and len(Course_list)==0: # continue next loop incase no tracks/ courses detected.
                continue
            elif len(tracks_list)!=0 and len(Course_list)==0:# treat ewach track like a program desc if exists, and add back to main program
                for u in tracks_list:
                    text = requests.get(u).text
                    course=re.findall(uni["Title"], text)[0]
                    Course_list=[]
                    for pst in re.findall(uni["Courseregex"] ,    text):
                        Course_list.extend([pst])
                    for u in Course_list:
                        Courses={'name':'',"desc":'','track':''}
                        text = requests.get(u.split('" ')[0]).text
                        text2=re.findall(uni["course_desc"], text)
                        if len(text2)==0: # check for empty text issues
                            text2=["EMPTY PAGE"]
                        CourseName=re.findall(uni["CourseName"], text)
                        CourseDesc=re.sub('<[^>]+>', ' ', text2[0])
                        CourseDesc=re.sub('\n', ' ', CourseDesc)
                        Courses['name']=CourseName
                        Courses['desc']=CourseDesc
                        Courses['track']=course
                        dict_of_college['Courses'].extend([Courses])
                
            elif len(Course_list)!=0: # pull course data
                for u in Course_list:
                    Courses={'name':'',"desc":'','track':''}
                    
                    text = requests.get(u.split('" ')[0]).text
                    text2=re.findall(uni["course_desc"], text)
                    if len(text2)==0:
                        text2=["EMPTY PAGE"]
                    CourseName=re.findall(uni["CourseName"], text)
                    CourseDesc=re.sub('<[^>]+>', ' ', text2[0])
                    CourseDesc=re.sub('\n', ' ', CourseDesc)
                    Courses['name']=CourseName
                    Courses['desc']=CourseDesc
                    Courses['track']=""
                    dict_of_college['Courses'].extend([Courses])
            data.extend([dict_of_college])
            #print(dict_of_college)
   

    # save data to name of univeristy, needs to be adjusted each time manually
    with open(filename_out, 'w') as f:
        json.dump(data, f)

