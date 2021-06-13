import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    print("basics 불러오기 완료")

    # genres 테이블
    print("====genres 테이블 생성 시작")
    genres = basics.loc[:, ['tconst']]
    genres['genre'] = basics['genres'].str.split(',')
    genres = genres.explode('genre').dropna(axis=0)

    conn.execute("""CREATE TABLE genres (
        tconst varchar(20) not null, 
        genre varchar(20) not null,
        PRIMARY KEY (tconst,genre),
        FOREIGN KEY (tconst) REFERENCES movie (tconst)
        );""")
    for i in range(0, genres.shape[0], 10000):
        genres.iloc[i:i+10000].to_sql(name='genres', con=db_connection,
                                      if_exists='append', index=False)
        print("%d/%d완료" % (i, genres.shape[0]))
    print("genres 테이블 생성 완료")
