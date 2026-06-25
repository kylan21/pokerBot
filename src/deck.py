import random
from card import Card

class Deck:
        RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        SUITS = ['s', 'h', 'd', 'c']

        def __init__(self):
                self.cards = [Card(rank, suit) for suit in self.SUITS for rank in self.RANKS]

        def shuffle(self):
                random.shuffle(self.cards)
        def draw(self):
                if len(self.cards) == 0:
                        raise ValueError("empty deck")
                return self.cards.pop()