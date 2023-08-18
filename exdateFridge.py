from tabulate import tabulate
import strChanger as sc


def create_expiration_view(new_cursor):
    create_view_query = """
        CREATE OR REPLACE VIEW ExpirationCountsView AS
        SELECT
            SUM(CASE WHEN expiration_date - SYSDATE <= 7 THEN 1 ELSE 0 END) AS within_7_days,
            SUM(CASE WHEN expiration_date - SYSDATE <= 30 THEN 1 ELSE 0 END) AS within_30_days,
            SUM(CASE WHEN expiration_date < SYSDATE THEN 1 ELSE 0 END) AS expired
        FROM Fridge
    """
    new_cursor.execute(create_view_query)


def exdateFridge(new_cursor):
    print()
    print(sc.str_Yellow("기한별로 갯수보기 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))

    create_expiration_view(new_cursor)

    select_view_query = "SELECT * FROM ExpirationCountsView"
    new_cursor.execute(select_view_query)
    expiration_counts = new_cursor.fetchone()

    print()
    table_data = [
        ["유통기한 지남", expiration_counts[2]],
        ["7일 이하", expiration_counts[0]],
        ["한달 이하", expiration_counts[1]],
    ]

    table_headers = ["남은기간", "음식 갯수"]
    table = tabulate(table_data, headers=table_headers, tablefmt="rounded_grid")

    print(table)
    print()

    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
