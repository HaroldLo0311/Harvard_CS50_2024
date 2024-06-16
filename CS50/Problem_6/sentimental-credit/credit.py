
def main():
    while True:
        try:
            number = input("Number: ")
            if number.isdigit():
                break
            else:
                pass
        except ValueError:
            pass
    sum = 0
    number_len = len(number)

    for i in range(number_len - 2, -1, -2):
        if (int(number[i]) >= 5):
            sum += 2 * (int(number[i]) - 5) + 1
        else:
            sum += 2 * int(number[i])
    for i in range(number_len - 1, -1, -2):
        sum += int(number[i])

    if (sum % 10 == 0):
        if (len(number) == 15 and (number[0:2] == '34' or number[0:2] == '37')):
            print("AMEX")
            return 0
        elif (len(number) == 16 and (number[0:2] == '51' or number[0:2] == '52' or number[0:2] == '53' or number[0:2] == '54' or number[0:2] == '55')):
            print("MASTERCARD")
            return 0
        elif (len(number) == 13 or len(number) == 16 and (number[0] == '4')):
            print("VISA")
            return 0
        else:
            print("INVALID")
            return 1
    else:
        print("INVALID")
        return 1


main()
