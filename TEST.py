import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

# ratings = pd.read_csv('title.ratings.tsv', sep='\t', low_memory=False)
# print("ratings 불러오기 완료")
# basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
# print("basics 불러오기 완료")
akas = pd.read_csv('title.akas.tsv', sep='\t', low_memory=False)
akas.rename(columns={'titleId': 'tconst'}, inplace=True)
print(akas)
# crew = pd.read_csv('title.crew.tsv', sep='\t', low_memory=False)
# print("crew 불러오기 완료")
# episode = pd.read_csv('title.episode.tsv', sep='\t', low_memory=False)
# print("episode 불러오기 완료")
# principals = pd.read_csv('title.principals.tsv', sep='\t', low_memory=False)
# print("principals 불러오기 완료")
# name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
# print("name_basics 불러오기 완료")

# merge_df = pd.merge(basics, episode, left_on='tconst',
#                     right_on='tconst', how='left')
# print(merge_df)

# dtypesql = {'tconst': sqlalchemy.types.VARCHAR(20),
#             'averageRating': sqlalchemy.types.FLOAT(),
#             'numVotes': sqlalchemy.INTEGER(),
#             }
# ratings.to_sql(name='title_ratings', con=db_connection,
#             if_exists='append', index=False, dtype=dtypesql)
# print("삽입완료")
# conn.execute('ALTER TABLE title_ratings ADD PRIMARY KEY (tconst);')
# print("설정완료")
