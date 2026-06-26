class BettingRound:
    def __init__(self, player, computer, pot=0):
        self.player = player
        self.computer = computer
        self.pot = pot
        self.current_bet = 0
        self.player_bet = 0
        self.computer_bet = 0

    def run(self):
        # player acts first postflop, computer acts first preflop (dealer)
        # keep it simple for now, player always acts first

        players = [self.player, self.computer]
        bets = [self.player_bet, self.computer_bet]
        names = ["player", "computer"]

        i = 0  # whose turn
        last_aggressor = None

        while True:
            actor = players[i]
            to_call = round(self.current_bet - bets[i], 1)

            action, amount = actor.get_action(to_call, self.pot)

            if action == "fold":
                return f"{names[i]}_fold", self.pot

            elif action == "call":
                bets[i] += to_call
                self.pot += to_call
                actor.stack -= to_call
                # if both have acted and bets are equal, round is over
                if bets[0] == bets[1] and last_aggressor != i:
                    return "continue", self.pot

            elif action == "raise":
                bets[i] += amount
                self.pot += amount
                actor.stack -= amount
                self.current_bet = bets[i]
                last_aggressor = i

            elif action == "check":
                if bets[0] == bets[1] and last_aggressor is None:
                    if i == 1:  # both checked
                        return "continue", self.pot

            i = 1 - i  # swap turns