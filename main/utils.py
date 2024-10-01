import random

symbols = [letter for letter in "qwertyuiopasdfghjklzxcvbnm1234567890"]


def generate_password():
    password = random.choice(symbols[:26])
    for i in range(random.randint(7, 11)):
        password += random.choice(symbols)
    return password
