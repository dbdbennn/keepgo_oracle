def login(admin_cursor, admin_connection):
    while True:
        print("로그인")
        user_id = input("사용자 ID를 입력하세요: ")
        user_pw = input("비밀번호를 입력하세요: ")

        try:
            # 사용자 정보 조회 쿼리 실행
            login_query = """
                SELECT user_id
                FROM Users
                WHERE user_id = :user_id AND user_pw = :user_pw
            """
            admin_cursor.execute(login_query, user_id=user_id, user_pw=user_pw)
            result = admin_cursor.fetchone()

            if result:
                print("로그인 성공!")
                return result[0]  # 로그인한 사용자의 user_id 반환
            else:
                print("로그인 실패: 사용자 정보가 일치하지 않습니다.")
        except cx_Oracle.DatabaseError as e:
            print("로그인 중 오류가 발생했습니다:", e)

        retry = input("다시 로그인하시겠습니까? (Y/N): ")
        if retry.lower() != "y":
            return None  # 로그인 시도 중단
