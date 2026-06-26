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
            to_call = self.current_bet - bets[i]

            action, amount = actor.get_action(to_call, self.pot)

            if action == "fold":
                return f"{names[i]}_fold", self.pot

            elif action == "call":
                bets[i] += to_call
                self.pot += to_call
                actor.stack -= to_call
                # if both have acted and bets are