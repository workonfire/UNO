from game import *


def main():
    players = []
    print("Please type the player names.")
    print("Hint: type \"Computer\" to play with the computer.")  # TODO
    for i in range(1, 10):
        players.append(Player(input(f"Player {i}: ")))
        if i == 2:
            print("More than two players are not supported for now.")  # TODO
            break
    deck_size = int(input("Deck size: "))
    initial_cards = int(input("Initial cards: "))

    game = Game(players=players,
                deck_size=deck_size,
                initial_cards=initial_cards)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            print(f"Winner: {game.winner}")
            break
        print(f"\nTurn: {game.turn.name}")
        print(f"Your cards: {game.turn.hand}")
        print(f"Current card: {game.last_played_card}")
        while True:
            card_input = input("Please input the card that you want to play (or type D to draw): ").upper()
            card = None
            if card_input == 'D':
                game.draw(game.turn)
            else:
                if card_input in ['WILDCARD', '+4']:
                    card = Card(card_input, 'BLUE')
                else:
                    card_type, card_color = card_input.split(' ')
                    try:
                        card = Card(card_type, card_color)
                    except InvalidCardException:
                        print("That card is not a valid card.")
                try:
                    game.play(card, game.turn)
                except CardNotPlayableError:
                    print("That card is not playable.")
                except CardNotInPossessionError:
                    print("You do not have that card in your hand.")
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
