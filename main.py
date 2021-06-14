import pymysql
import pandas as pd
import os

conn = pymysql.connect(host='localhost', user='root',
                       password='0000', db='imdb')  # DB 연결
curs = conn.cursor(pymysql.cursors.DictCursor)  # 커서 생성

print("===IMDB 영화 검색 프로그램===")
print("\n메뉴를 선택하세요.")
menu = int(input(
    "[1] 제목 검색 [2] 배우 검색 [3] 감독 검색 [4] 장르 검색 [5] 작가 검색 [0] 종료\n=> "))

while (menu != 0):
    if (menu == 1):
        # 제목검색
        movieName = input("제목을 입력하세요 : ")
        sql = "select titleType, primaryTitle, primaryName,startYear from movie join directors on movie.tconst = directors.tconst join person on directors.director = person.nconst where primaryTitle = '%s';" % movieName
        curs.execute(sql)
        row = curs.fetchall()
        os.system('cls')
        print("\n[제목이 %s인 영화목록]" % movieName)
        df = pd.DataFrame(row)
        print(df)
    elif (menu == 2):
        # 특정배우 등장영화 별점높은순
        actorName = input("배우 이름을 입력하세요 : ")
        sql = """select primaryTitle,averageRating,person.nconst from movie 
            join principals on movie.tconst = principals.tconst
            join person on principals.nconst = person.nconst
            join ratings on movie.tconst = ratings.tconst
            where (principals.category = 'actor' or principals.category = 'actress') 
            and primaryName='%s' order by averageRating desc;""" % actorName
        curs.execute(sql)
        row = curs.fetchall()
        os.system('cls')
        print("\n[%s가 출연한 영화목록]" % actorName)
        df = pd.DataFrame(row)
        print(df)
    elif (menu == 3):
        # 특정감독 제작영화 개봉연도순
        directorName = input("감독 이름을 입력하세요 : ")
        sql = """select primaryTitle,startYear from movie join directors on movie.tconst = directors.tconst 
            join person on directors.director = person.nconst
            join ratings on movie.tconst = ratings.tconst
            where primaryName = '%s' order by startYear desc;""" % directorName
        curs.execute(sql)
        row = curs.fetchall()
        os.system('cls')
        print("\n[%s가 제작한 영화목록]" % directorName)
        df = pd.DataFrame(row)
        print(df)
    elif (menu == 4):
        # 장르 선택
        myGenre = input("장르를 입력하세요 : ")
        # 어떤 순서로 볼 지 선택 (리뷰많은순, 별점높은순)
        ror = "averageRating"
        if int(input("[1] 리뷰많은순 [2] 별점높은순 : ")) == 1:
            ror = "numVotes"
        myLimit = input("검색 개수를 선택하세요 (큰 수를 입력할 수록 시간이 소요됨) : ")
        sql = """select primaryTitle,averageRating,numVotes,genre from movie join genres on movie.tconst = genres.tconst 
            join ratings on movie.tconst = ratings.tconst 
            where genre = '%s' order by %s desc limit %s;""" % (myGenre, ror, myLimit)
        curs.execute(sql)
        row = curs.fetchall()
        os.system('cls')
        print("\n[장르 : %s]" % myGenre)
        df = pd.DataFrame(row)
        print(df)
    elif (menu == 5):
        # 작가 검색 개봉일순
        writerName = input("작가 이름을 입력하세요 : ")
        sql = """select primaryTitle,startYear from movie join writers on movie.tconst = writers.tconst 
            join person on writers.writer = person.nconst
            where startYear != 9999 and primaryName = '%s' order by startYear;""" % writerName
        curs.execute(sql)
        row = curs.fetchall()
        os.system('cls')
        print("\n[%s가 작가인 영화목록]" % writerName)
        df = pd.DataFrame(row)
        print(df)
    else:
        print("적절한 번호가 아닙니다.")
    print("\n메뉴를 선택하세요.")
    menu = int(input(
        "[1] 제목 검색 [2] 배우 검색 [3] 감독 검색 [4] 장르 검색 [5] 작가 검색 [0] 종료\n=> "))
conn.close()  # 종료
