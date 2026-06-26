class Player:
    def __init__(self, stack=1000):
        self.stack = stack

    def get_action(self, to_call, pot):
        print(f"\nPot: {pot} | To call: {to_call} | Your stack: {self.stack}")
        action = input("Action (fold/call/raise/check): ").strip().lower()

        if action == "raise":
            amount = int(input("Raise amount: "))
            return "raise", amount
        return action, 0