def chips(x):
    return round(x, 2)

class BettingRound:
    def __init__(self, player, computer, pot=0, player_bet=0, computer_bet=0, current_bet=0, first_actor=0):
        self.player = player
        self.computer = computer
        self.pot = chips(pot)
        self.current_bet = chips(current_bet)
        self.player_bet = chips(player_bet)
        self.computer_bet = chips(computer_bet)
        self.first_actor = first_actor

    def run(self):
        players = [self.player, self.computer]
        bets = [self.player_bet, self.computer_bet]
        names = ["player", "computer"]

        i = self.first_actor
        last_aggressor = None
        has_acted = set()

        while True:
            actor = players[i]
            opponent = players[1 - i]
            to_call = chips(self.current_bet - bets[i])

            # if actor has no stack left, skip their action
            if actor.stack == 0:
                has_acted.add(i)
                i = 1 - i
                # if both are all-in or opponent already called, end round
                if opponent.stack == 0 or bets[0] == bets[1]:
                    return "continue", self.pot
                continue

            action, amount = actor.get_action(to_call, self.pot)

            # calling nothing is a check
            if action == "call" and to_call == 0:
                action = "check"

            # can't raise if opponent is all-in — force call/fold
            if action == "raise" and opponent.stack == 0:
                print(f"Can't raise, opponent is all-in — treating as call")
                action = "call"

            if action == "fold":
                return f"{names[i]}_fold", self.pot

            elif action == "call":
                actual_call = chips(min(to_call, actor.stack))
                bets[i] = chips(bets[i] + actual_call)
                self.pot = chips(self.pot + actual_call)
                actor.stack = chips(max(actor.stack - actual_call, 0))
                has_acted.add(i)
                if bets[0] == bets[1] and (1 - i) in has_acted:
                    return "continue", self.pot

            elif action == "raise":
                # cap raise to actor's stack
                actual_raise = chips(min(amount, actor.stack))
                bets[i] = chips(bets[i] + actual_raise)
                self.pot = chips(self.pot + actual_raise)
                actor.stack = chips(max(actor.stack - actual_raise, 0))
                self.current_bet = bets[i]
                last_aggressor = i
                has_acted.add(i)

            elif action == "check":
                has_acted.add(i)
                if bets[0] == bets[1] and last_aggressor is None:
                    if i == 1:
                        return "continue", self.pot

            i = 1 - i