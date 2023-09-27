# TODO
from cs50 import get_string


def main():
    text = get_string("Text:")

    numbers = count_letters(text)

    words = count_words(text)

    sentences = count_sentences(text)

    calculation = (
        float(0.0588 * numbers / words * 100) - (0.296 * sentences / words * 100) - 15.8
    )
    index = int(round(calculation))

    if index < 1:
        print("Before Grade 1")
        return 0
    if index >= 16:
        print("Grade 16+")
        return 0
    else:
        print(f"Grade {index}")


def count_letters(text):
    count = 0

    for character in text:
        if character.isalpha():
            count += 1

    return count


def count_words(text):
    count = 1

    for character in text:
        if character == " ":
            count += 1

    return count


def count_sentences(text):
    count = 0

    for character in text:
        if character == "." or character == "!" or character == "?":
            count += 1
    return count


main()
