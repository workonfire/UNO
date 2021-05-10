import sys

from uno.game import *
import argparse
import traceback
from colorama import Fore  # TODO: Color support on Windows

__VERSION__: str = 'ALPHA'


def main():
    print(f"{Fore.RED}U{Fore.GREEN}N{Fore.BLUE}O{Fore.RESET} {__VERSION__}")
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument('-C', '--cheats', action='store_true')
    argparser.add_argument('-D', '--debug', action='store_true')

    arguments: argparse.Namespace = argparser.parse_args()
    cheats: bool = arguments.cheats
    debug: bool = arguments.debug

    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG if debug else logging.INFO,
                        format=f'{Fore.LIGHTBLACK_EX}%(levelname)s: %(message)s{Fore.RESET}')

    players: List[Player] = []
    print("Please type the player names.")
    print("Hint: type \"computer\" to play with the computer.")
    for i in range(1, 10):
        while True:
            player_name: str = input(f"Player {i}: ").lower()
            if player_name in [player.name for player in players]:
                print("That player already exists.")
            else:
                break
        players.append(Player(player_name))
        if i == 2:
            print(Fore.RED + "More than two players are not supported for now." + Fore.RESET)  # TODO
            break
    while True:
        initial_cards: int = int(input("Initial cards: "))
        if initial_cards > 1:
            break
        print(Fore.RED + "The number of initial cards can't be lower than 2." + Fore.RESET)
    card_stacking: bool = input("Card stacking (Y/n): ").lower() == 'y' or ''

    rules: Dict[str, Any] = {'initial_cards': initial_cards,
                             'cheats': cheats,
                             'card_stacking': card_stacking}
    game: Game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            print(Fore.GREEN + f"Winner: {game.winner.name}" + Fore.RESET)
            break
        print(f"\nTurn: {game.turn.name}")
        while True:
            if game.turn.is_computer:
                computer_turn: TurnWrapper = TurnWrapper(game)
                card: Card = computer_turn.get_result()
                print(f"Computer put {card}")
                game.play(card, game.turn)
                logging.debug(f"Opponent's cards: {game.opponent.format_hand_contents()}")
                print(f"Opponent's remaining cards: {len(game.opponent.hand)}")
            else:
                print(f"Your cards: {game.turn.format_hand_contents()}")
                # game.last_played_card.display()
                print(f"Current card: {game.last_played_card}")
                card_input: str = input("Card (e.g. 4 BLUE, Enter to draw): ")
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
                elif card_input == 'PASS':
                    print("You passed.")
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
                        print(Fore.RED + "Incorrect input. Please type a card name, e.g. \"7 GREEN\"" + Fore.RESET)
            break
