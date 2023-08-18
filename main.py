import subprocess

required_modules = ["cx_Oracle", "tabulate[widechars]"]

for module in required_modules:
    try:
        __import__(module)
    except ImportError:
        print(f"Installing {module} module...")
        subprocess.check_call(["pip", "install", module])

from printFridge import printFridge
from inputFridge import inputFridge
from deleteFridge import deleteFridge
from setFridge import setFridge
import strChanger as sc
import cx_Oracle


# 연결 정보
admin_username = "system"
admin_password = "1234"
hostname = "localhost"
port = "1521"
service_name = "XE"

dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)

# 관리자 계정으로 연결
admin_connection = cx_Oracle.connect(admin_username, admin_password, dsn)
admin_cursor = admin_connection.cursor()

# 사용자 'KEEPGO'가 이미 존재하는지 확인
existing_user_query = """
    SELECT COUNT(*)
    FROM dba_users
    WHERE username = 'KEEPGO'
"""
admin_cursor.execute(existing_user_query)
user_count = admin_cursor.fetchone()[0]

if user_count == 0:
    # 사용자 'KEEPGO' 생성
    new_username = "KEEPGO"
    new_password = "keepgo"
    admin_cursor.execute(f"CREATE USER {new_username} IDENTIFIED BY {new_password}")
    admin_cursor.execute(f"GRANT CONNECT, RESOURCE TO {new_username}")
    print("User 'KEEPGO' created successfully.")

# 사용자 'KEEPGO' 계정으로 연결
new_dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
new_connection = cx_Oracle.connect("KEEPGO", "keepgo", dsn=new_dsn)
new_cursor = new_connection.cursor()

# 'Fridge' 테이블이 이미 존재하지 않는 경우에만 테이블 생성
existing_table_query = """
    SELECT COUNT(*)
    FROM all_tables
    WHERE owner = 'KEEPGO' AND table_name = 'FRIDGE'
"""
new_cursor.execute(existing_table_query)
table_count = new_cursor.fetchone()[0]

if table_count == 0:
    create_table_query = """
        CREATE TABLE FRIDGE (
            food_name VARCHAR2(255) primary key,
            expiration_date DATE,
            food_pieces NUMBER(3)
        )
    """
    new_cursor.execute(create_table_query)
    new_connection.commit()
    print("Table 'FRIDGE' created successfully.")
else:
    print("Table 'FRIDGE' already exists.")


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
        elif menu == "3":
            setFridge(new_cursor)
        elif menu == "4":
            deleteFridge(new_cursor)
        elif menu == "5":
            print()
            isExit = input(
                sc.str_Green(
                    """
    \t정말 keep Go를 나가시겠습니까? 🥺

   \t나가시겠다면 아무 키를,
   \t메뉴로 돌아가려면 1을 입력하세요 > """
                )
            )
            if isExit == "1":
                main()
            else:
                exit()
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
