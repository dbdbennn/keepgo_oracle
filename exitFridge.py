import strChanger as sc


def exitFridge():
    print()
    isExit = input(
        sc.str_Green(
            """\t정말 keep Go를 나가시겠습니까? 🥺

    \t나가시겠다면 아무 키를,
    \t메뉴로 돌아가려면 1을 입력하세요 > """
        )
    )

    return isExit
