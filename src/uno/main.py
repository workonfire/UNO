import sys
import time
import argparse
import traceback

from uno.game import *
from rich.console import Console
from time import sleep

__VERSION__: str = 'ALPHA-2025-06-01'

console = Console(color_system='standard')

def print_error(message):
    console.print(f"[bright_red]{message}[/bright_red]")

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
                        format='%(levelname)s: %(message)s')

    players: list[Player] = []
    while True:
        try:
            number_of_players = int(input("Please enter the number of players: "))
            if number_of_players > 1:
                break
            print_error("The number can't be lower than 2.")
        except ValueError:
            print_error("Enter a valid number.")
    print("Please enter the player names.")
    print("Hint: type \"computer\" to play with the computer.\n---")
    for i in range(1, number_of_players + 1):
        while True:
            player_name: str = input(f"Player #{i}: ").lower()
            if player_name in [player.name for player in players]:
                print_error("That player already exists.")
            else:
                break
        players.append(Player(player_name))
    while True:
        try:
            starting_cards: int = int(input("Starting cards: "))
            if starting_cards > 1:
                break
            print_error("The number can't be lower than 2.")
        except ValueError:
            print_error("Enter a valid number.")
    card_stacking: bool = input("Similar card stacking (Y/n): ").lower() in ('y', '')

    rules: dict[str, Any] = {'starting_cards': starting_cards,
                             'cheats': cheats,
                             'card_stacking': card_stacking}
    game: Game = Game(players, rules)

    while game.active:
        if game.get_winner() is not None:
            game.win(game.get_winner())
            console.print(f"> [green]Winner: {game.winner.name}[/green]")
            break
        if not all(player.is_computer for player in players): # Automated game
            print("\n- Turn: [", end='')
            for player in game.players:
                if player == game.turn:
                    console.print(f' [bold][bright_white][underline]{player.name}[/bold][/bright_white][/underline]', end='')
                else:
                    console.print(f' {player.name}', end='')
            print(' ]')
        else:
            console.print(f"\n- Turn: [bold][italic]{game.turn.name}[/bold][/italic]")
        while True:
            if game.turn.is_computer:
                computer_turn: Turn = Turn(game)
                card: Card = computer_turn.get_result()
                if not game.turn.is_computer or not game.next_turn.is_computer:
                    time.sleep(0.5)
                console.print(f"-> Computer put {card}")
                event: GameEvent = game.play(card, game.turn)
                match event.type:
                    case GameEventType.COLOR_CHANGED:
                        console.print(f"{event.payload['player'].name} changed the color to "
                                      f"[bright_{event.payload['new_color'].name.lower()}]"
                                      f"{event.payload['new_color']}[bright_white]")
                        game.stack[0] = Card(None, event.payload['new_color'])
                    case GameEventType.AWAIT_COLOR_INPUT:
                        raise NotImplementedError
                    case GameEventType.STACKING_ACTIVE:
                        for card in event.payload['stacked_cards']:
                            # if not game.turn.is_computer:
                            #    sleep(0.2)
                            console.print(f"> Stacking {card}...")
                logging.debug(f"-  {game.turn.name}'s cards: {game.next_turn.format_hand_contents()}")
                print(f"-- {game.turn.name} remaining cards: {len(game.next_turn.hand)}") # FIXME: Include all players somehow
            else:
                if not game.turn.is_computer or not game.next_turn.is_computer:
                    time.sleep(0.25)
                console.print(
                    f"\n   [ [bright_cyan]-> [bright_blue]Current card[bright_white]: "
                    f"[bold][underline]{game.last_played_card}[/bold][/underline] "
                    f"[bright_cyan]<- [/bright_cyan]]\n"
                )
                # TODO: Create card visuals
                # game.last_played_card.display(centered=True)
                if not game.turn.is_computer or not game.next_turn.is_computer:
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
                            print_error(traceback.format_exc())
                        break
                    except IndexError:
                        pass
                card_input = card_input.upper()
                if card_input == '':
                    try:
                        game.deal_card(game.turn)
                    except IndexError:
                        print_error("Can't draw more cards.") # Does it even make sense?
                elif card_input == 'PASS': # TODO: Make it depend on game rules
                    print("You passed the turn.")
                    game.set_next_turn()
                else:
                    if card_input in ('WILDCARD', '+4'):
                        card = Card(CardType["CARD_" + card_input.upper().replace('+', "PLUS_")], None)
                    else:
                        card = Card.from_str(card_input)
                    try:
                        event: GameEvent = game.play(card, game.turn)
                        match event.type:
                            case GameEventType.COLOR_CHANGED:
                                console.print(f"{event.payload['player'].name} changed the color to "
                                              f"[bright_{event.payload['new_color'].name.lower()}]"
                                              f"{event.payload['new_color']}[bright_white]")
                                game.stack[0] = Card(None, event.payload['new_color'])
                            case GameEventType.AWAIT_COLOR_INPUT:
                                while True:
                                    try:
                                        new_color = CardColor[input("New card color: ").upper()]
                                        break
                                    except KeyError:
                                        console.print("[bright_red]Incorrect input. "
                                                      "Please type a card color, for example \"GREEN\"[/bright_red]")
                                game.stack[0] = Card(None, new_color)
                            case GameEventType.STACKING_ACTIVE:
                                for card in event.payload['stacked_cards']:
                                    sleep(0.2)
                                    console.print(f"> Stacking {card}...")
                    except CardNotPlayableError:
                        print_error(f"The card {card!r} is not playable.")
                    except CardNotInPossessionError:
                        print_error(f"You do not have {card!r} in your hand.")
                    except AttributeError:
                        print_error("Incorrect input. Please enter a card name, for example: \"7 GREEN\"")
            break
