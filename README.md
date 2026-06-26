# pokerBot

A heads-up Texas Hold'em engine in Python with a human player vs. a computer opponent.

## Project Structure

```
pokerBot/
├── game.py        # orchestrator — hand loop, blinds, showdown
├── betting.py     # betting round logic for each street
├── player.py      # human input handler
├── computer.py    # random computer opponent
└── evaluator.py   # standalone hand eval scratch script
```

## Flow

```
Game.__init__()
└── play_hand() [loops until bust]
    ├── post blinds
    ├── deal cards
    ├── BettingRound (preflop) → fold? award pot : continue
    ├── BettingRound (flop)    → fold? award pot : continue
    ├── BettingRound (turn)    → fold? award pot : continue
    ├── BettingRound (river)   → fold? award pot : continue
    └── showdown() → award pot
```

## Setup

```bash
pip install treys
python game.py
```

## Rules

- Heads-up, blinds are 0.5 / 1.0
- Blinds alternate each hand
- Standard hand rankings via [`treys`](https://github.com/ihendley/treys)
- Computer plays randomly (fold / call / raise with equal weight)
