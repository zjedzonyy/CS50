# TODO
def main():
    cents = get_cents()
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 0.25
    cents = round(cents, 2)

    dimes = calculate_dimes(cents)
    cents = cents - dimes * 0.10
    cents = round(cents, 2)

    nickels = calculate_nickels(cents)
    cents = cents - nickels * 0.05
    cents = round(cents, 2)

    pennies = calculate_pennies(cents)
    cents = cents - pennies * 0.01
    cents = round(cents, 2)

    coins = quarters + dimes + nickels + pennies

    print(f"{coins}")


def get_cents():
    while True:
        try:
            n = float(input("Owed: "))
            if n > 0:
                break
        except ValueError:
            print("Not an integer")
    return n


def calculate_quarters(cents):
    quarters = 0.25
    count = 0

    while cents >= quarters:
        cents -= quarters
        count += 1

    return count


def calculate_dimes(cents):
    dimes = 0.10
    count = 0

    while cents >= dimes:
        cents -= dimes
        count += 1

    return count


def calculate_nickels(cents):
    nickels = 0.05
    count = 0

    while cents >= nickels:
        cents -= nickels
        count += 1

    return count


def calculate_pennies(cents):
    pennies = 0.01
    count = 0

    while cents >= pennies:
        cents -= pennies
        count += 1

    return count


main()
