#include <cs50.h>
#include <stdio.h>

int get_cents(void);
int calculate_quarters(int cents);
int calculate_dimes(int cents);
int calculate_nickels(int cents);
int calculate_pennies(int cents);

int main(void)
{
    // Ask how many cents the customer is owed
    int cents = get_cents();

    // Calculate the number of quarters to give the customer
    int quarters = calculate_quarters(cents);
    cents = cents - quarters * 25;

    // Calculate the number of dimes to give the customer
    int dimes = calculate_dimes(cents);
    cents = cents - dimes * 10;

    // Calculate the number of nickels to give the customer
    int nickels = calculate_nickels(cents);
    cents = cents - nickels * 5;

    // Calculate the number of pennies to give the customer
    int pennies = calculate_pennies(cents);
    cents = cents - pennies * 1;

    // Sum coins
    int coins = quarters + dimes + nickels + pennies;

    // Print total number of coins to give the customer
    printf("%i\n", coins);
}

int get_cents(void)
{
    // TODO
    int n;
    {
        do
        {
            n = get_int("Owed: ");
        }
        while (n < 0);
        return n;
    }
}

int calculate_quarters(int cents)
{
    // TODO
    int i = 25;
    if (i <= cents)
    {
        for (int j = 25; j <= cents; j++)
        {
            cents = cents / 25;
        }
        return cents;
    }
    else
    {
        cents = 0;
        return cents;
    }
}

int calculate_dimes(int cents)
{
    // TODO
    int i = 10;
    if (i <= cents)
    {
        for (int j = 10; j <= cents; j++)
        {
            cents = cents / 10;
        }
        return cents;
    }
    else
    {
        cents = 0;
        return cents;
    }
}

int calculate_nickels(int cents)
{
    // TODO
    int i = 5;
    if (i <= cents)
    {
        for (int j = 5; j <= cents; j++)
        {
            cents = cents / 5;
        }
        return cents;
    }
    else
    {
        cents = 0;
        return cents;
    }
}

int calculate_pennies(int cents)
{
    // TODO
    int i = 1;
    if (i <= cents)
    {
        for (int j = 1; j <= cents; j++)
        {
            cents = cents / 1;
        }
        return cents;
    }
    else
    {
        cents = 0;
        return cents;
    }
}
