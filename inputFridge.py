import isDate as id
import strChanger as sc


def inputFridge(cursor):
    print("\n냉장고에 음식 넣기 + 🍅 + 🥕 + 🥬 + 🥩 + 🥚 + 🍇 + 🥔 + 🧃")

    while True:
        name = input("\n\t무슨 음식인가요? > ")

        if not name.strip():  # Check if the input is empty or just whitespace
            print("\n\t\033[31m❗ 음식 이름을 입력해주세요.\033[0m")
            continue
        else:
            break  # Proceed if the food_name is unique

    while True:
        try:
            food_pieces = int(input("\n\t갯수는요? > "))
            break
        except ValueError:
            print("\n\t\033[31m❗ 숫자만 입력해주세요.\033[0m")

    while True:
        expiration_date = input("\n\t유통기한은요? (YYYY-MM-DD) > ")
        if id.isDate(expiration_date):
            break
        else:
            print("\n\t\033[31m❗ YYYY-MM-DD 형태로 입력해주세요.\033[0m")

    cursor.execute(
        """INSERT INTO 
            Fridge (food_name, expiration_date, food_pieces) 
            VALUES (:food_name, TO_DATE(:expiration_date, 'YYYY-MM-DD'), :food_pieces)""",
        {
            "food_name": name,
            "expiration_date": expiration_date,
            "food_pieces": food_pieces,
        },
    )
    cursor.connection.commit()
    print("\n\t\t" + sc.str_Blue(name) + "을(를) 넣었습니다!")
    print()
    inputMenu = input("\t 엔터를 누르면 메뉴로 돌아갑니다 ⬇️  ")
    if isinstance(inputMenu, str):
        return
