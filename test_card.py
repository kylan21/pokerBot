from card import Card

def test_card_creation():
    card = Card("A", "s")
    assert card.suit == "s"
    assert card.rank == "A"