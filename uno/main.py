import sys
import time

from uno.game import *
import argparse
import traceback

__VERSION__: str = 'ALPHA-2025-03-21'

# TODO: Define a print_error() function
# TODO: Check `[bright_white]`


def main():
    console.print("[red]88   88[/red][green] 88b 88[/green][blue]  dP\"Yb  ")
    console.print("[red]88   88[/red][green] 88Yb88[/green][blue] dP   Yb ")
    console.print("[red]Y8   8P[/red][green] 88 Y88[/green][blue] Yb   dP ")
    console.print("[red]`YbodP'[/red][green] 88  Y8[/green][blue]  YbodP  ")
    console.print(f"\n[bright_red]U[bright_green]N[bright_blue]O[/bright_blue][bright_white] | version {__VERSION__}")
    print("---")
    argparser: argparse.ArgumentParser = argparse.ArgumentParser()
    argparser.add_argument('-C', '--cheats', action='store_true')
    argparser.add_argument('-D', '--debug', action='store_true')

    arguments: argparse.Namespace = argparser.parse_args()
    cheats: bool = arguments.cheats
    debug: bool = arguments.debug

    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG if debug else logging.INFO,
                        format='[bright_black]%(levelname)s: %(message)s[/bright_black]')

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
            console.print("[bright_red]Playing with more than two players is currently not supported.[/bright_red]" )
            break
    while True:
        initial_cards: int = int(input("Starting cards: "))
        if initial_cards > 1:
            break
        console.print("[bright_red]The number can't be lower than 2.[/bright_red]")
    card_stacking: bool = input("Similar card stacking (Y/n): ").lower() in ('y', '')

    rules: dict[str, Any] = {'initial_cards': initial_cards,
                             'cheats': cheats,
                             'card_stacking': card_stacking}
    game: Game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            console.print(f"> [green]Winner: {game.winner.name}[/green]")
            break
        console.print(f"\n- Turn: [bold][italic]{game.turn.name}[/bold][/italic]")
        while True:
            if game.turn.is_computer:
                computer_turn: TurnWrapper = TurnWrapper(game)
                card: Card = computer_turn.get_result()
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.5)
                console.print(f"-> Computer put {card}")
                game.play(card, game.turn)
                logging.debug(f"-  Opponent's cards: {game.opponent.format_hand_contents()}")
                print(f"-- Opponent's remaining cards: {len(game.opponent.hand)}")
            else:
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.25)
                console.print(
                    f"\n   [ [bright_cyan]-> [bright_blue]Current card[bright_white]: "
                    f"[bold][underline]{game.last_played_card}[/bold][/underline] "
                    f"[bright_cyan]<- [/bright_cyan]]\n"
                )
                # TODO: Create card visuals
                # game.last_played_card.display(centered=True)
                if not game.turn.is_computer or not game.opponent.is_computer:
                    time.sleep(0.25)
                console.print(f"-- Your cards: {game.turn.format_hand_contents()}\n")
                # game.last_played_card.display()
                card_input: str = console.input("Card ([bright_blue]Enter[/bright_blue] to draw) >[bright_white] ")
                if game.rules['cheats']:
                    try:
                        cheat_code: str = card_input.split('#')[1]
                        # noinspection PyBroadException
                        try:
                            exec(cheat_code)
                        except Exception:
                            console.print("[bright_red]" + traceback.format_exc() + "[/bright_red]")
                        break
                    except IndexError:
                        pass
                card_input = card_input.upper()
                if card_input == '':
                    try:
                        game.deal_card(game.turn)
                    except IndexError:
                        console.print("[bright_red]Can't draw more cards.[/bright_red]")
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
                        console.print(f"[bright_red]The card {card!r} is not playable.[/bright_red]")
                    except CardNotInPossessionError:
                        console.print(f"[bright_red]You do not have {card!r} in your hand.[/bright_red]")
                    except AttributeError:
                        console.print("[bright_red]Incorrect input. Please enter a card name, e.g. \"7 GREEN\"[/bright_red]")
            break
