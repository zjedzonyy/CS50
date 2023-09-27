# TODO
def get_height():
    while True:
        try:
            n = int(input("Height: "))
            if n >= 1 and n <= 8:
                return n
        except ValueError:
            print("Not an integer")


def print_grid(n):
    for i in range(n):
        for k in range(n - 1 - i):
            print(" ", end="")
        for j in range(i + 1):
            print("#", end="")
        print()


def main():
    n = get_height()
    print_grid(n)


main()
