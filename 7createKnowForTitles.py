import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
print("basics 불러오기 완료")
name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
print("name_basics 불러오기 완료")

# knownForTitles 테이블
print("====knownForTitles 테이블 생성 시작")
knownForTitles = name_basics.loc[:, ['nconst']
                                 ][name_basics.knownForTitles != '\\N']
knownForTitles['knownForTitle'] = name_basics[name_basics.knownForTitles !=
                                              '\\N']['knownForTitles'].str.split(',')
knownForTitles = knownForTitles.explode('knownForTitle')
knownForTitles = pd.merge(knownForTitles, basics, left_on="knownForTitle",
                          right_on="tconst", how="inner").loc[:, ['nconst', 'knownForTitle']]
directorstype = {'tconst': sqlalchemy.types.VARCHAR(20),
                 'knownForTitle': sqlalchemy.types.VARCHAR(20),
                 }
knownForTitles.to_sql(name='knownForTitles', con=db_connection,
                      if_exists='append', index=False, dtype=directorstype)
print("삽입완료")
conn.execute(
    'ALTER TABLE knownForTitles ADD PRIMARY KEY (nconst,knownForTitle);')
conn.execute(
    'ALTER TABLE knownForTitles ADD FOREIGN KEY (nconst) REFERENCES person (nconst);')
conn.execute(
    'ALTER TABLE knownForTitles ADD FOREIGN KEY (knownForTitle) REFERENCES movie (tconst);')
print("설정완료")
print("knownForTitles 테이블 생성 완료")
