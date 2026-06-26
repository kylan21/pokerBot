Basic game structure

Game.__init__()
└── play_hand() [loops until bust]
    ├── post blinds
    ├── deal cards
    ├── BettingRound (preflop) → fold? award pot : continue
    ├── BettingRound (flop)    → fold? award pot : continue
    ├── BettingRound (turn)    → fold? award pot : continue
    ├── BettingRound (river)   → fold? award pot : continue
    └── showdown() → award pot
