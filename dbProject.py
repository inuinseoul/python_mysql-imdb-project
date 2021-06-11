import pymysql

conn = pymysql.connect(host='localhost', user='root',
                       password='0000', db='university')  # DB 연결
curs = conn.cursor(pymysql.cursors.DictCursor)  # 커서 생성

print("===수강신청 관리 프로그램===")
print("\n메뉴를 선택하세요.")
menu = int(input(
    "[1] 학생등록 [2] 학생 삭제 [3] 학생 조회 [4] 과목 등록 [5] 과목 삭제 [6] 과목 조회 [7] 수강신청 [8] 수강취소 [9] 수강조회 [0] 종료\n=> "))

while (menu != 0):
    if (menu == 1):
        # • 메뉴1: 학생 등록
        # – 학생 정보를 콘솔에서 입력 받음
        sinfo = input("학생정보를 입력하세요(sno sname syear dept)\n=> ")
        sinfo_array = sinfo.split()
        sql = "insert into student (sno, sname, syear, dept) values (%s, %s, %s, %s)"
        a = (int(sinfo_array[0]), sinfo_array[1],
             int(sinfo_array[2]), sinfo_array[3])
        curs.execute(sql, a)
        conn.commit()
    elif (menu == 2):
        # • 메뉴2: 학생 삭제 – 삭제할 학생의 학번을 콘솔에서 입력 받음
        sno = input("삭제를 원하는 학번을 입력하세요\n=> ")
        sql = "delete from student where sno = %s;" % sno
        curs.execute(sql)
        conn.commit()
    elif (menu == 3):
        # • 메뉴3: 학생 조회
        # – 전체 학생 및 특정 학번 조회, 학번순.
        print("\n메뉴를 선택하세요.")
        menu3 = int(input("[1] 전체조회 [2] 학번으로 조회\n=> "))
        if (menu3 == 1):
            sql = "SELECT * FROM student order by sno;"
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        elif (menu3 == 2):
            sno = input("조회를 원하는 학번을 입력하세요\n=> ")
            sql = "SELECT * FROM student where sno=%s order by sno;" % sno
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        else:
            print("적절한 번호가 아닙니다.")
    elif (menu == 4):
        # • 메뉴4: 과목 등록
        # – 과목 정보를 콘솔에서 입력 받음
        cinfo = input("과목정보를 입력하세요(cno, cname, credit, dept, prname)\n=> ")
        cinfo_array = cinfo.split()
        sql = "insert into course (cno, cname, credit, dept, prname) values (%s, %s, %s, %s, %s)"
        a = (cinfo_array[0], cinfo_array[1],
             int(cinfo_array[2]), cinfo_array[3], cinfo_array[4])
        curs.execute(sql, a)
        conn.commit()
    elif (menu == 5):
        # • 메뉴5: 과목 삭제
        # – 삭제할 과목의 과목번호를 콘솔에서 입력 받음
        cno = input("삭제를 원하는 과목번호를 입력하세요\n=> ")
        sql = "delete from course where cno = '%s';" % cno
        curs.execute(sql)
        conn.commit()
    elif (menu == 6):
        # • 메뉴6: 과목 조회
        # – 전체 과목 및 특정 과목번호 조회, 과목번호순.
        print("\n메뉴를 선택하세요.")
        menu6 = int(input("[1] 전체조회 [2] 과목번호로 조회\n=> "))
        if (menu6 == 1):
            sql = "SELECT * FROM course order by cno;"
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        elif (menu6 == 2):
            cno = input("조회를 원하는 과목번호를 입력하세요\n=> ")
            sql = "SELECT * FROM course where cno='%s' order by cno;" % cno
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        else:
            print("적절한 번호가 아닙니다.")
    elif (menu == 7):
        # • 메뉴7: 수강신청 – 학번 및 과목번호 입력받음.
        sno = input("학번을 입력하세요\n=> ")
        cno = input("과목번호를 입력하세요\n=> ")
        sql = "insert into enrol (sno, cno, grade, midterm, final) values (%s, %s, %s, %s, %s)"
        a = (sno, cno, "F", 0, 0)
        curs.execute(sql, a)
        conn.commit()
    elif (menu == 8):
        # • 메뉴8: 수강취소
        # – 학번 및 과목번호 입력받음.
        sno = input("학번을 입력하세요\n=> ")
        cno = input("과목번호를 입력하세요\n=> ")
        sql = "delete from enrol where sno = %s and cno = %s"
        a = (sno, cno)
        curs.execute(sql, a)
        conn.commit()
    elif (menu == 9):
        # • 메뉴9: 수강조회
        # – 학번으로 조회
        # – 과목으로 조회
        # – 전체 수강정보 조회
        print("\n메뉴를 선택하세요.")
        menu9 = int(input("[1] 학번으로 조회 [2] 과목번호로 조회 [3] 전체 조회\n=> "))
        if (menu9 == 1):
            sno = input("학번을 입력하세요\n=> ")
            sql = "SELECT * FROM enrol where sno=%s;" % sno
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        elif (menu9 == 2):
            cno = input("과목번호를 입력하세요\n=> ")
            sql = "SELECT * FROM enrol where cno='%s';" % cno
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        elif (menu9 == 3):
            sql = "SELECT * FROM enrol;"
            curs.execute(sql)
            row = curs.fetchone()
            while row:
                print(row)
                row = curs.fetchone()
        else:
            print("적절한 번호가 아닙니다.")
    else:
        print("적절한 번호가 아닙니다.")
    print("\n메뉴를 선택하세요.")
    menu = int(input(
        "[1] 학생등록 [2] 학생 삭제 [3] 학생 조회 [4] 과목 등록 [5] 과목 삭제 [6] 과목 조회 [7] 수강신청 [8] 수강취소 [9] 수강조회 [0] 종료\n=> "))
conn.close()  # 종료
