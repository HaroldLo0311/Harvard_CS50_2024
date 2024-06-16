def main():
    number = 0
    while True:
        try:
            change = float(input("Change: "))
            if (change > 0):
                break
            elif (change == 0):
                print("0")
                return 0
            else:
                pass
        except ValueError:
            pass
    change = change * 100
    while (change > 0):
        if change >= 25:
            change -= 25
        elif change >= 10:
            change -= 10
        elif change >= 5:
            change -= 5
        else:
            change -= 1
        number += 1
    print(number)
    return 0


main()
