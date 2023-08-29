from tabulate import tabulate
import strChanger as sc
import date_calculate as dc
from clear import clear


def userFridge(new_cursor):
    print()
    print(sc.str_Yellow("사용자별 음식갯수 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))
    print()

    select_data_query = """
        SELECT U.user_name, SUM(F.food_pieces) AS food_count
        FROM USERS U
        LEFT JOIN FRIDGE F ON U.user_id = F.user_id
        GROUP BY U.user_name
    """

    new_cursor.execute(select_data_query)
    selected_data = new_cursor.fetchall()

    table_data = []
    for row in selected_data:
        user_id, food_count = row
        table_data.append([user_id, food_count])

    table_headers = ["사용자", "음식 개수"]
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
        clear()
        return


# 이하 코드에서 냉장고 정보를 출력하는 함수 호출 등의 부분이 있을 것입니다.
