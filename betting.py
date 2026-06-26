def chips(x):
    return round(x, 2)

class BettingRound:
    def __init__(self, player, computer, pot=0, player_bet=0, computer_bet=0, current_bet=0):
        self.player = player
        self.computer = computer
        self.pot = chips(pot)
        self.current_bet = chips(current_bet)
        self.player_bet = chips(player_bet)
        self.computer_bet = chips(computer_bet)

    def run(self):
        players = [self.player, self.computer]
        bets = [self.player_bet, self.computer_bet]
        names = ["player", "computer"]

        i = 0
        last_aggressor = None

        while True:
            actor = players[i]
            to_call = chips(self.current_bet - bets[i])

            action, amount = actor.get_action(to_call, self.pot)

            if action == "fold":
                return f"{names[i]}_fold", self.pot

            elif action == "call":
                actual_call = chips(min(to_call, actor.stack))
                bets[i] = chips(bets[i] + actual_call)
                self.pot = chips(self.pot + actual_call)
                actor.stack = chips(max(actor.stack - actual_call, 0))
                if bets[0] == bets[1] and last_aggressor != i:
                    return "continue", self.pot

            elif action == "raise":
                actual_raise = chips(min(amount, actor.stack))
                bets[i] = chips(bets[i] + actual_raise)
                self.pot = chips(self.pot + actual_raise)
                actor.stack = chips(max(actor.stack - actual_raise, 0))
                self.current_bet = bets[i]
                last_aggressor = i

            elif action == "check":
                if bets[0] == bets[1] and last_aggressor is None:
                    if i == 1:
                        return "continue", self.pot

            i = 1 - i