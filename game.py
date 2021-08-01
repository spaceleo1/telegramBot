from numpy import random

suits = {
    0: 'черви',
    1: 'пики',
    2: 'бубны',
    3: 'трефы'
}

numbers = range(1, 14)


class Card:
    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def get_suit(self):
        return suits[self.suit]

    def get_number(self):
        return numbers[self.number]

    def __str__(self):
        return f"{self.get_number()} {self.get_suit()}"


class Game:
    def __init__(self):
        self.generate_deck()

        self.state = 0
        self.current_sum = [0, 0]

    def generate_deck(self):
        self.deck = []
        for suit in range(4):
            for number in range(1, 14):
                self.deck.append(Card(suit, number))
        random.shuffle(self.deck)

