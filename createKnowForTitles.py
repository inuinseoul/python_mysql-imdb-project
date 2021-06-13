import sqlalchemy
import pandas as pd


def start():
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

    conn.execute("""CREATE TABLE knownForTitles (
        nconst varchar(20) not null, 
        knownForTitle varchar(20) not null,
        PRIMARY KEY (nconst,knownForTitle),    
        FOREIGN KEY (nconst) REFERENCES person (nconst),
        FOREIGN KEY (knownForTitle) REFERENCES movie (tconst)
        );""")
    print("start!")
    for i in range(0, 17130681, 10000):
        knownForTitles.iloc[i:i+10000].to_sql(name='knownForTitles', con=db_connection,
                                              if_exists='append', index=False)
        print("%d 완료" % i)
    print("knownForTitles 테이블 생성 완료")
