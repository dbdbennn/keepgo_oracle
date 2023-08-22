from tabulate import tabulate
import strChanger as sc


def exdateFridge(new_cursor):
    print()
    print(sc.str_Yellow("기한별로 갯수보기 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))

    select_data_query = """
        SELECT *
        FROM Fridge
        ORDER BY EXPIRATION_DATE
    """

    new_cursor.execute(select_data_query)
    selected_data = new_cursor.fetchall()

    if len(selected_data) == 0:
        print("\n\t\t\033[31m❗ 냉장고가 비었어요.\033[0m")
        print()
        inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
        if isinstance(inputMenu, str):
            return

    create_view_query = """
        CREATE OR REPLACE VIEW ExpirationCountsView AS
            SELECT
                (SELECT SUM(food_pieces) FROM Fridge 
                    WHERE expiration_date < SYSDATE) AS expired,
                (SELECT SUM(food_pieces) FROM Fridge 
                    WHERE expiration_date - SYSDATE <= 7 AND expiration_date - SYSDATE >= 1) AS within_7_days,
                (SELECT SUM(food_pieces) FROM Fridge 
                    WHERE expiration_date - SYSDATE <= 30 AND expiration_date - SYSDATE >= 8) AS within_30_days,
                (SELECT SUM(food_pieces) FROM Fridge 
                    WHERE expiration_date > SYSDATE + 30) AS more_than_30_days
            FROM Fridge
        """
    new_cursor.execute(create_view_query)

    select_view_query = "SELECT * FROM ExpirationCountsView"
    new_cursor.execute(select_view_query)
    expiration_counts = new_cursor.fetchone()

    print()
    table_data = [
        [sc.str_bRed("유통기한 지남"), expiration_counts[0]],
        [sc.str_Red("7일 이하"), expiration_counts[1]],
        [sc.str_Yellow("한달 이하"), expiration_counts[2]],
        [sc.str_Blue("한달 이상"), expiration_counts[3]],
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
