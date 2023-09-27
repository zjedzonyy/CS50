class Jar:
    def __init__(self, capacity=12):
        if capacity < 1:
            raise Exception("Sorry, no numbers below zero ")
        self.cookies = capacity
        self.n = 0

    def __str__(self):
        return "🍪" * self.n

    def deposit(self, n):
        if self.n + n > self.cookies:
            raise Exception("Too much brooo ")
        self.n += n

    def withdraw(self, n):
        if self.n < n:
            raise Exception("There are less cookies than you want to remove ")
        self.n -= n

    @property
    def capacity(self):
        return self.cookies

    @property
    def size(self):
        return self.n

def main():
    jar = Jar(9)
    jar.deposit(3)
    print(jar)
    jar.withdraw(2)
    print(jar)


main()