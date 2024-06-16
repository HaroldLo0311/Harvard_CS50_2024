while True:
    try:
        s = int(input("Height: "))
        if s > 0 and s < 9:
            break
    except ValueError:
        pass

for i in range(1, s + 1):
    for j in range(i, i + 1):
        print(" "*(s-j), end="")
        print("#"*j)
