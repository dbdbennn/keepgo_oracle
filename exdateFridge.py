from tabulate import tabulate
import strChanger as sc


def exdateFridge(new_cursor):
    print()
    print(sc.str_Yellow("기한별로 갯수보기 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))

    create_view_query = """
        CREATE OR REPLACE VIEW ExpirationCountsView AS
            SELECT
                SUM(CASE WHEN expiration_date < SYSDATE THEN food_pieces ELSE 0 END) AS expired,
                SUM(CASE WHEN expiration_date - SYSDATE <= 7 AND expiration_date - SYSDATE >= 1 THEN food_pieces ELSE 0 END) AS within_7_days,
                SUM(CASE WHEN expiration_date - SYSDATE <= 30 AND expiration_date - SYSDATE >= 8 THEN food_pieces ELSE 0 END) AS within_30_days,
                SUM(CASE WHEN expiration_date > SYSDATE + 30 THEN food_pieces ELSE 0 END) AS more_than_30_days
            FROM Fridge
        """
    new_cursor.execute(create_view_query)

    select_view_query = "SELECT * FROM ExpirationCountsView"
    new_cursor.execute(select_view_query)
    expiration_counts = new_cursor.fetchone()

    print()
    table_data = [
        ["유통기한 지남", expiration_counts[0]],
        ["7일 이하", expiration_counts[1]],
        ["한달 이하", expiration_counts[2]],
        ["한달 이상", expiration_counts[3]],
    ]

    table_headers = ["남은기한", "음식 갯수"]
    table = tabulate(table_data, headers=table_headers, tablefmt="rounded_grid")

    print(table)
    print()

    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
