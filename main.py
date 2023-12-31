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
from exdateFridge import exdateFridge
from exitFridge import exitFridge
from userFridge import userFridge
from signup import signup
from login import login
import strChanger as sc
from clear import clear
import cx_Oracle

clear()


# 연결 정보
admin_username = "system"
admin_password = "0503"
# admin_password = "1234"
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
    admin_cursor.execute(
        f"GRANT CONNECT, RESOURCE, CREATE VIEW, DROP ANY VIEW TO {new_username}"
    )
    print("User 'KEEPGO' created successfully.")
else:
    print("User 'KEEPGO' already exists.")

# 사용자 'KEEPGO' 계정으로 연결
new_dsn = cx_Oracle.makedsn(hostname, port, service_name=service_name)
new_connection = cx_Oracle.connect("KEEPGO", "keepgo", dsn=new_dsn)
new_cursor = new_connection.cursor()

# 'Users' 테이블이 이미 존재하지 않는 경우에만 테이블 생성
existing_table_query = """
    SELECT COUNT(*)
    FROM all_tables
    WHERE owner = 'KEEPGO' AND table_name = 'USERS'
"""
new_cursor.execute(existing_table_query)
table_count = new_cursor.fetchone()[0]

if table_count == 0:
    create_table_query = """
        CREATE TABLE USERS (
            user_id VARCHAR2(255) PRIMARY KEY,
            user_name VARCHAR2(255),
            user_pw NUMBER(4)
        )
    """
    new_cursor = new_connection.cursor()
    new_cursor.execute(create_table_query)
    new_connection.commit()
    print("Table 'Users' created successfully.")
else:
    print("Table 'Users' already exists.")

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
            food_id NUMBER PRIMARY KEY,
            food_name VARCHAR2(255),
            expiration_date DATE,
            food_pieces NUMBER(3),
            user_id VARCHAR2(255),
            CONSTRAINT fk_user_id
                FOREIGN KEY (user_id)
                REFERENCES Users(user_id)
        )
    """
    new_cursor = new_connection.cursor()
    new_cursor.execute(create_table_query)

    create_trigger_query = """
        CREATE OR REPLACE TRIGGER FRIDGE_TRIGGER
        BEFORE INSERT ON FRIDGE
        FOR EACH ROW
        BEGIN
            SELECT NVL(MAX(food_id), 0) + 1 INTO :new.food_id FROM FRIDGE;
        END;
    """
    new_cursor.execute(create_trigger_query)

    new_connection.commit()
    print("Table 'FRIDGE' and trigger created successfully.")
else:
    print("Table 'FRIDGE' already exists.")

print("All settings are Successful!")

####################################################

print(
    sc.str_Cyan(
        """
