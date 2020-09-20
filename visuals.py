from colorama import init, deinit


def color_print(color, text, no_newline=False):
    init(autoreset=True)
    print(color + text, end='') if no_newline else print(color + text)
    deinit()


class CardVisual:
    CARD_1 = ["________________",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░░░░██╗░░░░░▌",
              "▌░░░░░███║░░░░░▌",
              "▌░░░░░╚██║░░░░░▌",
              "▌░░░░░░██║░░░░░▌",
              "▌░░░░░░██║░░░░░▌",
              "▌░░░░░░╚═╝░░░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"]
    CARD_2 = ["________________",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░██████╗░░░░▌",
              "▌░░░╚════██╗░░░▌",
              "▌░░░░█████╔╝░░░▌",
              "▌░░░██╔═══╝░░░░▌",
              "▌░░░███████╗░░░▌",
              "▌░░░╚══════╝░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "▌░░░░░░░░░░░░░░▌",
              "¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯¯"]
    CARD_3 = []
    CARD_4 = []
    CARD_5 = []
    CARD_6 = []
    CARD_7 = []
    CARD_8 = []
    CARD_9 = []
    CARD_PLUS_2 = []
    CARD_PLUS_4 = []
    CARD_SKIP = []
    CARD_WILDCARD = []
    CARD_REVERSE = []

    def __init__(self, card):
        self.card = card

    @property
    def art(self) -> str:
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
