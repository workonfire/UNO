from game import *
from sys import argv


def main():
    players = []
    print("Please type the player names.")
    print("Hint: type \"Computer\" to play with the computer.")
    for i in range(1, 10):
        players.append(Player(input(f"Player {i}: ")))
        if i == 2:
            print("More than two players are not supported for now.")  # TODO
            break
    deck_size = int(input("Deck size: "))
    initial_cards = int(input("Initial cards: "))

    if len(argv) > 1:
        cheats = argv[1] == '--cheats' or argv[1] == '-C'
    else:
        cheats = False

    game = Game(players, deck_size, initial_cards, cheats=cheats)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            print(f"Winner: {game.winner.name}")
            break
        print(f"\nTurn: {game.turn.name}")
        while True:
            if game.turn.is_computer:
                computer_turn = ComputerTurn(game)
                card = computer_turn.get_result()
                if game.cheats:
                    print(f"Opponent's cards: {game.turn.hand}")
                print(f"Computer put {card}")
                game.play(card, game.turn)
            else:
                print(f"Your cards: {game.turn.hand}")
                print(f"Current card: {game.last_played_card}")
                card = None
                card_input = input("Please input the card that you want to play (or type D to draw): ").upper()
                if card_input == 'D':
                    game.draw(game.turn)
                else:
                    if card_input in ['WILDCARD', '+4']:
                        card = Card(card_input, random.choice(Card.COLORS))
                    else:
                        try:
                            card_type, card_color = card_input.split(' ')
                            card = Card(card_type, card_color)
                        except InvalidCardException:
                            print("That card is not a valid card.")
                        except ValueError:
                            print("Incorrect input. Please type a card name, e.g. \"7 GREEN\"")
                    try:
                        game.play(card, game.turn)
                    except CardNotPlayableError:
                        print("That card is not playable.")
                    except CardNotInPossessionError:
                        print("You do not have that card in your hand.")
                    except AttributeError:
                        print("Incorrect card type. Please type a card name, e.g. \"7 GREEN\"")
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
