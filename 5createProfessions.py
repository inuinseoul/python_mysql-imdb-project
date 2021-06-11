import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
print("name_basics 불러오기 완료")

# personProfessions 테이블
print("====personProfessions 테이블 생성 시작")
personProfessions = name_basics.loc[:, ['nconst']]
personProfessions['primaryProfession'] = name_basics['primaryProfession'].str.split(
    ',')
personProfessions = personProfessions.explode('primaryProfession')

personProfessionstype = {'tconst': sqlalchemy.types.VARCHAR(20),
                         'primaryProfession': sqlalchemy.types.VARCHAR(20),
                         }
personProfessions.to_sql(name='personProfessions', con=db_connection,
                         if_exists='append', index=False, dtype=personProfessionstype)
print("삽입완료")
conn.execute(
    'ALTER TABLE personProfessions ADD PRIMARY KEY (nconst,primaryProfession);')
conn.execute(
    'ALTER TABLE personProfessions ADD FOREIGN KEY (nconst) REFERENCES person (nconst);')
print("설정완료")
print("personProfessions 테이블 생성 완료")
