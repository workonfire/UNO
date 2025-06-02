from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uno.game import Card


class Type(Enum):
    def __str__(self) -> str:
        return self.name


class GameEventType(Type):
    AWAIT_COLOR_INPUT = auto()
    COLOR_CHANGED = auto()
    STACKING_ACTIVE = auto()
    NO_EVENT = auto()


class CardColor(Type):
    BLUE = auto()
    RED = auto()
    GREEN = auto()
    YELLOW = auto()


class CardType(Type):
    CARD_0 = auto()
    CARD_1 = auto()
    CARD_2 = auto()
    CARD_3 = auto()
    CARD_4 = auto()
    CARD_5 = auto()
    CARD_6 = auto()
    CARD_7 = auto()
    CARD_8 = auto()
    CARD_9 = auto()
    CARD_PLUS_2 = auto()
    CARD_PLUS_4 = auto()
    CARD_SKIP = auto()
    CARD_WILDCARD = auto()
    CARD_REVERSE = auto()
