import strChanger as sc


def deleteFridge(cursor):
    print()
    print(sc.str_Cyan("냉장고에서 음식 꺼내기 - 🍅 - 🥕 - 🥬 - 🥩 - 🥚 - 🍇 - 🥔 - 🍠"))

    # Oracle에서 데이터를 가져와서 처리
    cursor.execute("SELECT food_name FROM Fridge")
    fridge = [row[0] for row in cursor.fetchall()]

    if len(fridge) == 0:
        print("\n\t  ❗ 음식이 없어 꺼낼 수 없습니다.")
    name = input("\n\t\t꺼낼 음식은? > ")
    while name not in fridge:
        print(sc.str_Red("\n\t\t❗ 입력한 음식이 없습니다."))
        name = input("\n\t\t꺼낼 음식은? > ")

    amount = int(input("\n\t\t꺼낼 음식의 갯수는? > "))
    while amount <= 0:
        print(sc.str_Red("\n\t\t❗ 입력한 음식의 갯수가 올바르지 않습니다."))
        amount = int(input("\n\t\t꺼낼 음식의 갯수는? > "))

    # Oracle SQL로 데이터 업데이트 수행

    cursor.execute(
        "SELECT food_pieces FROM Fridge WHERE food_name = :name", {"name": name}
    )
    current_pieces = cursor.fetchone()[0]
    if amount >= current_pieces:
        cursor.execute("DELETE FROM Fridge WHERE food_name = :name", {"name": name})
    else:
        cursor.execute(
            "UPDATE Fridge SET food_pieces = food_pieces - :amount WHERE food_name = :name",
            {"amount": amount, "name": name},
        )
    cursor.connection.commit()

    if amount >= current_pieces:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) 모두 꺼냈습니다!")
    else:
        print("\n\t\t" + sc.str_Blue(name) + "을(를) " + str(amount) + "개 꺼냈습니다!")
