class BankAccount:
    def __init__(self, name, amount):
        self.name = name
        self.amt = amount

    def __str__(self):
        return f"Your account, {self.name}, has {str(self.amt)} dollars."


if __name__ == '__main__':
    t1 = BankAccount("Bob", 100)
    print(t1)
