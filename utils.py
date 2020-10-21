# Utils.py
from bs4 import BeautifulSoup
import requests
import pandas as pd
from numpy import arange
import re as re
import argparse


def optional_parser_arguments():
    """
    Function for adding all parameters that could be parsed on input of the program
    :param args_parser: object of ArgumentParses class for which the arguments are defined
    :return: Namespace object of arguments
    """
    opt_parser = argparse.ArgumentParser()
    opt_parser.add_argument("-url", type=str, default='http://www.imdb.com/chart/top')
    opt_parser.add_argument("-csv_name", type=str, default='Top_imdb_movies.csv')
    opt_parser.add_argument("-m", "--movie_rank", type=int, choices=range(1, 251),
                        help="display the name and rating of a movie based on its ranking")
    args = opt_parser.parse_args()
    return args


class IMDB_scraper:
    def get_the_movies(self):
        """
        Uses http://www.imdb.com/chart/top website to obtain the information within the <tr> tag
        Url parameter for the function could also be other movie ranking from the website like
        'Most Popular Movies' (http://www.imdb.com/chart/moviemeter), 'Top Rated English Movies'
        (http://www.imdb.com/chart/top-english-movies) or some other movie ranking of interest.
        However the goal is to scrape the 'Top Rated Movies' ranking, that's why the default
        url is http://www.imdb.com/chart/top
        :raise BaseException: if unexpected error happens
        :return tr: returns all the tr tags
        """
        # Get the information from the website
        args = optional_parser_arguments()
        movies_get = requests.get(args.url)
        if movies_get.status_code != 200:
            raise BaseException(
                f"Unexpected error while obtaining the website information\nCode: {movies_get.status_code} - {movies_get.text}")
        soup = BeautifulSoup(movies_get.text, 'lxml')
        # Get the information about the movies within <tr> tag
        tr = soup.find_all("tr")
        return tr

    @classmethod
    def scraping_info(cls, self):
        """
        Iteration over all the <tr> tag and appending wanted information about the movies
        (title, director, actors, year, rating)
        """
        tr = self.get_the_movies()
        title = []  # list to store the movie titles
        director = []  # list to store the name of directors
        actors = []  # list to store the name of actors
        year = []  # list to store the year of releases
        ratings = []  # list to store the movie ratings
        title_tag_info = re.compile(r"^(.*?)\(dir\.\)\,(.*?)$")  # compile regular expression to get the directors and actors
        # The iteration
        for movie in iter(tr):
            if movie.find('td') is not None:  # to not go through the first td tag witch is a None object
                title.append(movie.find('td', {'class': 'titleColumn'}).find('a').contents[0])
                title_tag_info_matched = re.match(title_tag_info,
                                                  movie.find('td', {'class': 'titleColumn'}).find('a')['title'])
                director.append(title_tag_info_matched.group(1).rstrip())
                actors.append(title_tag_info_matched.group(2).lstrip())
                year.append(
                    movie.find('td', {'class': 'titleColumn'}).find('span', {'class': 'secondaryInfo'}).contents[
                        0].strip('()'))
                if movie.find('td', {'class': 'ratingColumn imdbRating'}).find('strong') is not None: # in 'Most Popular Movie' ranking some movies do not have to have rakings
                    ratings.append(movie.find('td', {'class': 'ratingColumn imdbRating'}).find('strong').contents[0])
                else:
                    ratings.append(None)
        df = pd.DataFrame(
            {'Title': title, 'Director': director, 'Actors': actors, 'Release_Year': year, 'Rating': ratings})
        self.df = df


if __name__ == '__main__':
    args = optional_parser_arguments()
    if args.movie_rank is not None:
        obj = IMDB_scraper()
        IMDB_scraper.scraping_info(obj)
        df = obj.df
        df.index = arange(1, len(df) + 1)
        print(df.iloc[args.movie_rank - 1].loc[['Title', 'Rating']])
