import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    ratings = pd.read_csv('title.ratings.tsv', sep='\t', low_memory=False)
    print("ratings 불러오기 완료")

    # ratings 테이블
    print("====ratings 테이블 생성 시작")
    conn.execute("""CREATE TABLE ratings (
        tconst varchar(20) not null, 
        averageRating float,
        numVotes int,
        PRIMARY KEY (tconst),
        FOREIGN KEY (tconst) REFERENCES movie (tconst)
        );""")
    for i in range(0, ratings.shape[0], 10000):
        ratings.iloc[i:i+10000].to_sql(name='ratings', con=db_connection,
                                       if_exists='append', index=False)
        print("%d/%d완료" % (i, ratings.shape[0]))
    print("ratings 테이블 생성 완료")
