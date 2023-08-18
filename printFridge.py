from tabulate import tabulate
import strChanger as sc
import date_calculate as dc


def printFridge(new_cursor):
    select_data_query = """
        SELECT *
        FROM Fridge
    """

    new_cursor.execute(select_data_query)
    selected_data = new_cursor.fetchall()

    # 선택된 데이터 출력
    table_data = []
    for row in selected_data:
        food_name, expiration_date, food_pieces = row

        # Calculate remaining days using the ca function
        remaining_days_str = dc.ca(expiration_date.date())  # ca 모듈 안의 ca 함수 호출
        # Add data to the table
        formatted_date = expiration_date.date()  # 날짜 부분만 추출
        table_data.append([food_name, formatted_date, food_pieces, remaining_days_str])

    table_headers = ["음식", "유통기한", "갯수", "남은기한"]
    table = tabulate(
        table_data, headers=table_headers, tablefmt="rounded_grid", stralign="center"
    )

    print(table)
    print()
    inputMeun = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if str(type(inputMeun)) == "<class 'str'>":
        return
