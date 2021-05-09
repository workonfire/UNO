from uno.game import *
import argparse
import traceback
from colorama import Fore, init


def main():
    init(convert=True)
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument('-C', '--cheats', action='store_true')
    argparser.add_argument('-D', '--debug', action='store_true')

    arguments = argparser.parse_args()
    cheats: bool = arguments.cheats
    debug: bool = arguments.debug

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
    deck_size: int = int(input("Deck size: "))
    initial_cards: int = int(input("Initial cards: "))
    card_stacking: bool = input("Card stacking (y/n): ").lower() == 'y' or ''

    rules: Dict[str, Any] = {'deck_size': deck_size,
                             'initial_cards': initial_cards,
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
                card: Union[None, Card] = computer_turn.get_result()
                print(Fore.BLUE + f"Computer put {card}" + Fore.RESET)
                game.play(card, game.turn)
                print(f"Opponent's cards: {game.opponent}" if debug else f"Opponent's remaining cards: "
                                                                         f"{len(game.opponent.hand)}")
            else:
                print(f"Your cards: {game.turn.hand}")
                print(Fore.LIGHTMAGENTA_EX + f"Current card: {game.last_played_card}", Fore.RESET)
                card = None
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
                else:
                    if card_input in ('WILDCARD', '+4'):
                        card = Card(CardType["CARD_" + card_input.upper().replace('+ ', "PLUS_")], None)  # TODO
                    else:
                        try:
                            card = Card.from_str(card_input)
                        except InvalidCardException:
                            print(Fore.RED + "That card is not a valid card." + Fore.RESET)
                        except ValueError:
                            print(Fore.RED + "Incorrect input. Please type a card name, e.g. \"7 GREEN\"" + Fore.RESET)
                    try:
                        game.play(card, game.turn)
                    except CardNotPlayableError:
                        print(Fore.RED + "That card is not playable." + Fore.RESET)
                    except CardNotInPossessionError:
                        print(Fore.RED + "You do not have that card in your hand." + Fore.RESET)
                    except AttributeError:
                        print(Fore.RED + "Incorrect card type. Please type a card name, e.g. \"7 GREEN\"" + Fore.RESET)
            break
