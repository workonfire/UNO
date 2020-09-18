import random
from visuals import color_print, CardVisual
from colorama import Fore
from shutil import get_terminal_size
from exceptions import *

from typing import List


class Card:
    COLORS = ['BLUE', 'RED', 'GREEN', 'YELLOW']
    TYPES = [str(i) for i in range(10)] + ['+2', '+4', 'SKIP', 'WILDCARD', 'REVERSE']

    # Some functional cards were skipped for now, since they're pointless in a 1v1 game.

    def __init__(self, card_type: str, color: str):
        self.color: str = color
        self.card_type: str = card_type
        self.is_wild: bool = self.card_type in ['WILDCARD', '+4']
        if self.is_wild:
            self.color = 'BLUE'
        if self.card_type not in self.TYPES or self.color not in self.COLORS:
            raise InvalidCardException(f"{self.card_type}/{self.color} is not a valid card object.")

    def __repr__(self) -> str:
        return f'{self.card_type}' if self.is_wild else f'{self.card_type} {self.color}'

    def __eq__(self, other) -> bool:
        return self.card_type == other.card_type and self.color == other.color

    def playable(self, comparator) -> bool:
        """
        Compares two cards between their types and colors.
        :param comparator: card object
        :return: true, if they're similar
        """
        # TODO: Stacking
        if self.is_wild:
            return True
        else:
            return self.card_type == comparator.card_type or self.color == comparator.color

    def display(self, centered: bool):
        """
        Creates a visual representation of the card.
        :param centered: whether to center the card on the display, or not
        """
        colors = {'BLUE': Fore.BLUE,
                  'RED': Fore.RED,
                  'GREEN': Fore.GREEN,
                  'YELLOW': Fore.YELLOW}
        card_types = {'1': CardVisual.CARD_1}  # TODO
        if centered:
            card_to_display = '\n'.join(card_types.get(self.card_type)).center(get_terminal_size().columns)
        else:
            card_to_display = '\n'.join(card_types.get(self.card_type))
        color_print(colors.get(self.color), card_to_display)


class Deck:
    def __init__(self, size: int):
        self.stack: List[Card] = []
        for i in range(size):
            card_type = random.choice(Card.TYPES)
            color = random.choice(Card.COLORS)
            self.stack.append(Card(card_type, color))

    def draw(self, number: int = 1) -> [List[Card], Card]:
        """
        Draws a specified amount of cards.
        :param number: a number of cards that you want to draw. Default is 1.
        :return: a list of cards, if the amount is greater than 1.
        """
        if number > len(self.stack):
            raise IndexError(f"Tried to draw {number} from a deck that has only {len(self.stack)} cards.")
        return self.stack.pop(-1) if number == 1 else [self.stack.pop(-1) for _ in range(number)]


class Player:
    def __init__(self, name=None):
        self.hand: List[Card] = []
        self.name: str = name

    def __repr__(self) -> str:
        return f'{self.name}: ' + ', '.join([str(self.hand)])


class Table:
    def __init__(self, players: List[Player], deck_size: int, initial_cards: int):
        self.players: List[Player] = players
        self.initial_cards: int = initial_cards

        self.deck: Deck = Deck(deck_size)
        self.stack: List[Card] = [self.deck.draw()]

        for player in players:
            player.hand = self.deck.draw(self.initial_cards)

        self.turn: Player = self.players[0]  # This was random at some point.

    @property
    def last_played_card(self) -> Card:
        return self.stack[0]

    def play(self, card: Card, player: Player, check_possession: bool = True):
        """
        Puts the selected card on top of the stack.
        """
        if card.playable(self.last_played_card):
            if check_possession and card not in player.hand:
                raise CardNotInPossessionError("You do not have that card in your hand.")
            self.stack.insert(0, card)
            player.hand.remove(card)
            if card.is_wild:
                # TODO: A more proper way to select a color.
                new_color = input("Please input a new card color: ")  # TODO: Language file
                new_card = Card(random.choice([str(i) for i in range(10)]), new_color)
                self.stack.insert(0, new_card)
                if card.card_type == '+4':
                    new_cards = self.deck.draw(4)
                    for card in new_cards:
                        self.get_opponent().hand.append(card)
            elif card.card_type == '+2':
                new_cards = self.deck.draw(2)
                for card in new_cards:
                    self.get_opponent().hand.append(card)
            if card.card_type not in ['SKIP', 'REVERSE']:
                print("Turn changed.")
                self.next_turn()
        else:
            raise CardNotPlayableError("You cannot play with this type of card.")

    def draw(self, player: Player, amount: int = 1):
        """
        Gives the player a card from the deck.
        """
        cards = self.deck.draw(amount)
        if amount > 1:
            for card in cards:
                player.hand.append(card)
        else:
            player.hand.append(cards)

    def get_opponent(self) -> Player:
        """
        I know, it's ugly. I haven't figured out a queue system yet, since this is just a 1v1 game.
        """
        return self.players[0] if self.turn == self.players[1] else self.players[1]

    def next_turn(self):
        """
        Switches the table turn.
        """
        self.turn = self.get_opponent()


class Game(Table):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active: bool = True
        self.winner: [None, Player] = None
        while self.last_played_card.is_wild:
            self.stack.insert(0, self.deck.draw())

    def end(self):
        """
        Ends the game and sets its status to inactive.
        """
        if not self.active:
            raise RuntimeError("The game is already inactive.")
        self.active = False

    def get_winner(self) -> Player:
        """
        Checks if somebody has won the game.
        """
        for player in self.players:
            if not player.hand:
                return player

    def win(self, player: Player):
        """
        Sets the game winner and ends it.
        :param player:
        """
        if self.winner is not None:
            raise WinnerAlreadySetException("The winner has already been set.")
        self.winner = player
        self.end()


class ComputerTurn:
    def __init__(self, table: Table):
        self.table = table
        self.last_card: Card = self.table.last_played_card
        self.hand: List[Card] = self.table.turn.hand

    @property
    def playable_cards(self) -> List[Card]:
        playable_cards = []
        for card in self.hand:
            if card.playable(self.last_card):
                playable_cards.append(card)
        return playable_cards

    @property
    def most_reasonable_color(self) -> str:
        all_card_colors = [card.color for card in self.playable_cards]
        return max(set(all_card_colors), key=all_card_colors.count)

    def get_result(self) -> Card:
        while not self.playable_cards:
            self.table.draw(self.table.turn)
        card = random.choice(self.playable_cards)
        if card.is_wild:  # TODO
            pass
        return card
