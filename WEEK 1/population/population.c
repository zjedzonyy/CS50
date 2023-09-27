#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // TODO: Prompt for start size
    int x = get_int("What's the start size? ");
    while ( x < 9)
    {
        x = get_int("What's the start size? ");
    }
    // TODO: Prompt for end size
    int y = get_int("What's the end size? ");
    while (y < x)
    {
        y = get_int("What's the end size? ");
    }
    // TODO: Calculate number of years until we reach threshold
    int i = 0;
    while (x < y)
    {
       x = x + (x / 3) - (x / 4);
        i++;
    }

    printf("Years: %i\n", i);
}