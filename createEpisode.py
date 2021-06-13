import sqlalchemy
import pandas as pd


def start():
    db_connection_str = 'mysql+pymysql://root:0000@localhost/imdb'
    db_connection = sqlalchemy.create_engine(db_connection_str)
    conn = db_connection.connect()

    episode = pd.read_csv('title.episode.tsv', sep='\t', low_memory=False)
    print("episode 불러오기 완료")
    basics = pd.read_csv('title.basics.tsv', sep='\t', low_memory=False)
    print("basics 불러오기 완료")

    episode = pd.merge(episode, basics, left_on="parentTconst",
                       right_on="tconst", how="inner").loc[:, ['tconst_x', 'parentTconst', 'seasonNumber', 'episodeNumber']]
    episode.rename(columns={'tconst_x': 'tconst'}, inplace=True)
    episode['seasonNumber'] = episode.seasonNumber.replace({"\\N": -1})
    episode['episodeNumber'] = episode.episodeNumber.replace({"\\N": -1})

    # episode 테이블
    print("====episode 테이블 생성 시작")
    conn.execute("""CREATE TABLE episode (
        tconst varchar(20) not null, 
        parentTconst varchar(20) not null, 
        seasonNumber int,
        episodeNumber int,
        PRIMARY KEY (tconst),
        FOREIGN KEY (tconst) REFERENCES movie (tconst),
        FOREIGN KEY (parentTconst) REFERENCES movie (tconst)
        );""")
    for i in range(0, episode.shape[0], 10000):
        episode.iloc[i:i+10000].to_sql(name='episode', con=db_connection,
                                       if_exists='append', index=False)
        print("%d/%d완료" % (i, episode.shape[0]))
    print("episode 테이블 생성 완료")
