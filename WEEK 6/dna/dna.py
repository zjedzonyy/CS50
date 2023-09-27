import csv
import sys


def main():
    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        sys.exit("Usage: [1] program, [2] CSV file, [3] DNA to identify")

    # TODO: Read database file into a variable
    database = []

    with open(sys.argv[1]) as f:
        reader = csv.DictReader(f)
        for name in reader:
            database.append(name)

    # TODO: Read DNA sequence file into a variable
    DNA = []

    with open(sys.argv[2]) as f:
        DNA = f.read()

    # TODO: Find longest match of each STR in DNA sequence
    # sequence = database[0]['AGATC']
    sequence = DNA

    ## save all the nucs in the list
    ### ['AGATC', 'TTTTTTCT', 'AATG', 'TCTAG', 'GATA', 'TATC', 'GAAA', 'TCTG']
    key_list = list(database[0].keys())

    # save all the numbers of nucs for each name
    ## ['15', '49', '38', '5', '14', '44', '14', '12']
    ##lock_list = list(database[0].values())
    ##print(lock_list[1:])

    # save how many times AGATC repeated in the DNA
    ## [46, 49, 48, 29, 15, 5, 28, 41]
    results = []
    for key in key_list[1:]:
        subsequence = key
        Nuk_1 = longest_match(sequence, subsequence)
        results.append(Nuk_1)

    # TODO: Check database for matching profiles
    # for i in range(len(database)):

    winners = []
    for i in range(len(database)):
        values = list(database[i].values())[1:]
        winners.append(values)

    count = 0
    required = len(key_list[1:])
    for i in range(len(database)):
        for j in range(len(key_list[1:])):
            if int(winners[i][j]) == int(results[j]):
                count += 1
                if count == required:
                    print(f'{database[i]["name"]}')
                    break
            else:
                count = 0
        if count == required:
            break
    else:
        print("No match")


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
