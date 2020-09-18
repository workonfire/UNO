class InvalidCardException(Exception):
    pass


class CardNotInPossessionError(Exception):
    pass


class CardNotPlayableError(Exception):
    pass


class WinnerAlreadySetException(Exception):
    pass
