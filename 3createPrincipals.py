import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

principals = pd.read_csv('title.principals.tsv', sep='\t', low_memory=False)
print("principals 불러오기 완료")

# principals 테이블
print("====principals 테이블 생성 시작")
principals = principals.iloc[:, 0:4]
principalstype = {'tconst': sqlalchemy.types.VARCHAR(20),
                  'ordering': sqlalchemy.types.INTEGER(),
                  'nconst': sqlalchemy.VARCHAR(20),
                  'category': sqlalchemy.VARCHAR(100),
                  }
principals.to_sql(name='principals', con=db_connection,
                  if_exists='append', index=False, dtype=principalstype)
print("삽입완료")
conn.execute('ALTER TABLE principals ADD PRIMARY KEY (tconst,ordering);')
print("설정완료")
print("principals 테이블 생성 완료")
