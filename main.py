# main.py
from utils import IMDB_scraper
from utils import optional_parser_arguments
from numpy import arange


def get_df():
    obj = IMDB_scraper()
    IMDB_scraper.scraping_info(obj)
    df = obj.df
    return df


df = get_df()
args = optional_parser_arguments()
df.index = arange(1, len(df) + 1)
df.to_csv(args.csv_name, index=True, index_label='Rank', encoding='utf-8-sig')
