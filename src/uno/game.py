import logging
import random

from rich.console import Console

from uno.enums import *
from uno.exceptions import *
from shutil import get_terminal_size
from time import sleep

from typing import Any, Generator, Optional

console = Console(color_system='standard') # TODO: make this not a dependency

def print_error(message):
    console.print(f"f[bright_red]{message}[/bright_red]")


class Card:
    def __init__(self, card_type: Optional[CardType], color: Optional[CardColor]):
        self.card_type: Optional[CardType] = card_type
        self.is_wild: bool = self.card_type in (CardType.CARD_WILDCARD, CardType.CARD_PLUS_4)
        self.color: Optional[CardColor] = None if self.is_wild else color
        if self.card_type is None and self.color is None:
            raise InvalidCardException

    def __repr__(self) -> str:
        if self.card_type is None and self.color is not None:
            return f'* {self.color.name}'
        card_type_name: str = ' '.join(self.card_type.name.split('_')[1:]).replace('PLUS ', '+')
        # noinspection PyUnresolvedReferences
        return card_type_name if self.is_wild and self.color is None else f'{card_type_name} {self.color.name}'

    def __str__(self) -> str:
        color: str = f'[bright_{self.color.name.lower()}]' if self.color is not None else '[bright_white]'
        return color + self.__repr__() + '[bright_white]'

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Card):
            return self.card_type == other.card_type and self.color == other.color
        else:
            return NotImplemented

    @staticmethod
    def from_str(value: str) -> Optional['Card']:
        try:
            card_type, card_color = value.upper().split(' ')
            card: Optional['Card'] = Card(CardType["CARD_" + card_type.replace('+', 'PLUS_')], CardColor[card_color])
        except ValueError:
            if value.upper() == 'WILDCARD':
                card = Card(CardType.CARD_WILDCARD, None)
            elif value.upper() == '+4':
                card = Card(CardType.CARD_PLUS_4, None)
            else:
                card = None
        except KeyError:
            card = None
        return card

    def playable(self, comparator: 'Card') -> bool:
        """
        Compares two cards between their types and colors.
        :param comparator: card object
        :return: true, if they're similar
        """
        if self.is_wild:
            return True
        else:
            return self.card_type == comparator.card_type or self.color == comparator.color

    def display(self, centered: bool = False):
        """
        Creates a visual representation of the card.
        :param centered: whether to center the card on the display, or not
        """
        card_to_display: str = CardVisual(self).art
        # TODO: Card visuals
        # card_to_display: str = ''.join(CardVisual.get_card_visual('>', self.card_type.value))
        if centered:
            card_to_display = card_to_display.center(get_terminal_size().columns)
        console.print(f'[bright_{self.color.name.lower()}]' + card_to_display + '[bright_white]')


class Deck:
    def draw(self, number: int = 1) -> list[Card] | Card:
        """
        Draws a specified amount of cards.
        :param number: a number of cards that you want to draw. Default is 1.
        :return: a list of cards, if the amount is greater than 1.
        """
        # TODO: Just return a list and expect a list in a parent function
        return self.stack if number == 1 else [self.stack for _ in range(number)]

    @staticmethod
    def _stack() -> Generator[Card, None, None]:
        card_type: CardType = random.choice([*CardType])
        color: CardColor = random.choice([*CardColor])
        yield Card(card_type, color)

    @property
    def stack(self) -> Card:
        return next(self._stack())


class Player:
    def __init__(self, name: str = ''):
        self.hand: list[Card] = []
        self.name: str = name
        self.is_computer: bool = 'computer' in self.name.lower() if self.name is not None else False

    def format_hand_contents(self) -> str:
        return ', '.join([card.__str__() for card in self.hand])

    def __repr__(self) -> str:
        return f'{self.name}: ' + ', '.join([str(self.hand)])


