if __name__ == '__main__':
    Rainfull_mi = "45, 65, 70.4, 82.6, 20.1, 90.8, 76.1, 30.92, 46.8, 67.1, 79.9"
    num_rainy_months = sum(map(lambda x: float(x) > 75, Rainfull_mi.split(",")))
    print(num_rainy_months)
