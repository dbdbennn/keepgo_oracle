import subprocess
import cx_Oracle
from tabulate import tabulate
from printFridge import printFridge  # Import the function from the separate file
from inputFridge import inputFridge


# 모듈 설치 함수
def install_module(module):
    subprocess.check_call(["pip", "install", module])


# 필요한 모듈들 목록
required_modules = ["cx_Oracle", "tabulate[widechars]"]  # 필요한 모듈들 추가

# 필요한 모듈 설치
for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Installing {module} module...")
        install_module(module)

from datetime import datetime
from tabulate import tabulate  # 표 작성

tabulate.WIDE_CHARS_MODE = False


# 연결 정보
admin_username = "system"
admin_password = "0503"
hostname = "localhost"
port = "1521"
service_name = "XE"

dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)

# 관리자 계정으로 연결
admin_connection = cx_Oracle.connect(admin_username, admin_password, dsn)
admin_cursor = admin_connection.cursor()

# 사용자 'yje'가 이미 존재하는지 확인
existing_user_query = """
    SELECT COUNT(*)
    FROM dba_users
    WHERE username = 'YJE'
"""
admin_cursor.execute(existing_user_query)
user_count = admin_cursor.fetchone()[0]

if user_count == 0:
    # 사용자 'yje' 생성
    new_username = "YJE"
    new_password = "yje1234"
    admin_cursor.execute(f"CREATE USER {new_username} IDENTIFIED BY {new_password}")
    admin_cursor.execute(f"GRANT CONNECT, RESOURCE TO {new_username}")
    print("User 'YJE' created successfully.")

# 사용자 'yje' 계정으로 연결
new_dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
new_connection = cx_Oracle.connect("YJE", "yje1234", dsn=new_dsn)
new_cursor = new_connection.cursor()

# 'Fridge' 테이블이 이미 존재하지 않는 경우에만 테이블 생성
existing_table_query = """
    SELECT COUNT(*)
    FROM all_tables
    WHERE owner = 'YJE' AND table_name = 'FRIDGE'
"""
new_cursor.execute(existing_table_query)
table_count = new_cursor.fetchone()[0]

if table_count == 0:
    create_table_query = """
        CREATE TABLE Fridge (
            food_name VARCHAR2(255) primary key,
            expiration_date DATE,
            food_pieces NUMBER(3)
        )
    """
    new_cursor.execute(create_table_query)
    new_connection.commit()
    print("Table 'Fridge' created successfully.")
else:
    print("Table 'Fridge' already exists.")


####################################################
# main
def main():
    while True:  # 무한 루프로 메뉴 선택을 계속 받음
        # 메뉴창 출력문
        print(" " + "_" * 52)
        print(
            """|                                                    |
|        ,--,--,--.  ,---.  ,--,--,  ,--.,--.        |
|        |        | | .-. : |      \ |  ||  |        |
|        |  |  |  | \   --. |  ||  | '  ''  '        |
|        `--`--`--'  `----' `--''--'  `----'         |
|                                                    |"""
        )
        print("|\t\t1. 냉장고 열어보기                   |")
        print("|\t\t2. 냉장고에 음식 넣기                |")
        print("|\t\t3. 음식 정보 바꾸기                  |")
        print("|\t\t4. 냉장고에서 음식 꺼내기            |")
        print("|\t\t5. 프로그램 종료                     |")
        print("|" + "_" * 52 + "|")
        print()
        # 메뉴창 출력 끝

        # 메뉴 선택 창
        menu = input("\t\t메뉴 선택 > ")

        if menu == "1":
            printFridge(new_cursor)  # printFridge 함수 실행
        elif menu == "2":
            inputFridge(new_cursor)
        elif menu == "5":
            print("프로그램을 종료합니다.")
            break  # 무한 루프 종료
        else:
            print("잘못된 입력입니다. 다시 선택해주세요.")

    # 프로그램 종료 시에만 연결 해제
    if new_cursor:
        new_cursor.close()
    if new_connection:
        new_connection.close()
    if admin_cursor:
        admin_cursor.close()
    if admin_connection:
        admin_connection.close()


main()
