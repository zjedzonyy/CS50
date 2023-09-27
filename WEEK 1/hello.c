#include <cs50.h>
#include <stdio.h>

int main(void)
{
    string first = get_string("What's your first name?\n ");
    printf("hello, %s\n", first);
}