import pytest
from poker import PKCard, Deck, Card, Hands, suits, ranks

def test_PKcard_init():
    card = PKcard('AC')
    assert card.rank == 'A' and card.suit == 'C'


