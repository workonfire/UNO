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

    def __init__(self, card_type: [None, str], color: str):
        self.color: str = color
        self.card_type: [None, str] = card_type
        self.is_wild: bool = self.card_type in ['WILDCARD', '+4']
        if self.is_wild:
            self.color = 'BLUE'
        if self.card_type not in self.TYPES or self.color not in self.COLORS:
            if self.card_type is not None:
                raise InvalidCardException(f"{self.card_type}/{self.color} is not a valid card object.")

    def __repr__(self) -> str:
        if self.card_type is None:
            return f'* {self.color}'
        return f'{self.card_type}' if self.is_wild else f'{self.card_type} {self.color}'

    def __eq__(self, other) -> bool:
        return self.card_type == other.card_type and self.color == other.color

    def playable(self, comparator) -> bool:
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
        colors = {'BLUE': Fore.BLUE,
                  'RED': Fore.RED,
                  'GREEN': Fore.GREEN,
                  'YELLOW': Fore.YELLOW}
        if centered:
            card_to_display = '\n'.join(CardVisual(self).art).center(get_terminal_size().columns)
        else:
            card_to_display = '\n'.join(CardVisual(self).art)
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

    @property
    def is_computer(self) -> bool:
        if self.name is not None:
            return 'computer' in self.name
        return False


class Table:
    def __init__(self, players: List[Player], rules: dict):
        self.rules: dict = rules
        self.players: List[Player] = players

        self.deck: Deck = Deck(self.rules['deck_size'])
        self.stack: List[Card] = [self.deck.draw()]

        for player in players:
            player.hand = self.deck.draw(self.rules['initial_cards'])

        self.turn: Player = self.players[0]  # This was random at some point.

    @property
    def last_played_card(self) -> Card:
        return self.stack[0]

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
                    new_color = TurnWrapper(self).most_reasonable_color
                    print(f"{self.turn.name} changed the color to {new_color}")
                else:
                    new_color = input("Please input a new card color: ").upper()  # TODO: Language file
                if card.card_type == '+4':
                    new_cards = self.deck.draw(4)
                    for new_card in new_cards:
                        self.opponent.hand.append(new_card)
                new_card = Card(None, new_color)
                self.stack.insert(0, new_card)
            else:
                if card.card_type == '+2':  # TODO: Queue +2 and +4 stacking
                    new_cards = self.deck.draw(2)
                    for new_card in new_cards:
                        self.opponent.hand.append(new_card)

                if self.rules['card_stacking'] and not stacking:
                    for playable_card in TurnWrapper(self).playable_cards:
                        if not playable_card.is_wild and playable_card.card_type == self.last_played_card.card_type:
                            self.play(playable_card, player, stacking=True)
                            print(f"Took out {playable_card}")

            if card.card_type not in ['SKIP', 'REVERSE'] and not stacking:
                self.next_turn()
        else:
            raise CardNotPlayableError(f"The player {player} cannot play with {card}.")

    def deal_card(self, player: Player, amount: int = 1):
        """
        Gives the player a card from the deck.
        """
        cards = self.deck.draw(amount)
        if amount > 1:
            for card in cards:
                player.hand.append(card)
        else:
            player.hand.append(cards)

    @property
    def opponent(self) -> Player:
        """
        I know, it's ugly. I haven't figured out a queue system yet, since this is just a 1v1 game.
        """
        return self.players[0] if self.turn == self.players[1] else self.players[1]

    def next_turn(self):
        """
        Switches the table turn.
        """
        self.turn = self.opponent


class Game(Table):
    def __init__(self, players: List[Player], rules: dict):
        super().__init__(players, rules)
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
        card_colors = [card.color for card in self.playable_cards]
        if not card_colors:
            return random.choice(Card.COLORS)
        return max(set(card_colors), key=card_colors.count)

    def get_result(self) -> Card:
        while not self.playable_cards:
            self.table.deal_card(self.table.turn)
        return random.choice(self.playable_cards)
