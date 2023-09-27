#include <cs50.h>
#include <stdio.h>

long get_number(void);
long calculate_digits(long number);
long calculate_addition(long number);
long calculate_validation(long number);

int main(void)
{
    long number = get_number();
    // STEP 1.1
    long digits = calculate_digits(number);
    
    // STEP 1.2
    int sum = calculate_addition(digits);
    // STEP 2
    // STEP 3
    printf("VALID\n");

}

long get_number(void)
{
        long i = get_long("What's the card number? ");
}


int calculate_digits(void);
{

}

int calculate_addition(void);
{

}