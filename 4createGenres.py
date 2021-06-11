import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
print("basics 불러오기 완료")

# genres 테이블
print("====genres 테이블 생성 시작")
genres = basics.loc[:, ['tconst']]
genres['genre'] = basics['genres'].str.split(',')
genres = genres.explode('genre')

genrestype = {'tconst': sqlalchemy.types.VARCHAR(20),
              'genre': sqlalchemy.types.VARCHAR(20),
              }
genres.to_sql(name='genres', con=db_connection,
              if_exists='append', index=False, dtype=genrestype)
print("삽입완료")
conn.execute('ALTER TABLE genres ADD PRIMARY KEY (tconst,genre);')
conn.execute(
    'ALTER TABLE genres ADD FOREIGN KEY (tconst) REFERENCES movie (tconst);')
print("설정완료")
print("genres 테이블 생성 완료")
