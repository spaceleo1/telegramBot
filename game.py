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

    def has_face(self):
        return 11 <= self.number <= 13

    def __str__(self):
        return f"{self.get_number()} {self.get_suit()}"


class Game:
    def __init__(self):
        self.croupier_box = []
        self.box = []
        self.deck = []

        self.doubled = False
        self.finished = True

    def start(self):
        self.generate_deck()

        for i in range(2):
            self.add_card(self.box)

        self.add_card(self.croupier_box)
        self.finished = False
        self.doubled = False

    def add_card(self, box):
        box.append(self.deck.pop())

    def generate_deck(self):
        self.deck = []
        for i in range(6):
            for suit in range(4):
                for number in range(1, 14):
                    self.deck.append(Card(suit, number))
        random.shuffle(self.deck)

    def get_box_opt(self, box: list) -> int:
        sm = 0
        cnt = 0
        for card in box:
            if card.number == 1:
                cnt += 1
            elif card.has_face():
                sm += 10
            else:
                sm += card.number
        sm += cnt
        while cnt > 0 and sm + 10 <= 21:
            sm += 10
            cnt -= 1
        return sm

    def get_box_max(self, box: list) -> int:
        sm = 0
        for card in box:
            if card.number == 1:
                sm += 11
            elif card.has_face():
                sm += 10
            else:
                sm += card.number

        return sm

    def get_box_min(self, box: list) -> int:
        sm = 0
        for card in box:
            if card.has_face():
                sm += 10
            else:
                sm += card.number

        return sm

    def hit(self):
        top_card = self.deck.pop()
        self.box.append(top_card)

        if self.doubled:
            return False

        return self.get_box_min(self.box) < 21

    def stand(self):
        self.finish()

    def double_down(self):
        self.doubled = True

    def finish(self):
        self.finished = True

        if self.get_box_min(self.box) > 21:
            return -1

        while self.get_box_opt(self.croupier_box) < 17:
            self.add_card(self.croupier_box)

        if self.get_box_min(self.croupier_box) > 21:
            return 1

        croupier_points = self.get_box_opt(self.croupier_box)
        player_points = self.get_box_opt(self.box)

        if croupier_points == player_points:
            return 0
        elif croupier_points > player_points:
            return -1
        else:
            return 1
