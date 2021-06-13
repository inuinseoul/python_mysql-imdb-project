import sqlalchemy
import pandas as pd


def start():
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

    conn.execute("""CREATE TABLE directors (
        tconst varchar(20) not null,
        director varchar(20) not null,
        PRIMARY KEY (tconst,director),
        FOREIGN KEY (tconst) REFERENCES movie (tconst),
        FOREIGN KEY (director) REFERENCES person (nconst)
        );""")
    for i in range(0, directors.shape[0], 10000):
        directors.iloc[i:i+10000].to_sql(name='directors', con=db_connection,
                                         if_exists='append', index=False)
        print("%d/%d완료" % (i, directors.shape[0]))
    print("삽입완료")
    print("directors 테이블 생성 완료")

    # writers 테이블
    print("====writers 테이블 생성 시작")
    writers = crew.loc[:, ['tconst']][crew.writers != '\\N']
    writers['writer'] = crew[crew.writers != '\\N']['writers'].str.split(',')
    writers = writers.explode('writer')
    writers = pd.merge(writers, name_basics, left_on="writer",
                       right_on="nconst", how="inner").loc[:, ['tconst', 'writer']]
    conn.execute("""CREATE TABLE writers (
        tconst varchar(20) not null,
        writer varchar(20) not null,
        PRIMARY KEY (tconst,writer),
        FOREIGN KEY (tconst) REFERENCES movie (tconst),
        FOREIGN KEY (writer) REFERENCES person (nconst)
        );""")
    for i in range(2400000, writers.shape[0], 10000):
        writers.iloc[i:i+10000].to_sql(name='writers', con=db_connection,
                                       if_exists='append', index=False)
        print("%d/%d완료" % (i, writers.shape[0]))
    print("writers 테이블 생성 완료")
