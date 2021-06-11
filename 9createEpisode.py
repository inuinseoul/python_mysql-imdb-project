import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

episode = pd.read_csv('title.episode.tsv', sep='\t', low_memory=False)
print("episode 불러오기 완료")
basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
print("basics 불러오기 완료")

episode = pd.merge(episode, basics, left_on="parentTconst",
                   right_on="tconst", how="inner").loc[:, ['tconst_x', 'parentTconst', 'seasonNumber', 'episodeNumber']]
episode.rename(columns={'tconst_x': 'tconst'}, inplace=True)

# episode 테이블
print("====episode 테이블 생성 시작")
episodetype = {'tconst': sqlalchemy.types.VARCHAR(20),
               'parentTconst': sqlalchemy.types.VARCHAR(20),
               'seasonNumber': sqlalchemy.types.INTEGER(),
               'episodeNumber': sqlalchemy.types.INTEGER(),
               }
episode.to_sql(name='episode', con=db_connection,
               if_exists='append', index=False, dtype=episodetype)
print("삽입완료")
conn.execute(
    'ALTER TABLE episode ADD PRIMARY KEY (tconst);')
conn.execute(
    'ALTER TABLE episode ADD FOREIGN KEY (tconst) REFERENCES movie (tconst);')
conn.execute(
    'ALTER TABLE episode ADD FOREIGN KEY (parentTconst) REFERENCES movie (tconst);')
print("설정완료")
print("episode 테이블 생성 완료")
