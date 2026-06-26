import random

class Computer:
    def __init__(self, stack=1000):
        self.stack = stack

    def get_action(self, to_call, pot):
        if to_call == 0:
            action = random.choice(["check", "raise"])
        else:
            action = random.choice(["fold", "call", "raise"])

        amount = int(pot * 0.5) if action == "raise" else 0
        print(f"Computer: {action}{f' {amount}' if amount else ''}")
        return action, amount