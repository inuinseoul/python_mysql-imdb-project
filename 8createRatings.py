import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

ratings = pd.read_csv('title.ratings.tsv', sep='\t', low_memory=False)
print("ratings 불러오기 완료")

# ratings 테이블
print("====ratings 테이블 생성 시작")
ratingstype = {'tconst': sqlalchemy.types.VARCHAR(20),
               'averageRating': sqlalchemy.types.FLOAT(),
               'numVotes': sqlalchemy.types.INTEGER(),
               }
ratings.to_sql(name='ratings', con=db_connection,
               if_exists='append', index=False, dtype=ratingstype)
print("삽입완료")
conn.execute(
    'ALTER TABLE ratings ADD PRIMARY KEY (tconst);')
conn.execute(
    'ALTER TABLE ratings ADD FOREIGN KEY (tconst) REFERENCES movie (tconst);')
print("설정완료")
print("ratings 테이블 생성 완료")
