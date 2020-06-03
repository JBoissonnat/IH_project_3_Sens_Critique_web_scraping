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

### Links

Source page : 
Presentation : 
