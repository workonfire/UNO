# UNO
A simple Python implementation of the UNO game.

### WARNING: WORK IN PROGRESS.
It's best to look at the `#TODO` notes inside files.

No screenshots for now, because the current interface is just temporary.

To-do features:
- Easy to use API
- Multiplayer
- Interface (cards etc.) displayed as ASCII art
- Cheat system based on pure Python console
- Fully customizable rooms with custom game rules

#### CLI switches
- `--debug` or `-D` - always shows the opponent's cards
- `--cheats` or `-C` - enables the cheat console; example:
```
Turn: test
Your cards: [7 RED, +2 YELLOW, SKIP BLUE]
Current card: 5 RED
Please input the card that you want to play (or type D to draw): #game.opponent.hand = [Card('6', 'BLUE') for _ in range(666)]
```
All cheats must be preceded with `#`.

## API Preview
These are just **examples**.
- Inspecting a card
```python
card = Card(CardType.CARD_6, CardColor.BLUE)
other_card = Card.from_str('7 RED')
if card.playable(other_card):
    print("This card is playable with the other card.")
```

- Generating a deck
```python
deck = Deck(size=50)
cards: List[Card] = deck.draw(15)
```

- Inspecting a player
```python
player = Player('wzium')
if player.is_computer:
    print("The player is a computer.")
if len(player.hand) == 0:
    print("The player does not have any card.")
```

- Working with the table
```python
players: List[Player] = [Player('Wzium'), Player('Computer')]
# Custom rules (W.I.P.)
rules: Dict[str, Any] = {'deck_size': 50,
                         'initial_cards': 7,
                         'cheats': False,
                         'card_stacking': True}

table = Table(players, rules)
table.play(table.turn.hand[0], table.turn) # Gets the user to play the first card 
print(table.last_played_card) # Get the last player card
table.deal_card(table.opponent, 5) # Gives 5 cards to the opponent
```

- Operating with the game
```python
game = Game(players, rules)
while game.active:
    if game.get_winner() is not None:
        game.win(game.get_winner())
```

- Faking a turn
```python
turn = TurnWrapper(table)
print(turn.playable_cards) # gets all currently playable cards
print(turn.most_reasonable_color) # selects the appriopriate color based on how many times it appears
print(turn.get_result()) # Prints a card to play with
```