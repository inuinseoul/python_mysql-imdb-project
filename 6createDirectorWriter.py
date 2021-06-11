import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

crew = pd.read_csv('title.crew.tsv', sep='\t', low_memory=False)
print("crew 불러오기 완료")
name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
print("name_basics 불러오기 완료")

# directors 테이블
print("====directors 테이블 생성 시작")
directors = crew.loc[:, ['tconst']][crew.directors != '\\N']
directors['director'] = crew[crew.directors !=
                             '\\N']['directors'].str.split(',')
directors = directors.explode('director')
directors = pd.merge(directors, name_basics, left_on="director",
                     right_on="nconst", how="inner").loc[:, ['tconst', 'director']]

directorstype = {'tconst': sqlalchemy.types.VARCHAR(20),
                 'director': sqlalchemy.types.VARCHAR(20),
                 }
directors.to_sql(name='directors', con=db_connection,
                 if_exists='append', index=False, dtype=directorstype)
print("삽입완료")
conn.execute(
    'ALTER TABLE directors ADD PRIMARY KEY (tconst,director);')
conn.execute(
    'ALTER TABLE directors ADD FOREIGN KEY (tconst) REFERENCES movie (tconst);')
conn.execute(
    'ALTER TABLE directors ADD FOREIGN KEY (director) REFERENCES person (nconst);')
print("설정완료")
print("directors 테이블 생성 완료")

# writers 테이블
print("====writers 테이블 생성 시작")
writers = crew.loc[:, ['tconst']][crew.writers != '\\N']
writers['writer'] = crew[crew.writers != '\\N']['writers'].str.split(',')
writers = writers.explode('writer')
writers = pd.merge(writers, name_basics, left_on="writer",
                   right_on="nconst", how="inner").loc[:, ['tconst', 'writer']]
writerstype = {'tconst': sqlalchemy.types.VARCHAR(20),
               'writer': sqlalchemy.types.VARCHAR(20),
               }
writers.to_sql(name='writers', con=db_connection,
               if_exists='append', index=False, dtype=writerstype)
print("삽입완료")
conn.execute(
    'ALTER TABLE writers ADD PRIMARY KEY (tconst,writer);')
conn.execute(
    'ALTER TABLE writers ADD FOREIGN KEY (tconst) REFERENCES movie (tconst);')
conn.execute(
    'ALTER TABLE writers ADD FOREIGN KEY (writer) REFERENCES person (nconst);')
print("설정완료")
print("writers 테이블 생성 완료")