class Table:
    def __init__(self, players: list[Player], rules: dict[str, Any]):
        self.rules: dict[str, Any] = rules
        self.players: list[Player] = players
        self.deck: Deck = Deck()
        self.stack: list[Card] = [self.deck.draw()]
        self.turn_index: int = 0
        self.direction: int = 1
        while self.stack[0].card_type in (CardType.CARD_PLUS_4, CardType.CARD_PLUS_2, CardType.CARD_WILDCARD):
            self.stack = [self.deck.draw()]
        for player in players:
            player.hand = self.deck.draw(self.rules['initial_cards'])

    @property
    def last_played_card(self) -> Card:
        return self.stack[0]

    @property
    def turn(self) -> Player:
        return self.players[self.turn_index]

    def play(self, card: Card, player: Player, stacking: bool = False):
        """
        Puts the selected card on top of the stack.
        :param card: card object.
        :param player: player object.
        :param stacking: describes if the player is currently in the middle of card-stacking.
        """
        if card.playable(self.last_played_card):
            if card not in player.hand:
                raise CardNotInPossessionError(f"The player {player} does not have {card} card in hand.")
            self.stack.insert(0, card)
            player.hand.remove(card)

            if card.is_wild:
                if self.turn.is_computer:
                    new_color: CardColor = TurnWrapper(self).most_reasonable_color
                    console.print(
                        f"{self.turn.name} changed the color to [bright_{new_color.name.lower()}]{new_color}[bright_white]")
                else:
                    # TODO: Language file
                    while True:
                        try:
                            new_color = CardColor[input("New card color: ").upper()]
                            break
                        except KeyError:
                            console.print(
                                "[bright_red]Incorrect input. Please type a card color, e.g. \"GREEN\"[/bright_red]")
                if card.card_type == CardType.CARD_PLUS_4:
                    next_player: Player = self.players[(self.turn_index + self.direction) % len(self.players)]
                    new_cards: list[Card] = self.deck.draw(4)
                    next_player.hand.extend(new_cards)
                self.stack[0] = Card(None, new_color)
                logging.debug(f"Card on stack: {self.stack[0]}")
            else:
                if card.card_type == CardType.CARD_PLUS_2:  # TODO: Queue +2 and +4 stacking
                    next_player = self.players[(self.turn_index + self.direction) % len(self.players)]
                    new_cards = self.deck.draw(2)
                    next_player.hand.extend(new_cards)
                if self.rules.get('card_stacking') and not stacking:
                    for playable_card in TurnWrapper(self).playable_cards:
                        if not playable_card.is_wild and playable_card.card_type == self.last_played_card.card_type:
                            self.play(playable_card, player, stacking=True)
                            # TODO: +2 and/or +4 stacking
                            if not self.turn.is_computer:
                                sleep(0.2)
                            console.print(f"> Stacking {playable_card}...")
            if not stacking:
                if card.card_type == CardType.CARD_SKIP:
                    self.skip_next_player()
                elif card.card_type == CardType.CARD_REVERSE:
                    self.reverse_queue()
                    self.set_next_turn()
                else:
                    self.set_next_turn()
        else:
            raise CardNotPlayableError(f"The player {player} cannot play with {card}.")

    def deal_card(self, player: Player, amount: int = 1):
        """
        Gives the player a card from the deck.
        """
        cards = self.deck.draw(amount)
        if isinstance(cards, list):
            player.hand.extend(cards)
        else:
            player.hand.append(cards)

    @property
    def next_turn(self) -> Player:
        return self.players[(self.turn_index + self.direction) % len(self.players)]

    def set_next_turn(self):
        self.turn_index = (self.turn_index + self.direction) % len(self.players)

    def reverse_queue(self):
        self.direction *= -1

    def skip_next_player(self):
        self.turn_index = (self.turn_index + self.direction) % len(self.players)
        self.set_next_turn()

class Game(Table):
    def __init__(self, players: list[Player], rules: dict[str, Any]):
        super().__init__(players, rules)
        self.active: bool = True
        self.winner: Player | None = None
        while self.last_played_card.is_wild:
            self.stack.insert(0, self.deck.draw())

    def end(self):
        """
        Ends the game and sets its status to inactive.
        """
        if not self.active:
            raise RuntimeError("The game is already inactive.")
        self.active: bool = False

    def get_winner(self) -> Optional[Player]:
        """
        Checks if somebody has won the game.
        """
        for player in self.players:
            if not player.hand:
                return player
        return None

    def win(self, player: Player):
        """
        Sets the game winner and ends it.
        :param player: player object
        """
        if self.winner is not None:
            raise WinnerAlreadySetException("The winner has already been set.")
        self.winner = player
        self.end()


class TurnWrapper:
    def __init__(self, table: Table):
        self.table: Table = table
        self.last_card: Card = self.table.last_played_card
        self.hand: list[Card] = self.table.turn.hand

    @property
    def playable_cards(self) -> list[Card]:
        playable_cards: list[Card] = []
        for card in self.hand:
            if card.playable(self.last_card):
                playable_cards.append(card)
        return playable_cards

    @property
    def most_reasonable_color(self) -> CardColor:
        card_colors: list[Optional[CardColor]] = [card.color for card in self.playable_cards]
        if not card_colors or set(card_colors) == {None}:
            return random.choice([*CardColor])
        return max(set(card_colors), key=card_colors.count)

    def get_result(self) -> Card:
        while not self.playable_cards:
            self.table.deal_card(self.table.turn)
        return random.choice(self.playable_cards)
