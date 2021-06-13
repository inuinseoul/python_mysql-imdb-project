import sqlalchemy
import pandas as pd


def start():
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
    personProfessions = personProfessions.dropna(axis=0)

    conn.execute("""CREATE TABLE personProfessions (
        nconst varchar(20) not null, 
        primaryProfession varchar(70) not null,
        PRIMARY KEY (nconst,primaryProfession),
        FOREIGN KEY (nconst) REFERENCES person (nconst)
        );""")
    for i in range(0, personProfessions.shape[0], 10000):
        personProfessions.iloc[i:i+10000].to_sql(name='personProfessions', con=db_connection,
                                                 if_exists='append', index=False)
        print("%d/%d완료" % (i, personProfessions.shape[0]))
    print("personProfessions 테이블 생성 완료")
