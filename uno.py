from game import *
import argparse
import traceback
from visuals import color_print
from colorama import Fore


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument('-C', '--cheats', action='store_true')
    argparser.add_argument('-D', '--debug', action='store_true')

    arguments = argparser.parse_args()
    cheats = arguments.cheats
    debug = arguments.debug

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
    deck_size = int(input("Deck size: "))
    initial_cards = int(input("Initial cards: "))
    card_stacking = input("Card stacking (y/n): ").lower() == 'y'

    rules = {'deck_size': deck_size,
             'initial_cards': initial_cards,
             'cheats': cheats,
             'card_stacking': card_stacking}
    game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            color_print(Fore.GREEN, f"Winner: {game.winner.name}")
            break
        print(f"\nTurn: {game.turn.name}")
        while True:
            if game.turn.is_computer:
                computer_turn = TurnWrapper(game)
                card = computer_turn.get_result()
                color_print(Fore.BLUE, f"Computer put {card}")
                game.play(card, game.turn)
                print(f"Opponent's cards: {game.opponent}" if debug else f"Opponent's remaining cards: "
                                                                         f"{len(game.opponent.hand)}")
            else:
                print(f"Your cards: {game.turn.hand}")
                color_print(Fore.LIGHTMAGENTA_EX, f"Current card: {game.last_played_card}")
                card = None
                card_input = input("Please input the card that you want to play (or type D to draw): ")
                if game.rules['cheats']:
                    try:
                        cheat_code = card_input.split('#')[1]
                        # noinspection PyBroadException
                        try:
                            exec(cheat_code)
                        except Exception:
                            color_print(Fore.RED, traceback.format_exc())
                        break
                    except IndexError:
                        pass
                card_input = card_input.upper()
                if card_input == 'D':
                    try:
                        game.deal_card(game.turn)
                    except IndexError:
                        color_print(Fore.RED, "Can't draw more cards.")
                else:
                    if card_input in ['WILDCARD', '+4']:
                        card = Card(card_input, 'BLUE')
                    else:
                        try:
                            card_type, card_color = card_input.split(' ')
                            card = Card(card_type, card_color)
                        except InvalidCardException:
                            color_print(Fore.RED, "That card is not a valid card.")
                        except ValueError:
                            color_print(Fore.RED, "Incorrect input. Please type a card name, e.g. \"7 GREEN\"")
                    try:
                        game.play(card, game.turn)
                    except CardNotPlayableError:
                        color_print(Fore.RED, "That card is not playable.")
                    except CardNotInPossessionError:
                        color_print(Fore.RED, "You do not have that card in your hand.")
                    except AttributeError:
                        color_print(Fore.RED, "Incorrect card type. Please type a card name, e.g. \"7 GREEN\"")
            break


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
