from game import *
from sys import argv
import traceback


def main():
    players = []
    print("Please type the player names.")
    print("Hint: type \"computer\" to play with the computer.")
    for i in range(1, 10):
        while True:
            player_name = input(f"Player {i}: ").lower()
            if player_name in [player.name for player in players]:
                print("That player already exists.")
            else:
                break
        players.append(Player(player_name))
        if i == 2:
            print("More than two players are not supported for now.")  # TODO
            break
    deck_size = int(input("Deck size: "))
    initial_cards = int(input("Initial cards: "))
    card_stacking = input("Card stacking (y/n): ").lower() == 'y'

    if len(argv) > 1:
        cheats = argv[1] == '--cheats' or argv[1] == '-C'
    else:
        cheats = False

    rules = {'deck_size': deck_size,
             'initial_cards': initial_cards,
             'cheats': cheats,
             'card_stacking': card_stacking}
    game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            print(f"Winner: {game.winner.name}")
            break
        print(f"\nTurn: {game.turn.name}")
        while True:
            if game.turn.is_computer:
                computer_turn = TurnWrapper(game)
                card = computer_turn.get_result()
                print(f"Computer put {card}")
                game.play(card, game.turn)
                print(f"Opponent's remaining cards: {len(game.opponent.hand)}")
            else:
                print(f"Your cards: {game.turn.hand}")
                print(f"Current card: {game.last_played_card}")
                card = None
                card_input = input("Please input the card that you want to play (or type D to draw): ")
                if game.rules['cheats']:
                    try:
                        cheat_code = card_input.split('C: ')[1]
                        # noinspection PyBroadException
                        try:
                            exec(cheat_code)
                        except Exception:
                            traceback.print_exc()
                        break
                    except IndexError:
                        pass
                card_input = card_input.upper()
                if card_input == 'D':
                    game.deal_card(game.turn)
                else:
                    if card_input in ['WILDCARD', '+4']:
                        card = Card(card_input, 'BLUE')
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
