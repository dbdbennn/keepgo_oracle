import strChanger as sc


def is_numeric(password):
    try:
        int(password)
        return True
    except ValueError:
        return False


def login(admin_cursor, admin_connection):
    print(
        """                   
\t,--.              ,--.         
\t|  | ,---.  ,---. `--',--,--,  
\t|  || .-. || .-. |,--.|      \ 
\t|  |' '-' '' '-' '|  ||  ||  | 
\t`--' `---' .`-  / `--'`--''--' 
\t           `---'               
          """
    )
    while True:
        user_id = input("\t사용자 ID를 입력하세요 > ")
        user_pw = input("\t비밀번호를 입력하세요 > ")

        if not is_numeric(user_pw):
            print(sc.str_Red("\t비밀번호는 숫자만 가능합니다. 다시 입력해주세요."))
            print()
            continue

        # 사용자 정보 조회 쿼리 실행
        login_query = """
            SELECT user_id
            FROM Users
            WHERE user_id = :user_id AND user_pw = :user_pw
        """
        admin_cursor.execute(login_query, user_id=user_id, user_pw=user_pw)
        result = admin_cursor.fetchone()

        if result:
            print()
            print(sc.str_Blue("\t\t로그인 성공!"))
            print()
            return result[0]  # 로그인한 사용자의 user_id 반환

        print(sc.str_Red("\t로그인 실패: 사용자 정보가 일치하지 않습니다."))
        retry = input("\t다시 로그인하시겠습니까? (Y/N) > ")
        print()
        if retry.lower() != "y":
            return None  # 로그인 시도 중단
