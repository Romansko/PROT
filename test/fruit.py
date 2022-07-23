class AppleBasket:
    def __init__(self, color, quantity):
        self.apple_color = color
        self.apple_quantity = quantity

    def increase(self):
        self.apple_quantity += 1

    def __str__(self):
        return f"A basket of {str(self.apple_quantity)} {self.apple_color} apples."


if __name__ == '__main__':
    print("Example1:", AppleBasket("red", 4), "\nExample2:", AppleBasket("blue", 50))
