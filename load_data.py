import pymysql


def load_title_akas(filename, insert_sql):
    conn = pymysql.connect(host='localhost', user='root',
                           password='0000', db='imdb')

    cur = conn.cursor(pymysql.cursors.DictCursor)
    f = open(filename, "r", encoding='UTF8')

    oneline = f.readline()

    oneline = f.readline()[:-1]

    rows = []
    i = 0

    while oneline:
        attrs = tuple(oneline.split('\t'))
        rows.append(attrs)
        i += 1
        if i % 10000 == 0:
            cur.executemany(insert_sql, rows)
            conn.commit()
            rows = []
            print("%s : %d rows" % (filename, i))

        oneline = f.readline()[:-1]

    if rows:
        cur.executemany(insert_sql, rows)
        conn.commit()
        print("%s : %d rows" % (filename, i))

    f.close()
    cur.close()
    conn.close()


# load_title_akas('title.akas.tsv', "insert into title_akas (titleid, ordering, title, region, language, types, attributes, isOriginalTitle) values (%s, %s, %s, %s, %s, %s, %s, %s)")
# load_title_akas('title.basics.tsv', "insert into title_basics (tconst, titleType, primaryTitle, originalTitle, isAdult, startYear, endYear, runtimeMinutes, genres) values (%s, %s, %s, %s, %s, %s, %s, %s, %s)")
load_title_akas('title.crew.tsv',
                "insert into title_crew (tconst, directors, writers) values (%s, %s, %s)")
load_title_akas('title.episode.tsv',
                "insert into title_episode (tconst, parentTconst, seasonNumber, episodeNumber) values (%s, %s, %s, %s)")
load_title_akas('title.principals.tsv',
                "insert into title_principals (tconst, ordering, nconst, category, job, characters) values (%s, %s, %s, %s, %s, %s)")
load_title_akas('title.ratings.tsv',
                "insert into title_ratings (tconst, averageRating, numVotes) values (%s, %s, %s)")
load_title_akas('name.basics.tsv',
                "insert into name_basics (nconst, primaryName, birthYear, deathYear, primaryProfession, knownForTitles) values (%s, %s, %s, %s, %s, %s)")
