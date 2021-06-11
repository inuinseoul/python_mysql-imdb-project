import sqlalchemy
import pymysql
import pandas as pd

db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
db_connection = sqlalchemy.create_engine(db_connection_str)
conn = db_connection.connect()

basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
print("basics 불러오기 완료")
akas = pd.read_csv('title.akas.tsv', sep='\t', low_memory=False)
akas.rename(columns={'titleId': 'tconst'}, inplace=True)
print("akas 불러오기 완료")

# akas 테이블
print("====akas 테이블 생성 시작")
myakas = akas.loc[:, ['tconst', 'ordering', 'title',
                      'region', 'language', 'isOriginalTitle']]
akastype = {'tconst': sqlalchemy.types.VARCHAR(20),
            'ordering': sqlalchemy.types.INTEGER(),
            'title': sqlalchemy.VARCHAR(200),
            'region': sqlalchemy.VARCHAR(10),
            'language': sqlalchemy.VARCHAR(10),
            'isOriginalTitle': sqlalchemy.BOOLEAN(),
            }
myakas.to_sql(name='akas', con=db_connection,
              if_exists='append', index=False, dtype=akastype)
print("삽입완료")
conn.execute('ALTER TABLE akas ADD PRIMARY KEY (tconst,ordering);')
print("설정완료")
print("akas 테이블 생성 완료")

# types 테이블
print("====types 테이블 생성 시작")
types = akas.loc[:, ['tconst', 'ordering']][akas.types != '\\N']
types['type'] = akas[akas.types != '\\N']['types'].str.split()
types = types.explode('type')

typestype = {'tconst': sqlalchemy.types.VARCHAR(20),
             'ordering': sqlalchemy.types.INTEGER(),
             'type': sqlalchemy.VARCHAR(50),
             }
types.to_sql(name='types', con=db_connection,
             if_exists='append', index=False, dtype=typestype)
print("삽입완료")
conn.execute('ALTER TABLE types ADD PRIMARY KEY (tconst,ordering,type);')
conn.execute(
    'ALTER TABLE types ADD FOREIGN KEY (tconst,ordering) REFERENCES akas (tconst,ordering);')
print("설정완료")
print("types 테이블 생성 완료")

# attributes 테이블
print("====attributes 테이블 생성 시작")
attributes = akas.loc[:, ['tconst', 'ordering']][akas.attributes != '\\N']
attributes['attribute'] = akas[akas.attributes !=
                               '\\N']['attributes'].str.split()
attributes = attributes.explode('attribute')

attributestype = {'tconst': sqlalchemy.types.VARCHAR(20),
                  'ordering': sqlalchemy.types.INTEGER(),
                  'attribute': sqlalchemy.VARCHAR(50),
                  }
attributes.to_sql(name='attributes', con=db_connection,
                  if_exists='append', index=False, dtype=attributestype)
print("삽입완료")
conn.execute(
    'ALTER TABLE attributes ADD PRIMARY KEY (tconst,ordering,attribute);')
conn.execute(
    'ALTER TABLE attributes ADD FOREIGN KEY (tconst,ordering) REFERENCES akas (tconst,ordering);')
print("설정완료")

print("attributes 테이블 생성 완료")
