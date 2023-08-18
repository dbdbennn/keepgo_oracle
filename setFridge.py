from tabulate import tabulate  # 이 라인을 추가해주세요.
from isDate import isDate


def setFridge(cursor):
    print()
    print("음식 정보 바꾸기 • 🍅 • 🥕 • 🥬 • 🥩 • 🥚 • 🍇 • 🥔 • 🥗")

    # Oracle에서 데이터를 가져와서 처리
    cursor.execute("SELECT food_name FROM Fridge")
    fridge = [row[0] for row in cursor.fetchall()]

    if len(fridge) == 0:
        print("\n\t  ❗ 음식이 없어 수정할 수 없습니다.")
        return

    name = input("\n\t수정할 음식은? > ")
    while name not in fridge:
        print("\033[31m" + "\n\t\t❗ 입력한 음식이 없습니다." + "\033[0m")
        name = input("\n\t수정할 음식은? > ")

    set_list = [['음식 이름은 "1️" ', '음식 갯수는 "2️" ', '유통기한은 "3️" ']]
    print("\n" + tabulate(set_list, stralign="center", tablefmt="rounded_grid"))

    menu = input("\n\t무엇을 수정하시겠어요? > ")
    while menu not in ["1", "2", "3"]:
        print()
        menu = input("\t다시 선택해주세요 > ")

    if menu == "1":
        new_name = input("\n\t무슨 음식인가요? > ")
        # Oracle SQL로 데이터 업데이트 수행

        cursor.execute(
            "UPDATE Fridge SET food_name = :new_name WHERE food_name = :name",
            {"new_name": new_name, "name": name},
        )
        cursor.connection.commit()
        fridge.remove(name)
        fridge.append(new_name)
        print("\n\t\t" + new_name + "을(를) 수정했습니다!")

    elif menu == "2":
        while True:
            new_num = input("\n\t몇 개인가요? > ")
            if new_num.isdigit():
                new_num = int(new_num)
                break
            else:
                print("\033[31m" + "\n\t❗ 숫자만 입력해주세요." + "\033[0m")

        cursor.execute(
            "UPDATE Fridge SET food_pieces = :new_num WHERE food_name = :name",
            {"new_num": new_num, "name": name},
        )
        cursor.connection.commit()
        print("\n\t\t" + name + "의 갯수를 " + str(new_num) + "개로 수정했습니다!")

    elif menu == "3":
        while True:
            new_date = input("\n\t유통기한(YYYY-MM-DD) > ")
            if isDate(new_date):
                break
            else:
                print("\033[31m" + "\n\t❗ YYYY-MM-DD 형태로 입력해주세요." + "\033[0m")

        cursor.execute(
            "UPDATE Fridge SET expiration_date = TO_DATE(:new_date, 'YYYY-MM-DD') WHERE food_name = :name",
            {"new_date": new_date, "name": name},
        )
        cursor.connection.commit()
        print("\n\t\t" + name + "의 유통기한을 " + new_date + "로 수정했습니다!")
        print()
        inputMeun = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
        if str(type(inputMeun)) == "<class 'str'>":
            return
