import csv
import sys


def main():

    # Check for command-line usage
    from sys import argv
    if (len(argv) != 3):
        print("Error: wrong command-line number!")
        return 1

    # Read database file into a variable
    database_dict = []
    STR = []
    STR_num = 0
    # Read in STR
    with open(argv[1]) as file:
        reader = csv.DictReader(file)
        STR = (reader.fieldnames)
    STR_num = len(STR) - 1
    # Read in database as dict
    with open(argv[1]) as file:
        reader = csv.DictReader(file)
        for row in reader:
            database_dict.append(row)
    # Read DNA sequence file into a list variable
    input = []
    dna_seq = []
    with open(argv[2]) as file:
        input.append(file.read())
    for i in range(0, len(input[0])):
        if input[0][i] != "\n":
            dna_seq.append(input[0][i])
    # Find longest match of each STR in DNA sequence
    longest_num = {}
    for str in STR:
        str_list = []
        if str != "name":
            for x in str:
                str_list.append(x)
            longest_num[str] = longest_match(dna_seq, str_list)
    # Check database for matching profiles
    STR = STR[1:]
    # Run through all people
    for i in range(len(database_dict)):
        state = 1
        # Run through all str, if all number equals, print
        for str_check in STR:
            if int(longest_num[str_check]) != int(database_dict[i][str_check]):
                state = 0
        if (state == 1):
            print(database_dict[i]["name"])
            break
    print("No match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
