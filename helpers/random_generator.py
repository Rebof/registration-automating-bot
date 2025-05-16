import random
import string

class RandomNumberGenerator:
    def __init__(self, length=10):
        self.length = length

    def generate(self):
        number = ''.join(random.choices(string.digits, k=self.length))
        print(f"📱 Generated phone number: {number}")
        return number
