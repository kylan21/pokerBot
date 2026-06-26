from treys import Deck, Card, Evaluator
from betting import BettingRound
from player import Player
from computer import Computer

SMALL_BLIND = 0.5
BIG_BLIND = 1.0

def chips(x):
    """Round to 2 decimal places to avoid float drift."""
    return round(x, 2)

class Game:
    def __init__(self, starting_stack):
        self.player = Player(stack=chips(starting_stack))
        self.computer = Computer(stack=chips(starting_stack))
        self.hand_num = 0

    def play_hand(self):
        if self.player.stack <= 0 or self.computer.stack <= 0:
            winner = "Computer" if self.player.stack <= 0 else "You"
            print(f"\nGame over — {winner} win!")
            return False

        deck = Deck()
        board = []
        pot = 0

        print(f"\n{'='*40}")
        print(f"Your stack: {self.player.stack} | Computer stack: {self.computer.stack}")

        # post blinds — alternate who is SB
        if self.hand_num % 2 == 0:
            sb_player, bb_player = self.player, self.computer
            sb_name, bb_name = "You", "Computer"
        else:
            sb_player, bb_player = self.computer, self.player
            sb_name, bb_name = "Computer", "You"

        sb = chips(min(SMALL_BLIND, sb_player.stack))
        bb = chips(min(BIG_BLIND, bb_player.stack))

        sb_player.stack = chips(max(sb_player.stack - sb, 0))
        bb_player.stack = chips(max(bb_player.stack - bb, 0))
        pot = chips(sb + bb)

        print(f"\n{sb_name} posts SB: {sb} | {bb_name} posts BB: {bb} | Pot: {pot}")

        # player=0, computer=1; SB acts first preflop
        if self.hand_num % 2 == 0:
            # player is SB
            player_bet, computer_bet = sb, bb
            preflop_first_actor = 0
        else:
            # computer is SB
            player_bet, computer_bet = bb, sb
            preflop_first_actor = 1
        self.hand_num += 1

        player_hand = deck.draw(2)
        computer_hand = deck.draw(2)

        print("\n--- YOUR HAND ---")
        Card.print_pretty_cards(player_hand)

        # preflop — SB acts first, BB has option if SB just calls
        result, pot = BettingRound(
            self.player, self.computer, pot=pot,
            player_bet=player_bet, computer_bet=computer_bet,
            current_bet=BIG_BLIND, first_actor=preflop_first_actor
        ).run()
        if self.handle_fold(result, pot): return True

        # flop
        board += deck.draw(3)
        print("\n--- FLOP ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return True

        # turn
        board += deck.draw(1)
        print("\n--- TURN ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return True

        # river
        board += deck.draw(1)
        print("\n--- RIVER ---")
        Card.print_pretty_cards(board)
        result, pot = BettingRound(self.player, self.computer, pot=pot).run()
        if self.handle_fold(result, pot): return True

        self.showdown(player_hand, computer_hand, board, pot)
        return True

    def handle_fold(self, result, pot):
        if result == "player_fold":
            self.computer.stack = chips(self.computer.stack + pot)
            print("You folded, computer wins pot")
            return True
        if result == "computer_fold":
            self.player.stack = chips(self.player.stack + pot)
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
            self.player.stack = chips(self.player.stack + pot)
            print("You win")
        elif c_score < p_score:
            self.computer.stack = chips(self.computer.stack + pot)
            print("Computer wins")
        else:
            half = chips(pot / 2)
            self.player.stack = chips(self.player.stack + half)
            self.computer.stack = chips(self.computer.stack + half)
            print("Chop")

if __name__ == "__main__":
    game = Game(100.0)
    while game.play_hand():
        pass