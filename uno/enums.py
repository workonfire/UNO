from enum import Enum, auto


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
    CARD_1: str = """________________
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
                     ¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"""
    CARD_2: str = """________________
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
    CARD_3: str = """"""  # TODO
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

    def __init__(self, card):
        self.card = card

    @property
    def art(self) -> str:  # TODO: get rid of the dictionary
        types = {'1': self.CARD_1,
                 '2': self.CARD_2,
                 '3': self.CARD_3,
                 '4': self.CARD_4,
                 '5': self.CARD_5,
                 '6': self.CARD_6,
                 '7': self.CARD_7,
                 '8': self.CARD_8,
                 '9': self.CARD_9,
                 '+2': self.CARD_PLUS_2,
                 '+4': self.CARD_PLUS_4,
                 'SKIP': self.CARD_SKIP,
                 'WILDCARD': self.CARD_WILDCARD,
                 'REVERSE': self.CARD_REVERSE}
        return types.get(self.card.card_type)
