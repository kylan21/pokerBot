from dataclasses import dataclass

@dataclass(frozen=True)
class Card:
    rank: str
    suit: str

    def __str__(self):
        return f"{self.rank}{self.suit}"