while True:
    try:
        s = int(input("Height: "))
        if s < 9 and s > 0:
            break
    except ValueError:
        pass


for i in range(1, s + 1):
    print(" "*(s-i), end="")
    print("#"*(i), end="  ")
    print("#"*i)
