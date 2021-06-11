from os import name
import sqlalchemy
import pymysql
import pandas as pd

# db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
# db_connection = sqlalchemy.create_engine(db_connection_str)
# conn = db_connection.connect()

# ratings = pd.read_csv('title.ratings.tsv', sep='\t', low_memory=False)
# print("ratings 불러오기 완료")
basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
print("basics 불러오기 완료")
# akas = pd.read_csv('title.akas.tsv', sep='\t', low_memory=False)
# akas.rename(columns={'titleId': 'tconst'}, inplace=True)
# print("akas 불러오기 완료")
# crew = pd.read_csv('title.crew.tsv', sep='\t', low_memory=False)
# print("crew 불러오기 완료")
episode = pd.read_csv('title.episode.tsv', sep='\t', low_memory=False)
print("episode 불러오기 완료")
# principals = pd.read_csv('title.principals.tsv', sep='\t', low_memory=False)
# print("principals 불러오기 완료")
# name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
# print("name_basics 불러오기 완료")

print(episode)
episode = pd.merge(episode, basics, left_on="parentTconst",
                   right_on="tconst", how="inner").loc[:, ['tconst_x', 'parentTconst', 'seasonNumber', 'episodeNumber']]
episode.rename(columns={'tconst_x': 'tconst'}, inplace=True)
print(episode)