.-. .-')     ('-.     ('-.     _ (`-.                                
\  ( OO )  _(  OO)  _(  OO)   ( (OO  )                               
,--. ,--. (,------.(,------. _.`     \        ,----.     .-'),-----. 
|  .'   /  |  .---' |  .---'(__...--''       '  .-./-') ( OO'  .-.  '
|      /,  |  |     |  |     |  /  | |       |  |_( O- )/   |  | |  |
|     ' _)(|  '--. (|  '--.  |  |_.' |       |  | .--, \\_)  |  |\|  |
|  .   \   |  .--'  |  .--'  |  .___.'      (|  | '. (_/  \ |  | |  |
|  |\   \  |  `---. |  `---. |  |            |  '--'  |    `'  '-'  '
`--' '--'  `------' `------' `--'             `------'       `-----' 

        """
    )
)


def create_users_table():
    global logged_in_user
    while True:
        print(
            """╭────────────────────────────────────────────────────╮
│        ,--,--,--.  ,---.  ,--,--,  ,--.,--.        │
│        |        | | .-. : |      \ |  ||  |        │
│        |  |  |  | \   --. |  ||  | '  ''  '        │
│        `--`--`--'  `----' `--''--'  `----'         │
│                                                    │"""
        )
        # 로그인, 회원가입, 프로그램 종료 메뉴 출력
        print("│\t\t1. 로그인                            │")
        print("│\t\t2. 회원가입                          │")
        print("│\t\t3. 프로그램 종료                     │")
        print("╰" + "─" * 52 + "╯")
        print()

        login_menu = input("\t\t메뉴 선택 > ")

        if login_menu == "1":
            clear()
            logged_in_user = login(new_cursor, new_connection)  # 로그인 로직 실행
            if logged_in_user != None:
                main(logged_in_user)  # 로그인 후 메뉴 선택 창으로 이동
            else:
                print(sc.str_Red("\t❗ 로그인 하지 못했습니다."))
                print()
        elif login_menu == "2":
            clear()
            signup(new_cursor, new_connection)  # 회원가입 로직 실행

        elif login_menu == "3":
            clear()
            isExit = exitFridge()
            if isExit == "1":
                clear()
                create_users_table()
            else:
                exit()
            break  # 무한 루프 종료
        else:
            while login_menu != "1" and login_menu != "2" and login_menu != "3":
                print()
                login_menu = input("\t다시 선택해주세요 > ")
                if login_menu == "1":
                    clear()
                    logged_in_user = login(new_cursor, new_connection)  # 로그인 로직 실행
                    if logged_in_user != None:
                        main(logged_in_user)  # 로그인 후 메뉴 선택 창으로 이동
                    else:
                        print(sc.str_Red("\t❗ 로그인 하지 못했습니다."))
                        print()
                elif login_menu == "2":
                    clear()
                    signup(new_cursor, new_connection)  # 회원가입 로직 실행

                elif login_menu == "3":
                    clear()
                    isExit = exitFridge()
                    if isExit == "1":
                        clear()
                        create_users_table()
                    else:
                        exit()
                    break  # 무한 루프 종료


# main
def main(logged_in_user):
    while True:  # 무한 루프로 메뉴 선택을 계속 받음
        # 메뉴창 출력문
        print(
            """╭────────────────────────────────────────────────────╮
│        ,--,--,--.  ,---.  ,--,--,  ,--.,--.        │
│        |        | | .-. : |      \ |  ||  |        │
│        |  |  |  | \   --. |  ||  | '  ''  '        │
│        `--`--`--'  `----' `--''--'  `----'         │
│                                                    │"""
        )
        print("│\t\t1. 냉장고 열어보기                   │")
        print("│\t\t2. 기한별로 갯수보기                 │")
        print("│\t\t3. 냉장고에 음식 넣기                │")
        print("│\t\t4. 음식 정보 바꾸기                  │")
        print("│\t\t5. 사용자별 음식갯수                 │")
        print("│\t\t6. 프로그램 종료                     │")
        print("│\t\t7. 로그아웃                          │")
        print("╰" + "─" * 52 + "╯")
        print()
        # 메뉴창 출력 끝

        # 메뉴 선택 창
        menu = input("\t\t메뉴 선택 > ")

        if menu == "1":
            clear()
            printFridge(new_cursor, logged_in_user)  # printFridge 함수 실행
        elif menu == "2":
            clear()
            exdateFridge(new_cursor, logged_in_user)  # exdateFridge 함수 실행
        elif menu == "3":
            clear()
            inputFridge(new_cursor, logged_in_user)
        elif menu == "4":
            clear()
            setFridge(new_cursor, logged_in_user)
        elif menu == "5":
            clear()
            userFridge(new_cursor)
        elif menu == "6":
            clear()
            isExit = exitFridge()
            if isExit == "1":
                clear()
                main(logged_in_user)
            else:
                exit()
            break  # 무한 루프 종료
        elif menu == "7":
            clear()
            print()
            print(sc.str_Blue("\t\t로그아웃이 완료되었습니다."))
            print()
            create_users_table()
        else:  # 다른 수(str형태)가 입력됐을 때 while문을 돌린다.
            while (
                menu != "1"
                and menu != "2"
                and menu != "3"
                and menu != "4"
                and menu != "5"
                and menu != "6"
                and menu != "7"
            ):
                print()
                menu = input("\t다시 선택해주세요 > ")
                if menu == "1":
                    clear()
                    printFridge(new_cursor, logged_in_user)  # printFridge 함수 실행
                elif menu == "2":
                    clear()
                    exdateFridge(new_cursor, logged_in_user)  # exdateFridge 함수 실행
                elif menu == "3":
                    clear()
                    inputFridge(new_cursor, logged_in_user)
                elif menu == "4":
                    clear()
                    setFridge(new_cursor, logged_in_user)
                elif menu == "5":
                    clear()
                    userFridge(new_cursor)
                elif menu == "6":
                    clear()
                    isExit = exitFridge()
                    if isExit == "1":
                        clear()
                        main(logged_in_user)
                    else:
                        exit()
                    break  # 무한 루프 종료
                elif menu == "7":
                    clear()
                    print()
                    print(sc.str_Blue("\t로그아웃이 완료되었습니다."))
                    print()
                    create_users_table()

    # 프로그램 종료 시에만 연결 해제
    if new_cursor:
        new_cursor.close()
    if new_connection:
        new_connection.close()
    if admin_cursor:
        admin_cursor.close()
    if admin_connection:
        admin_connection.close()


create_users_table()
