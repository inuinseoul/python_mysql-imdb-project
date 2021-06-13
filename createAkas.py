import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    akas = pd.read_csv('title.akas.tsv', sep='\t', low_memory=False)
    akas.rename(columns={'titleId': 'tconst'}, inplace=True)
    print("akas 불러오기 완료")

    # akas 테이블
    print("====akas 테이블 생성 시작")
    myakas = akas.loc[:, ['tconst', 'ordering', 'title',
                          'region', 'language', 'isOriginalTitle']].dropna(axis=0)
    myakas['isOriginalTitle'] = myakas.isOriginalTitle.replace({"\\N": -1})

    conn.execute("""CREATE TABLE akas (
        tconst varchar(20) not null,
        ordering int not null,
        title text,
        region varchar(10),
        language varchar(10),
        isOriginalTitle int,
        PRIMARY KEY (tconst,ordering)
        );""")
    myakas1 = myakas.iloc[0:10000000]
    myakas1.to_sql(name='akas', con=db_connection,
                   if_exists='append', index=False)
    print("1차 성공")
    myakas2 = myakas.iloc[10000000:20000000]
    myakas2.to_sql(name='akas', con=db_connection,
                   if_exists='append', index=False)
    print("2차 성공")
    myakas3 = myakas.iloc[20000000:]
    myakas3.to_sql(name='akas', con=db_connection,
                   if_exists='append', index=False)
    print("3차 성공")
    print("akas 테이블 생성 완료")

    # types 테이블
    print("====types 테이블 생성 시작")
    types = akas.loc[:, ['tconst', 'ordering']][akas.types != '\\N']
    types['type'] = akas[akas.types != '\\N']['types'].str.split()
    types = types.explode('type')

    conn.execute("""CREATE TABLE types (
        tconst varchar(20) not null, 
        ordering int not null,
        type varchar(50) not null,
        PRIMARY KEY (tconst,ordering,type),
        FOREIGN KEY (tconst,ordering) REFERENCES akas (tconst,ordering)
        );""")
    print("start!")
    for i in range(0, types.shape[0], 10000):
        types.iloc[i:i+10000].to_sql(name='types', con=db_connection,
                                     if_exists='append', index=False)
        print("%d/%d완료" % (i, types.shape[0]))
    print("types 테이블 생성 완료")

    # attributes 테이블
    print("====attributes 테이블 생성 시작")
    attributes = akas.loc[:, ['tconst', 'ordering']][akas.attributes != '\\N']
    attributes['attribute'] = akas[akas.attributes !=
                                   '\\N']['attributes'].str.split()
    attributes = attributes.explode('attribute')

    conn.execute("""CREATE TABLE attributes (
        tconst varchar(20) not null, 
        ordering int not null,
        attribute varchar(50) not null,
        PRIMARY KEY (tconst,ordering,attribute),
        FOREIGN KEY (tconst,ordering) REFERENCES akas (tconst,ordering)
        );""")
    for i in range(0, attributes.shape[0], 10000):
        attributes.iloc[i:i+10000].to_sql(name='attributes', con=db_connection,
                                          if_exists='append', index=False)
        print("%d/%d완료" % (i, attributes.shape[0]))
    print("attributes 테이블 생성 완료")
