from treys import Deck, Evaluator, Card

deck = Deck()

board = deck.draw(5)
player1_hand = deck.draw(2)
player2_hand = deck.draw(2)

Card.print_pretty_cards(board)
Card.print_pretty_cards(player1_hand)
Card.print_pretty_cards(player2_hand)