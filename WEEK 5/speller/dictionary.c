// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// Words counter
int wordCounter = 0;

// TODO: Choose number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    int newindex = hash(word);
    node *cursor = table[newindex];
    while (cursor != NULL)
    {
        if (strcasecmp(word, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO: Improve this hash function
    int size = strlen(word);
    if (size >= 3 && size <= 12)
    {
        return toupper(word[0]) - 'A' + size;
    }
    if (size >= 0 && size < 3)
    {
        return size;
    }
    else if (size > 12)
    {

        return 252 + size;
    }

    return size;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // open dictionary file
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("I can't read this file\n");
        return 1;
    }

    // read string from file one at a time
    char word[LENGTH + 1];
    while (fscanf(input, "%s", word) != EOF)
    {

        // create a new node for each word
        node *p = malloc(sizeof(node));
        if (p == NULL)
        {
            return 2;
        }
        strcpy(p->word, word);

        // hash word to otbain a hash value
        unsigned int index = hash(word);

        // instert node into hash table at that location
        p->next = table[index];
        table[index] = p;
        wordCounter++;
    }
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    if (wordCounter > 0)
    {
        return wordCounter;
    }
    return 0;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO
    bool success = true;

    for (int i = 0; i < N; i++)
    {
        node *cursor = table[i];
        while (cursor != NULL)
        {
            node *tmp = cursor;
            cursor = cursor->next;
            free(tmp);
        }
    }
    return success;
}
