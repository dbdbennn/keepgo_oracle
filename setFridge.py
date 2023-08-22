from tabulate import tabulate
from isDate import isDate
from datetime import datetime
import strChanger as sc


def setFridge(cursor):
    print()
    print("음식 정보 바꾸기 • 🍅 • 🥕 • 🥬 • 🥩 • 🥚 • 🍇 • 🥔 • 🥗")

    cursor.execute(
        "SELECT food_id, food_name, expiration_date, food_pieces FROM Fridge"
    )
    fridge_data = cursor.fetchall()

    if len(fridge_data) == 0:
        print("\n\t  \033[31m❗ 음식이 없어 수정할 수 없습니다.\033[0m")
        print()
        inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
        if isinstance(inputMenu, str):
            return

    name = input("\n\t수정할 음식은? > ")
    matching_items = [(row[0], row[1]) for row in fridge_data if row[1] == name]

    while True:
        if len(matching_items) == 0:
            print("\033[31m" + "\n\t\t❗ 입력한 음식이 없습니다." + "\033[0m")
            name = input("\n\t수정할 음식은? > ")
            matching_items = [(row[0], row[1]) for row in fridge_data if row[1] == name]
        else:
            break

    if len(matching_items) > 1:
        table_headers = ["food_id", "음식 이름", "음식 갯수", "유통기한"]
        table_data = [
            (row[0], row[1], row[3], row[2].strftime("%Y-%m-%d"))
            for row in fridge_data
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
        food_id = input("\n\t수정할 음식의 ID를 입력하세요 > ")
        while not food_id.isdigit() or int(food_id) not in [
            item[0] for item in matching_items
        ]:
            print("\033[31m" + "\n\t\t❗ 올바른 ID를 입력하세요." + "\033[0m")
            food_id = input("\n\t수정할 음식의 ID를 입력하세요 > ")
        food_id = int(food_id)
    else:
        food_id = matching_items[0][0]

    set_list = [['음식 이름은 "1" ', '음식 갯수는 "2" ', '유통기한은 "3" ']]
    print("\n" + tabulate(set_list, stralign="center", tablefmt="rounded_grid"))

    menu = input("\n\t무엇을 수정하시겠어요? > ")
    while menu not in ["1", "2", "3"]:
        print()
        menu = input("\t다시 선택해주세요 > ")

    if menu == "1":
        new_name = input("\n\t무슨 음식인가요? > ")
        cursor.execute(
            "UPDATE Fridge SET food_name = :new_name WHERE food_id = :food_id",
            {"new_name": new_name, "food_id": food_id},
        )
        cursor.connection.commit()
        print(
            "\n\t"
            + sc.str_Yellow(name)
            + "을(를) "
            + sc.str_Blue(new_name)
            + "(으)로 수정했습니다!"
        )

    elif menu == "2":
        while True:
            new_num = input("\n\t몇 개인가요? > ")
            if new_num.isdigit():
                new_num = int(new_num)
                break
            else:
                print("\033[31m" + "\n\t❗ 숫자만 입력해주세요." + "\033[0m")

        if new_num == 0:
            cursor.execute(
                "DELETE FROM Fridge WHERE food_id = :food_id", {"food_id": food_id}
            )
            cursor.connection.commit()
            print("\n\t" + sc.str_Blue(name) + "을(를) 삭제했습니다!")
        else:
            cursor.execute(
                "UPDATE Fridge SET food_pieces = :new_num WHERE food_id = :food_id",
                {"new_num": new_num, "food_id": food_id},
            )
            cursor.connection.commit()
            print("\n\t" + sc.str_Blue(name) + "의 갯수를 " + str(new_num) + "개로 수정했습니다!")

    elif menu == "3":
        while True:
            new_date = input("\n\t유통기한(YYYY-MM-DD) > ")
            if isDate(new_date):
                break
            else:
                print("\033[31m" + "\n\t❗ YYYY-MM-DD 형태로 입력해주세요." + "\033[0m")
        cursor.execute(
            "UPDATE Fridge SET expiration_date = TO_DATE(:new_date, 'YYYY-MM-DD') WHERE food_id = :food_id",
            {"new_date": new_date, "food_id": food_id},
        )
        cursor.connection.commit()
        print("\n\t" + sc.str_Blue(name) + "의 유통기한을 " + new_date + "로 수정했습니다!")

    print()
    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
