#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <ctype.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Get a text
    string text = get_string("Text: ");

    // Calculate letters // chars from a to z  and from A to Z ONLY
    int numbers = count_letters(text);

    // Calculate words // Sequence of characters separated by spaces
    int words = count_words(text);

    // Calculate sentences // Any occurrence of a period, exclamation point, or question mark indicates the end of a sentence
    int sentences = count_sentences(text);

    // Calculate grade level
    float calculation = (0.0588 * numbers / words * 100) - (0.296 * sentences / words * 100) - 15.8;
    int index = round(calculation);

    //Print the grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
        return 0;
    }
    if (index >= 16)
    {
        printf("Grade 16+\n");
        return 0;
    }
    else
    {
        printf("Grade %i\n", index);
    }
}

// Calculate number of letters
int count_letters(string text)
{
    int numbers = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (isalpha(text[i]))
        {
            numbers += 1;
        }
    }
    return numbers;
}

// Calculate number of words
int count_words(string text)
{
    int words = 1;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == ' ')
        {
            words++;
        }
    }
    return words;
}

// Calculate number of sentences
int count_sentences(string text)
{
    int sentences = 0;
    for (int i = 0; i < strlen(text); i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            sentences++;
        }
    }
    return sentences;
}