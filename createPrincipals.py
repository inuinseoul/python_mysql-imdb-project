import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    principals = pd.read_csv('title.principals.tsv',
                             sep='\t', low_memory=False)
    print("principals 불러오기 완료")

    # principals 테이블
    print("====principals 테이블 생성 시작")
    principals = principals.iloc[:, 0:4]
    conn.execute("""CREATE TABLE principals (
        tconst varchar(20) not null, 
        ordering int not null,
        nconst varchar(20) not null, 
        category varchar(100),
        PRIMARY KEY (tconst,ordering)
        );""")
    for i in range(0, principals.shape[0], 10000):
        principals.iloc[i:i+10000].to_sql(name='principals', con=db_connection,
                                          if_exists='append', index=False)
        print("%d/%d완료" % (i, principals.shape[0]))
    print("principals 테이블 생성 완료")
