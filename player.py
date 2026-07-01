class Player:
    def __init__(self, stack=1000.0):
        self.stack = stack

    VALID_ACTIONS = {"fold", "call", "raise", "check"}

    def get_action(self, to_call, pot):
        print(f"\nPot: {pot} | To call: {to_call} | Your stack: {self.stack}")

        while True:
            action = input("Action (fold/call/raise/check): ").strip().lower()

            if action not in self.VALID_ACTIONS:
                print("Invalid action, try again")
                continue

            if action == "check" and to_call > 0:
                print(f"Can't check, there's {to_call} to call")
                continue

            if action == "raise":
                try:
                    amount = round(float(input("Raise amount: ")), 2)
                    if amount <= to_call:
                        print(f"Raise must be more than {to_call}")
                        continue
                    if amount > self.stack:
                        print(f"Not enough chips, max raise is {self.stack}")
                        continue
                    return "raise", amount
                except ValueError:
                    print("Enter a valid number")
                    continue

            return action, 0