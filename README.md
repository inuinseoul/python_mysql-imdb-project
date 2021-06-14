# python_mysql-imdb-project
2021년 건국대학교 데이터베이스과목 기말과제

## 본 과제는 아래의 내용을 담고 있습니다.

- IMDB(https://www.imdb.com/interfaces/) 로부터 받아온 데이터셋 활용
- 이를 정리 및 재구성하여 새로운 ER Diagram 제작

![db (3)](https://user-images.githubusercontent.com/70463738/121844246-a40d9a80-cd1e-11eb-993c-7044353b4225.png)

- `pandas`과 `mysql` 연동을 통한 테이블 생성 및 데이터 INSERT (allInsertData.py)
- 해당 DB를 기반으로 제목 기반 검색, 감독 기반 검색 등의 기본기능 제공
- +) index를 생성하여 쿼리문이 최적화되어 수행될 수 있도록 하였음
