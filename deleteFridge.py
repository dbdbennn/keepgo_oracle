import strChanger as sc


def deleteFridge(cursor):
    print()
    print(sc.str_Cyan("냉장고에서 음식 꺼내기 - 🍅 - 🥕 - 🥬 - 🥩 - 🥚 - 🍇 - 🥔 - 🍠"))

    cursor.execute("SELECT food_name, food_pieces FROM Fridge")
    fridge_data = {row[0]: row[1] for row in cursor.fetchall()}

    if not fridge_data:
        print("\n\t  \033[31m❗ 음식이 없어 꺼낼 수 없습니다.\033[0m")
        return

    name = input("\n\t\t꺼낼 음식은? > ")
    while name not in fridge_data:
        print(sc.str_Red("\n\t\t\033[31m❗ 입력한 음식이 없습니다.\033[0m"))
        name = input("\n\t\t꺼낼 음식은? > ")

    available_pieces = fridge_data[name]

    amount = int(input("\n\t\t꺼낼 음식의 갯수는? > "))
    while amount <= 0 or amount > available_pieces:
        if amount <= 0:
            print(sc.str_Red("\n\t\t\033[31m❗ 입력한 음식의 갯수가 올바르지 않습니다.\033[0m"))
        else:
            print(sc.str_Red("\n\t\t\033[31m❗ 초과하여 꺼낼 수 없습니다.\033[0m"))
        amount = int(input("\n\t\t꺼낼 음식의 갯수는? > "))

    cursor.execute(
        "UPDATE Fridge SET food_pieces = food_pieces - :amount WHERE food_name = :name",
        {"amount": amount, "name": name},
    )

    if available_pieces == amount:
        cursor.execute("DELETE FROM Fridge WHERE food_name = :name", {"name": name})

    cursor.connection.commit()

    if available_pieces == amount:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) 모두 꺼냈습니다!")
    else:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) " + str(amount) + "개 꺼냈습니다!")
    print()
    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
