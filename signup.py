import strChanger as sc


def signup(new_cursor, new_connection):
    print(
        """                                 
\t      ,--.                           
\t ,---.`--',---.,--,--,,--.,--.,---.  
\t(  .-',--| .-. |      |  ||  | .-. | 
\t.-'  `|  ' '-' |  ||  '  ''  | '-' ' 
\t`----'`--.`-  /`--''--'`----'|  |-'  
\t         `---'               `--'    
"""
    )

    while True:
        new_user_id = input("\t사용할 ID를 입력하세요 > ")

        # Check if the user_id already exists
        check_user_query = """
            SELECT COUNT(*)
            FROM USERS
            WHERE user_id = :new_user_id
        """
        new_cursor.execute(check_user_query, new_user_id=new_user_id)
        user_count = new_cursor.fetchone()[0]

        if user_count > 0:
            print(sc.str_Red("\t❗ 이미 존재하는 ID입니다. 다른 ID를 입력해주세요."))
            print()
            continue
        
        new_user_name = input('\t사용할 이름을 입력하세요 > ')

        while True:
            new_user_pw = input("\t사용할 비밀번호(4자리 숫자)를 입력하세요 > ")
            new_user_pw_confirm = input("\t비밀번호를 다시 입력하세요 > ")

            if len(new_user_pw) != 4 or not new_user_pw.isdigit():
                print(sc.str_Red("\t❗ 비밀번호는 4자리 숫자로 입력해주세요."))
                print()
                continue

            if new_user_pw != new_user_pw_confirm:
                print(sc.str_Red("\t❗ 비밀번호가 일치하지 않습니다. 다시 입력해주세요."))
                print()
                continue

            break

        # 사용자 등록을 위한 SQL 문 실행
        signup_query = """
            INSERT INTO USERS (user_id, user_pw)
            VALUES (:new_user_id, :new_user_pw)
        """
        new_cursor.execute(
            signup_query, new_user_id=new_user_id, new_user_pw=new_user_pw
        )
        new_connection.commit()
        print()
        print(sc.str_Blue("\t\t회원가입 성공!"))
        print()
        return new_user_id
