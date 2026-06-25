from deck import Deck

def test_deck_size():
    deck = Deck()
    assert len(deck.cards) == 52

def test_deck_draw():
    deck = Deck()
    card = deck.draw()
    assert len(deck.cards) == 51

def test_deck_draw_empty():
    deck = Deck()
    for _ in range(52):
        deck.draw()
    try:
        deck.draw()
        assert False  # should never reach here
    except ValueError:
        pass

def test_deck_shuffle():
    deck1 = Deck()
    deck2 = Deck()
    deck2.shuffle()
    assert deck1.cards != deck2.cards  # extremely unlikely to be equal after shuffle
