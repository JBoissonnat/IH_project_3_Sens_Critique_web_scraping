# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 02:52:13 2020

@author: jeanb
"""

import requests as r
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import dateparser

### FUNCTIONS

def create_request(url):
    request = r.get(url).content
    return BeautifulSoup(request)

def check_empty_list(lst):
    if len(lst)== 0:
        lst.append(float("nan"))
    return lst

def addition_lists(lst_of_lst):
    
    added = []
    
    for lst in lst_of_lst:
        check_empty_list(lst)
        added.append(lst[0])
        
    return added

def get_links():
    
    ran = int(input("How many movies pages do you want to scramble data from ? (1 page = 16 movies) ? : "))
    
    links_main = []
    links_details = []
    
    for i in range(1,ran+1):
        
        soup = create_request(f"https://www.senscritique.com/search?categories[0][0]=Films&p={i}")

        base_link = 'div.search__StyledResultsColumn-sc-1mr42vn-4.igWMhV  a[href*="film/"]'

        links_main_temp = [re.findall(r'"(.*?)"', str(j))[0] for j in soup.select(base_link)]
        
        links_main += links_main_temp
        
        links_details_temp = [k+"/details" for k in links_main_temp]
        
        links_details += links_details_temp
        
        time.sleep(2)
        
    return links_main, links_details
    
#links_main, links_details = get_links()

def get_main_info(links_main, i):
    
    main_soup = create_request(links_main[i])
    
    sc_id = [links_main[i].split("/")[-1]]
    
    name = [i.text.strip() for i in main_soup.select('div.pvi-hero-overlay h1')]
    
    cc = [[i.text.strip() for i in main_soup.select('b[class="pvi-stats-number"]')][0]]
    
    interest = [[i.text.strip() for i in main_soup.select('b[class="pvi-stats-number"]')][1]]
    
    glob_rating = [i.text.strip() for i in main_soup.select('span.pvi-scrating-value')]
    
    original_title = [i.text.strip() for i in main_soup.select('div.pvi-hero-overlay h2')]
    
    ratings_per_rate = [i.text.split() for i in main_soup.select('ol[class="elrg-graph product"]')]
    
    total_ratings = [sum([int(i) for i in ratings_per_rate[0]])]
    
    key = ["1","2","3","4","5","6","7","8","9","10"] ; values = ratings_per_rate[0]
    ratings_per_rate = [dict(zip(key,values))]
    
    description = [i.text.strip() for i in main_soup.select('p.pvi-productDetails-resume')]
    
    top_10 = [i.text.strip() for i in main_soup.select('span.pvi-tops10-value1')]
    
    #review = ["".join(re.findall(r'(\d)',str(i.text))) for i in main_soup.select('h5.d-heading2-opt')]
    #review = ["".join(re.findall(r'(\d)',str(i.text))) for i in main_soup.select('div.d-heading-opt')][1]
    #review = ["".join(re.findall(r'(\d)',("".join([str(i.text) for i in main_soup.select('div.d-heading-opt')]))))]
    review = [(re.findall(r'\(\d.*?\)',str(i.text))) for i in main_soup.select('div.d-heading-opt:contains("Critiques : avis d")')][0]
    review = [review[0].strip("()")]
    
    lst_info_main = [sc_id, name, cc, interest, glob_rating, original_title, ratings_per_rate, total_ratings, description,
                top_10, review]
    
    main_info = addition_lists(lst_info_main)
    
    return main_info
    
    
#main_info = get_main_info(links_main, 1)

def get_details_info(links_details, i):
    
    details_soup = create_request(links_details[i])
    
    main_actors = [[i.text for i in details_soup.select('div.d-rubric-inner span[itemprop="name"]')]]
    
    adding_actors = [[i.text for i in details_soup.select('table[class="pde-data"] a')]]
    
    real = [i.text.strip() for i in details_soup.select('h3.d-heading-opt:contains("Réalisateurs")+div ')]
    
    scenar = [[i.text.strip() for i in details_soup.select('h3.d-heading-opt:contains("Scénaristes")+table.d-rubric a ')]]
    
    distrib = [i.text.strip() for i in details_soup.select('h3.d-heading-opt:contains("Distributeurs")+table.d-rubric a ')]
    
    length = [i.text for i in details_soup.select('h4:contains("Durée")+span')]
    
    genre = [i.text.split() for i in details_soup.select('h4:contains("Genre")+ul')]
    
    fr_release = [" ".join(i.text.split()) for i in details_soup.select('h4:contains("française")+span')]
    
    original_release = [" ".join(i.text.split()) for i in details_soup.select('h4:contains("origine")+span')]
    
    budget = [" ".join(i.text.split()) for i in details_soup.select('h4:contains("Budget")+span')]
    
    origine_country = [i.text.split() for i in details_soup.select('h4:contains("origine")+ul')]
    
    lst_info_details = [main_actors, adding_actors, real, scenar, distrib, length, genre, fr_release,
                original_release, budget, origine_country]
    
    details_info = addition_lists(lst_info_details)

    return details_info

#details_info = get_details_info(links_details, 1)

#full_data = main_info+details_info

def movie_dataframe():
    
    columns = ["sc_id","name","cc","interest","glob_rating","original_title","ratings_per_rate","total_ratings","description",
           "top_10","review","main_actors","adding_actors","real","scenar","distrib","length","genre",
           "fr_release","original_release","budget","origine_country"]
    
    df = pd.DataFrame(columns=columns)
    
    return df

#df = movie_dataframe()

def fill_movie_dataframe(df, links_main, links_details):
    
    for i in range(len(links_main)):
    
        main_info = get_main_info(links_main, i)
        
        details_info = get_details_info(links_details, i)
        
        full_data = main_info+details_info
        
        df.loc[len(df), :] = full_data
        
        time.sleep(2)
        
    return df
    
#df_filled = fill_movie_dataframe(df, links_main, links_details)

def convert_cc_interest(string):
    
    if len(re.sub("[^A-Z]", "", string)) == 0:
        return int(string)
    
    elif "." in string:
        string+="00"
    else:
        string+="000"
        
    string = re.sub("[.K]","",string)
    
    return int(string)

def convert_length(string):
    
    string = re.sub("[min ]","",string)
    
    string = string.split("h")
    
    if string[1] == "":
        string.remove("")
    
    string = [int(e) for e in string]
    
    string[0] = string[0]*60
    
    string = sum(string)
    
    return string

def convert_date(string):
    
    if string == "error_year":
        
        return string

    elif string != "error_year":

        date = dateparser.parse(string).date()

        return str(date)

def wrangle_df(df):
    
    df.cc = df.cc.apply(lambda x : convert_cc_interest(x))
    df.interest = df.interest.apply(lambda x : convert_cc_interest(x))
    
    df.length = df.length.apply(lambda x : convert_length(x))
    
    df.fr_release = df.fr_release.fillna("error_year")
    df.fr_release = df.fr_release.apply(lambda x : convert_date(x))
    
    df.original_release = df.original_release.fillna("error_year")
    df.original_release = df.original_release.apply(lambda x : convert_date(x))
    
    return df
    
if __name__=="__main__":
    links_main, links_details = get_links()
    df = movie_dataframe()
    df = fill_movie_dataframe(df, links_main, links_details)
    df_wrangled = wrangle_df(df)
    
#limite : pas de cleaning de la colonne budget

#string = float("nan")

#convert_date(string)
