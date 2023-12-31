from tabulate import tabulate
import strChanger as sc
import date_calculate as dc
from clear import clear


def printFridge(new_cursor, logged_in_user):
    print()
    print(sc.str_Yellow("냉장고 열어보기 * 🍅 * 🥕 * 🥬 * 🥩 * 🥚 * 🍇 * 🥔 * 🧀"))
    print()

    select_data_query = """
        SELECT food_name, expiration_date, food_pieces
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
            clear()
            return

    else:
        table_data = []
        for row in selected_data:
            food_name, expiration_date, food_pieces = row

            remaining_days_str = dc.ca(expiration_date.date())
            formatted_date = expiration_date.date()
            table_data.append(
                [food_name, formatted_date, food_pieces, remaining_days_str]
            )

        table_headers = ["음식", "유통기한", "갯수", "남은기한"]
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
