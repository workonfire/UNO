import sys
import time

from uno.game import *
import argparse
import traceback
from colorama import Fore # TODO: Remove colorama dependency and fix colors on Windows
# TODO: https://pypi.org/project/rich/

__VERSION__: str = 'ALPHA-2025-02-23'


def main():
    print(f"{Fore.LIGHTRED_EX}U{Fore.LIGHTGREEN_EX}N{Fore.LIGHTBLUE_EX}O{Fore.RESET} | version {__VERSION__}")
    print("---")
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument('-C', '--cheats', action='store_true')
    argparser.add_argument('-D', '--debug', action='store_true')

    arguments: argparse.Namespace = argparser.parse_args()
    cheats: bool = arguments.cheats
    debug: bool = arguments.debug

    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG if debug else logging.INFO,
                        format=f'{Fore.LIGHTBLACK_EX}%(levelname)s: %(message)s{Fore.RESET}')

    players: list[Player] = []
    print("Please enter the player names.")
    print("Hint: type \"computer\" to play with the computer.\n")
    for i in range(1, 10): # TODO: A proper queue system
        while True:
            player_name: str = input(f"Player {i}: ").lower()
            if player_name in [player.name for player in players]:
                print("That player already exists.")
            else:
                break
        players.append(Player(player_name))
        if i == 2:
            print(Fore.RED + "Playing with more than two players is currently not supported." + Fore.RESET)  # TODO
            break
    while True:
        initial_cards: int = int(input("Starting cards: "))
        if initial_cards > 1:
            break
        print(Fore.RED + "The number can't be lower than 2." + Fore.RESET)
    card_stacking: bool = input("Similar card stacking (Y/n): ").lower() in ('y', '')

    rules: dict[str, Any] = {'initial_cards': initial_cards,
                             'cheats': cheats,
                             'card_stacking': card_stacking}
    game: Game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            print("> " + Fore.GREEN + f"Winner: {game.winner.name}" + Fore.RESET)
            break
        print(f"\n- Turn: {game.turn.name}")
        while True:
            if game.turn.is_computer:
                computer_turn: TurnWrapper = TurnWrapper(game)
                card: Card = computer_turn.get_result()
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.5)
                print(f"-> Computer put {card}")
                game.play(card, game.turn)
                logging.debug(f"-  Opponent's cards: {game.opponent.format_hand_contents()}")
                print(f"-- Opponent's remaining cards: {len(game.opponent.hand)}")
            else:
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.25)
                # TODO: Convert all colors to `colorama`
                print(f"\n   [\033[36;40;1m -> Current card: {game.last_played_card} \033[36;40;1m<- \033[0m]\n")
                # TODO: Create card visuals
                # game.last_played_card.display(centered=True)
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.25)
                print(f"-- Your cards: {game.turn.format_hand_contents()}\n")
                # game.last_played_card.display()
                card_input: str = input(f"Card ({Fore.LIGHTCYAN_EX}Enter{Fore.LIGHTWHITE_EX} to draw) >{Fore.RESET} ")
                if game.rules['cheats']:
                    try:
                        cheat_code: str = card_input.split('#')[1]
                        # noinspection PyBroadException
                        try:
                            exec(cheat_code)
                        except Exception:
                            print(Fore.RED + traceback.format_exc() + Fore.RESET)
                        break
                    except IndexError:
                        pass
                card_input = card_input.upper()
                if card_input == '':
                    try:
                        game.deal_card(game.turn)
                    except IndexError:
                        print(Fore.RED + "Can't draw more cards." + Fore.RESET)
                elif card_input == 'PASS': # TODO: Make it depend on game rules
                    print("You passed the turn.")
                    game.next_turn()
                else:
                    if card_input in ('WILDCARD', '+4'):
                        card = Card(CardType["CARD_" + card_input.upper().replace('+', "PLUS_")], None)
                    else:
                        card = Card.from_str(card_input)
                    try:
                        game.play(card, game.turn)
                    except CardNotPlayableError:
                        print(Fore.RED + f"The card {card!r} is not playable." + Fore.RESET)
                    except CardNotInPossessionError:
                        print(Fore.RED + f"You do not have {card!r} in your hand." + Fore.RESET)
                    except AttributeError:
                        print(Fore.RED + "Incorrect input. Please enter a card name, e.g. \"7 GREEN\"" + Fore.RESET)
            break
