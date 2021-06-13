import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    name_basics = pd.read_csv('name.basics.tsv', sep='\t', low_memory=False)
    print("name_basics 불러오기 완료")
    name_basics['birthYear'] = name_basics.birthYear.replace({"\\N": 9999})
    name_basics['deathYear'] = name_basics.deathYear.replace({"\\N": 9999})

    basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    print("basics 불러오기 완료")
    basics['startYear'] = basics.startYear.replace({"\\N": 9999})
    basics['endYear'] = basics.endYear.replace({"\\N": 9999})
    basics['isAdult'] = basics.isAdult.replace({"\\N": -1})
    basics['runtimeMinutes'] = basics.runtimeMinutes.replace(
        {"\\N": -1, "Reality-TV": 0, "Documentary": 0, "Talk-Show": 0, "Game-Show": 0, "Animation,Comedy,Family": 0})

    # person 테이블
    print("====person 테이블 생성 시작")
    person = name_basics.iloc[:, 0:4]
    persontype = {'nconst': sqlalchemy.types.VARCHAR(20),
                  'primaryName': sqlalchemy.types.VARCHAR(200),
                  'birthYear': sqlalchemy.INTEGER(),
                  'deathYear': sqlalchemy.INTEGER(),
                  }
    person.to_sql(name='person', con=db_connection,
                  if_exists='append', index=False, dtype=persontype)
    print("삽입완료")
    conn.execute('ALTER TABLE person ADD PRIMARY KEY (nconst);')
    print("설정완료")
    print("person 테이블 생성 완료")

    # movie 테이블
    print("====movie 테이블 생성 시작")
    movie = basics.iloc[:, :-1]
    movietype = {'tconst': sqlalchemy.types.VARCHAR(20),
                 'titleType': sqlalchemy.types.VARCHAR(20),
                 'primaryTitle': sqlalchemy.VARCHAR(450),
                 'originalTitle': sqlalchemy.VARCHAR(450),
                 'isAdult': sqlalchemy.INTEGER(),
                 'startYear': sqlalchemy.INTEGER(),
                 'endYear': sqlalchemy.INTEGER(),
                 'runtimeMinutes': sqlalchemy.INTEGER(),
                 }
    movie.to_sql(name='movie', con=db_connection,
                 if_exists='append', index=False, dtype=movietype)
    print("삽입완료")
    conn.execute('ALTER TABLE movie ADD PRIMARY KEY (tconst);')
    print("설정완료")
    print("movie 테이블 생성 완료")
