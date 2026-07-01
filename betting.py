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

    def _finish(self, result, bets):
        """Refund any uncalled excess (e.g. a raise a short-stacked
        opponent couldn't fully match) back to whoever bet more."""
        if bets[0] != bets[1]:
            hi, lo = (0, 1) if bets[0] > bets[1] else (1, 0)
            excess = chips(bets[hi] - bets[lo])
            players = [self.player, self.computer]
            players[hi].stack = chips(players[hi].stack + excess)
            self.pot = chips(self.pot - excess)
            bets[hi] = bets[lo]
        return result, self.pot

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
                    return self._finish("continue", bets)
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
                return self._finish(f"{names[i]}_fold", bets)

            elif action == "call":
                actual_call = chips(min(to_call, actor.stack))
                bets[i] = chips(bets[i] + actual_call)
                self.pot = chips(self.pot + actual_call)
                actor.stack = chips(max(actor.stack - actual_call, 0))
                has_acted.add(i)

                # if either side is now (or already was) out of chips,
                # no further decisions are possible for anyone this round
                if actor.stack == 0 or opponent.stack == 0:
                    return self._finish("continue", bets)

                if bets[0] == bets[1] and (1 - i) in has_acted:
                    return self._finish("continue", bets)

            elif action == "raise":
                # cap raise to actor's stack
                actual_raise = chips(min(amount, actor.stack))
                new_bet = chips(bets[i] + actual_raise)

                # a "raise" that wouldn't actually exceed the current bet is
                # not a valid raise — even if it's the actor's whole stack
                # (a short all-in that doesn't fully match is just a call).
                # Never let current_bet go down.
                if new_bet <= self.current_bet:
                    actual_call = chips(min(to_call, actor.stack))
                    bets[i] = chips(bets[i] + actual_call)
                    self.pot = chips(self.pot + actual_call)
                    actor.stack = chips(max(actor.stack - actual_call, 0))
                    has_acted.add(i)
                    if actor.stack == 0 or opponent.stack == 0 or (bets[0] == bets[1] and (1 - i) in has_acted):
                        return self._finish("continue", bets)
                else:
                    bets[i] = new_bet
                    self.pot = chips(self.pot + actual_raise)
                    actor.stack = chips(max(actor.stack - actual_raise, 0))
                    self.current_bet = new_bet
                    last_aggressor = i
                    has_acted.add(i)

            elif action == "check":
                has_acted.add(i)
                if opponent.stack == 0 or (bets[0] == bets[1] and len(has_acted) == 2):
                    return self._finish("continue", bets)

            i = 1 - i