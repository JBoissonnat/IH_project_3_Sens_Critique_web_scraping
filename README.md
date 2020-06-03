# Ironhack project 3 Sens Critique web scraping

![GitHub Logo](https://lh3.googleusercontent.com/aNkgNYxslBB27VYsfcbzXYcSRcTmUcLIK_HUeovpXSNprkjnxguSJQc263yMybkoChg)

### Project description

The goal of this project was to create a database for movies on the french website "Sens Critique", gathering informations such as title, director, actors, genre, year, budget, users ratings...

The scraping was made using the libraries requests and BeatifulSoup, and not by calling the Sens Critique API since it didn't provided all the informations about movies that were wanted. It is possible with the code to ask a specific number of movie pages to be scraped (knowing that 1 page = 16 movies).

The main structure of the code could be adapted to other categories of the website such as music, video games or books...

### Libraries

- requests
- BeautifulSoup (from bs4)
- time
- re (regex)
- pandas
- dateparser

### Code details

Functions for the code :
- create_request(), which uses and url to get content from the pages
- check_empty_list()
- addition_lists()
- get_links(), which ask the user the number of pages to scrap and scrap their url
- get_main_info() and get_details_info(), which respectively gets the main and details informations for a movie page (the page is different between the 2 functions)
- movie_dataframe(), which creates an empty dataframe for the movies
- fill_movie_dataframe(), which loops over the list of movies pages links to scrap each and fill the dataframe using the get_main_info
- convert_cc_interest(), convert_length(), convert_date() which respectively convert properly the informations about "coup de coeur" and interest, length and date of the movies
- wrangle_df(), which uses the convert functions to clean and and handle properly the dataframe

Eventually the code return a cleaned dataframe with 22 columns of informations about each movies scraped

### Links

Source page : https://www.senscritique.com/search?categories[0][0]=Films

Presentation : https://docs.google.com/presentation/d/1l8lPo4fnwpWrHODu7AtQ5Ll7oOY7anr0wbk8jU_hiGQ/edit?usp=sharing
