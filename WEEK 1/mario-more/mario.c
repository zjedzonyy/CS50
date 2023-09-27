#include <cs50.h>
#include <stdio.h>

int get_height(void);
void print_grid(int n);

int main(void)
{
    int n = get_height();
    print_grid(n);
}
int get_height(void)
{
    int n;
    do
    {
        n = get_int("Height: ");
    }
    while (n < 1 || n > 8);
    return n;
}
void print_grid(int n)
{
    for (int i = 1; i <= n; i++)
    {
        for (int k = i + 1; k <= n; k++)
        {
            printf(" ");
        }
        for (int j = 1; j <= i; j++)
        {
            printf("#");
        }
        printf("  ");
        for (int l = 1; l <= i; l++)
        {
            printf("#");
        }
        printf("\n");
    }
}