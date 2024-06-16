def main():
    text = input("Text: ")
    # Index i, Letters: l, Words: w, Sentences: s, Level: level
    i, l, w, s = 0, 0, 0, 0
    text_len = len(text)

    while (i < text_len):
        # Find word that's not end of the sentence
        if (text[i] == " "):
            if (text[i - 1] != "." and text[i - 1] != "?"):
                w += 1
        # Find letter
        elif (text[i].isalpha()):
            l += 1
        # Find end of the sentence
        elif (text[i] == "?" or text[i] == "."):
            w += 1
            s += 1
        i += 1
    L = l / w * 100
    S = s / w * 100
    level = 0.0588 * L - 0.296 * S - 15.8
    # Print out grade
    if (level < 0.5):
        print("Before Grade 1")
    elif (level < 1.5):
        print("Grade 1")
    elif (level < 2.5):
        print("Grade 2")
    elif (level < 3.5):
        print("Grade 3")
    elif (level < 4.5):
        print("Grade 4")
    elif (level < 5.5):
        print("Grade 5")
    elif (level < 6.5):
        print("Grade 6")
    elif (level < 7.5):
        print("Grade 7")
    elif (level < 8.5):
        print("Grade 8")
    elif (level < 9.5):
        print("Grade 9")
    elif (level < 10.5):
        print("Grade 10")
    else:
        print("Grade 16+")


main()
