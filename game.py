from treys import Deck, Card, Evaluator
from betting import BettingRound
from player import Player
from computer import Computer

class Game:
    def __init__(self, starting_stack):
        self.player = Player(stack=starting_stack)
        self.computer = Computer(stack=starting_stack)

    def play_hand(self):
        deck = Deck()
        board = []
        pot = 0

        print(f"Your stack: {self.player.stack} | Computer stack: {self.computer.stack}")

        # deal
        player_hand = deck.draw(2)
        computer_hand = deck.draw(2)

        print("\n--- YOUR HAND ---")
        Card.print_pretty_cards(player_hand)

        # preflop
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return

        # flop
        board += deck.draw(3)
        print("\n--- FLOP ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return

        # turn
        board += deck.draw(1)
        print("\n--- TURN ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return

        # river
        board += deck.draw(1)
        print("\n--- RIVER ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return

        # showdown
        self.showdown(player_hand, computer_hand, board, pot)

    def handle_fold(self, result, pot):
        if result == "player_fold":
            self.computer.stack += pot
            print("You folded, computer wins pot")
            return True
        if result == "computer_fold":
            self.player.stack += pot
            print("Computer folded, you win pot")
            return True
        return False

    def showdown(self, player_hand, computer_hand, board, pot):
        evaluator = Evaluator()
        p_score = evaluator.evaluate(board, player_hand)
        c_score = evaluator.evaluate(board, computer_hand)

        print("\n--- SHOWDOWN ---")
        print("Your hand:"); Card.print_pretty_cards(player_hand)
        print("Computer hand:"); Card.print_pretty_cards(computer_hand)

        if p_score < c_score:
            self.player.stack += pot
            print("You win")
        elif c_score < p_score:
            self.computer.stack += pot
            print("Computer wins")
        else:
            self.player.stack += pot/2
            self.computer.stack += pot/2
            print("Chop")

if __name__ == "__main__":
    game = Game(100.0)
    while True:
        game.play_hand()
        if input("\nPlay again? (y/n): ") != "y":
            break