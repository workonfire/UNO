from enum import Enum, auto
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from uno.game import Card


class Type(Enum):
    def __str__(self) -> str:
        return self.name


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


class CardVisual:
    CARD_0: str = """"""
    CARD_1: str = """
    ________________
    ▌░░░░░░░░░░░░░░▌
    ▌░░░░░░░░░░░░░░▌
    ▌░░░░░░██╗░░░░░▌
    ▌░░░░░███║░░░░░▌
    ▌░░░░░╚██║░░░░░▌
    ▌░░░░░░██║░░░░░▌
    ▌░░░░░░██║░░░░░▌
    ▌░░░░░░╚═╝░░░░░▌
    ▌░░░░░░░░░░░░░░▌
    ▌░░░░░░░░░░░░░░▌
    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯
    """
    CARD_2: str = """
    ________________
    ▌░░░░░░░░░░░░░░▌
    ▌░░░░░░░░░░░░░░▌
    ▌░░░██████╗░░░░▌
    ▌░░░╚════██╗░░░▌
    ▌░░░░█████╔╝░░░▌
    ▌░░░██╔═══╝░░░░▌
    ▌░░░███████╗░░░▌
    ▌░░░╚══════╝░░░▌
    ▌░░░░░░░░░░░░░░▌
    ▌░░░░░░░░░░░░░░▌
    ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"""
    CARD_3: str = """"""
    CARD_4: str = """"""
    CARD_5: str = """"""
    CARD_6: str = """"""
    CARD_7: str = """"""
    CARD_8: str = """"""
    CARD_9: str = """"""
    CARD_PLUS_2: str = """"""
    CARD_PLUS_4: str = """"""
    CARD_SKIP: str = """"""
    CARD_WILDCARD: str = """"""
    CARD_REVERSE: str = """"""

    def __init__(self, card: 'Card'):
        self.card: 'Card' = card
        self.art: str = getattr(self, self.card.card_type.name)
