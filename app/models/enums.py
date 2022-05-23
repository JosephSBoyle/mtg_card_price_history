from enum import Enum


class Format(str, Enum):
    """The formats in which a card can be sold."""

    paper = "paper"
    """A paper card."""

    magic_the_gathering_online = "mtgo"
    """A magic the gathering online card."""


class Vendor(str, Enum):
    """The vendors for which price quotes are available."""

    cardmarket = "cardmarket"
    cardkingdom = "cardkingdom"
    cardsphere = "cardshpere"
    tcgplayer = "tcgplayer"

    # online only vendor
    cardhoarder = "cardhoarder"


class Printing(str, Enum):
    """The card printing."""

    foil = "foil"
    """A foil card."""
    normal = "normal"
    """A non-foil card."""


class QuoteType(str, Enum):
    """The type of price quote."""

    retail = "retail"
    """The retail price of a card."""
    buylist = "buylist"
    """The buylist price of a card."""
