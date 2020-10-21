# Data Scientist Python assignment

---

Python scripts for scraping movie ranking data from imdb.com website and Jupyter Notebook with some visualisations from the scraped data.

---

The funcionality is divided into two files `util.py` and `main.py`. 
 - `util.py` - Takes a imdb.com webpage of some kind of movie ranking and scrape the desired information (Title, Director, Actors, Release Year, Rating). Also creates the command line interface for the app. 
 - `main.py` - Script to take output (DataFrame) of the IMDB_scraper from util.py `util.py` and save it as `.csv` file. 
 
 `Visualisation.ipynb` is the Jupyter Notebook with some of the visualisations for the output DataFrame of the script. 
 
 ---
 
 ### Notes
 
  - The IMBD_scraper works not only on the top rated movies of all time page but on any page of IMDB movie rankings (like 'Most Popular Movies', 'Top Rated English Movies', 'Top Rated Indian Movies' etc.)
  - The Command Line interfece is associated with that. One can put the desired imdb webpage as an argument and create `.csv` file of different name that can be passed as other argument. 
  - There is also -movie argument for command line that will display the title and rating information of the movies based on its rank that was put as an argument
  
