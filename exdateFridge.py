from tabulate import tabulate
import strChanger as sc


def exdateFridge(new_cursor, logged_in_user):
    print()
    print(sc.str_Yellow("기한별로 갯수보기 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))

    select_data_query = """
        SELECT *
        FROM Fridge
        WHERE user_id = :logged_in_user
        ORDER BY EXPIRATION_DATE
    """

    new_cursor.execute(select_data_query, logged_in_user=logged_in_user)
    selected_data = new_cursor.fetchall()

    if len(selected_data) == 0:
        print("\n\t\t\033[31m❗ 냉장고가 비었어요.\033[0m")
        print()
        inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
        if isinstance(inputMenu, str):
            return

    create_view_query = f"""
        CREATE OR REPLACE VIEW ExpirationCountsView AS
        SELECT
            (SELECT SUM(food_pieces) FROM Fridge 
                WHERE TRUNC(expiration_date) = TRUNC(SYSDATE) 
                AND user_id = '{logged_in_user}') AS today_expired,
            (SELECT SUM(food_pieces) FROM Fridge 
                WHERE expiration_date < TRUNC(SYSDATE) 
                AND user_id = '{logged_in_user}') AS expired,
            (SELECT SUM(food_pieces) FROM Fridge 
                WHERE TRUNC(expiration_date) BETWEEN TRUNC(SYSDATE) + 1 AND TRUNC(SYSDATE) + 7 
                AND user_id = '{logged_in_user}') AS within_7_days,
            (SELECT SUM(food_pieces) FROM Fridge 
                WHERE TRUNC(expiration_date) BETWEEN TRUNC(SYSDATE) + 8 AND TRUNC(SYSDATE) + 30 
                AND user_id = '{logged_in_user}') AS within_30_days,
            (SELECT SUM(food_pieces) FROM Fridge 
                WHERE expiration_date > TRUNC(SYSDATE) + 31 
                AND user_id = '{logged_in_user}') AS more_than_30_days
        FROM dual
    """
    new_cursor.execute(create_view_query)

    select_view_query = "SELECT * FROM ExpirationCountsView"
    new_cursor.execute(select_view_query)
    expiration_counts = new_cursor.fetchone()

    print()
    table_data = [
        [sc.str_bRed("오늘까지"), expiration_counts[0]],
        [sc.str_bRed("유통기한 지남"), expiration_counts[1]],
        [sc.str_Red("7일 이하"), expiration_counts[2]],
        [sc.str_Yellow("한달 이하"), expiration_counts[3]],
        [sc.str_Blue("한달 이상"), expiration_counts[4]],
    ]

    table_headers = ["남은기한", "음식 갯수"]
    table = tabulate(
        table_data,
        headers=table_headers,
        tablefmt="rounded_grid",
        stralign="center",
    )

    print(table)
    print()

    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
