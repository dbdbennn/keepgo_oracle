import strChanger as sc
from tabulate import tabulate


def deleteFridge(cursor):
    print()
    print(sc.str_Cyan("냉장고에서 음식 꺼내기 - 🍅 - 🥕 - 🥬 - 🥩 - 🥚 - 🍇 - 🥔 - 🍠"))

    cursor.execute("SELECT food_id, food_name, food_pieces FROM Fridge")
    fridge_data = cursor.fetchall()

    if not fridge_data:
        print("\n\t  \033[31m❗ 음식이 없어 꺼낼 수 없습니다.\033[0m")
        print()
        inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
        if isinstance(inputMenu, str):
            return

    name = input("\n\t\t꺼낼 음식은? > ")
    matching_items = [(row[0], row[1], row[2]) for row in fridge_data if row[1] == name]

    while True:
        if len(matching_items) == 0:
            print("\033[31m" + "\n\t\t❗ 입력한 음식이 없습니다." + "\033[0m")
            name = input("\n\t\t꺼낼 음식은? > ")
            matching_items = [
                (row[0], row[1], row[2]) for row in fridge_data if row[1] == name
            ]
        else:
            break

    if len(matching_items) > 1:
        cursor.execute(
            "SELECT food_id, food_name, food_pieces, expiration_date FROM Fridge"
        )  # 유통기한 정보 추가
        table_data = cursor.fetchall()
        table_headers = ["food_id", "음식 이름", "음식 갯수", "유통기한"]
        table_data = [
            (row[0], row[1], row[2], row[3].strftime("%Y-%m-%d"))
            for row in table_data
            if row[1] == name
        ]
        print(
            "\n"
            + tabulate(
                table_data,
                headers=table_headers,
                tablefmt="rounded_grid",
                stralign="center",
            )
        )
        food_id = input("\n\t\t꺼낼 음식의 ID를 입력하세요 > ")
        while not food_id.isdigit() or int(food_id) not in [
            item[0] for item in matching_items
        ]:
            print("\033[31m" + "\n\t\t❗ 올바른 ID를 입력하세요." + "\033[0m")
            food_id = input("\n\t\t꺼낼 음식의 ID를 입력하세요 > ")
        food_id = int(food_id)
    else:
        food_id = matching_items[0][0]

    available_pieces = matching_items[0][2]

    while True:
        amount_input = input("\n\t\t꺼낼 음식의 갯수는? > ")
        if not amount_input.isdigit():
            print(sc.str_Red("\n\t\t\033[31m❗ 숫자만 입력해주세요.\033[0m"))
            continue

        amount = int(amount_input)
        if amount <= 0:
            print(sc.str_Red("\n\t\t\033[31m❗ 입력한 음식의 갯수가 올바르지 않습니다.\033[0m"))
        elif amount > available_pieces:
            print(sc.str_Red("\n\t\t\033[31m❗ 초과하여 꺼낼 수 없습니다.\033[0m"))
        else:
            break

    cursor.execute(
        "UPDATE Fridge SET food_pieces = food_pieces - :amount WHERE food_id = :food_id",
        {"amount": amount, "food_id": food_id},
    )

    if available_pieces == amount:
        cursor.execute(
            "DELETE FROM Fridge WHERE food_id = :food_id", {"food_id": food_id}
        )

    cursor.connection.commit()

    if available_pieces == amount:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) 모두 꺼냈습니다!")
    else:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) " + str(amount) + "개 꺼냈습니다!")
    print()
    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
