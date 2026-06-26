from treys import Deck, Card
from evaluator import Evaluator
from betting import BettingRound
from player import Player
from computer import Computer

class Game:
    def __init__(self, starting_stack):
        self.evaluator = Evaluator()
        self.player = Player(stack=starting_stack)
        self.computer = Computer(stack=starting_stack)

    def play_hand(self):
        deck = Deck()
        board = []

        # deal
        player_hand = deck.draw(2)
        computer_hand = deck.draw(2)

        print("\n--- YOUR HAND ---")
        Card.print_pretty_cards(player_hand)

        # preflop
        result = BettingRound(self.player, self.computer).run()
        if result == "player_fold": print("You folded"); return
        if result == "computer_fold": print("Computer folded, you win"); return

        # flop
        board += deck.draw(3)
        print("\n--- FLOP ---")
        Card.print_pretty_cards(board)
        result = BettingRound(self.player, self.computer).run()
        if result == "player_fold": print("You folded"); return
        if result == "computer_fold": print("Computer folded, you win"); return

        # turn
        board += deck.draw(1)
        print("\n--- TURN ---")
        Card.print_pretty_cards(board)
        result = BettingRound(self.player, self.computer).run()
        if result == "player_fold": print("You folded"); return
        if result == "computer_fold": print("Computer folded, you win"); return

        # river
        board += deck.draw(1)
        print("\n--- RIVER ---")
        Card.print_pretty_cards(board)
        result = BettingRound(self.player, self.computer).run()
        if result == "player_fold": print("You folded"); return
        if result == "computer_fold": print("Computer folded, you win"); return

        # showdown
        self.showdown(player_hand, computer_hand, board)

    def showdown(self, player_hand, computer_hand, board):
        p_score = self.evaluator.evaluate(player_hand, board)
        c_score = self.evaluator.evaluate(computer_hand, board)

        print("\n--- SHOWDOWN ---")
        print("Your hand:"); Card.print_pretty_cards(player_hand)
        print("Computer hand:"); Card.print_pretty_cards(computer_hand)

        if p_score < c_score: print("You win")
        elif c_score < p_score: print("Computer wins")
        else: print("Chop")

if __name__ == "__main__":
    game = Game()
    while True:
        game.play_hand()
        if input("\nPlay again? (y/n): ") != "y":
            break