import pytest, random, enum
from poker import PKCard, Deck, Hands, Card, suits, ranks, Ranking


def test_PKCard_init():
    card = PKCard('AC')
    assert card.rank == 'A' and card.suit == 'C'
    assert card.card == 'AC'

def test_PKCard_init_exception():
    for face in ['10S', 'BD', 'TA']:
        with pytest.raises(ValueError):
            PKCard(face)

def test_PKCard_repr():
    assert repr(PKCard('AC')) == 'AC'

@pytest.fixture
def all_faces():
    return [r+s for r in ranks for s in suits]

def test_PKCard_value(all_faces):
    for face in all_faces:
        card, expected = PKCard(face), PKCard.values[face[0]]
        assert card.value() == expected

@pytest.fixture
def c9C():
    return PKCard('9C')

@pytest.fixture
def c9H():
    return PKCard('9H')

@pytest.fixture
def cTH():
    return PKCard('TH')

def test_PKCard_comp(c9C, c9H, cTH):
    assert c9C == c9C and c9C == c9H
    assert c9H < cTH and c9C < cTH
    assert c9C <= c9H <= cTH
    assert cTH > c9H and cTH > c9C
    assert cTH >= c9H >= c9C
    assert c9C != cTH and c9H != cTH

def test_PKCard_sort(all_faces):
    all_cards = [PKCard(r+s) for r in ranks for s in suits ]
    import random
    random.shuffle(all_cards)
    all_cards.sort()
    assert [c.value() for c in all_cards] == sorted([i for s in suits for i in range(2,2+len(ranks))])

@pytest.fixture
def deck():
    return Deck(PKCard)

def test_Deck_init(deck):
    assert len(deck.cards) == 52
    assert isinstance(deck.cards[0], PKCard)

def test_Deck_pop(deck):
    card = deck.pop()
    assert card.rank == ranks[-1] and card.suit == suits[-1] \
        and len(deck.cards) == 52 - 1

def test_Deck_len(deck):
    deck.pop(); deck.pop()
    assert len(deck.cards) == deck.__len__() == len(deck) == 52 - 2

def test_Deck_getitem(deck):
    assert (deck[10].rank, deck[10].suit) \
        == (deck.cards[10].rank, deck.cards[10].suit)
    
def test_is_flush(all_faces):
    card = []
    for i in all_faces:
        card.append(i)
    random.shuffle(card)
    my_card = card[5:]
    assert Hands.is_flush(my_card) == False


non_flush_suit = 'CHSDS'
flush_suit = 'SSSSS'
test_cases = {
    Ranking.STRAIGHT_FLUSH: (
        tuple(zip('AKQJT', flush_suit)),
        tuple(zip('KQJT9', flush_suit)),
    ),
    Ranking.FOUR_OF_A_KIND:(
        tuple(zip('TTTTQ', non_flush_suit)),
        tuple(zip('9999A', non_flush_suit)),
    ),
    Ranking.FULL_HOUSE:(
        tuple(zip('88877', non_flush_suit)),
        tuple(zip('22299', non_flush_suit)),
    ),
    Ranking.FLUSH:(
        tuple(zip('AJT98', flush_suit)),
        tuple(zip('AJ987', flush_suit)),
    ),
    Ranking.STRAIGHT:(
        tuple(zip('AKQJT', non_flush_suit)),
        tuple(zip('KQJT9', non_flush_suit)),
    ),
    Ranking.THREE_OF_A_KIND: (
        tuple(zip('888A9', non_flush_suit)),
        tuple(zip('888A7', non_flush_suit)),
    ),
    Ranking.TWO_PAIRS: (
        tuple(zip('AA998', non_flush_suit)),
        tuple(zip('AA778', non_flush_suit)),
        tuple(zip('JJTTK', non_flush_suit)),
    ),
    Ranking.ONE_PAIR:(
        tuple(zip('88AT9', non_flush_suit)),
        tuple(zip('88AT7', non_flush_suit)),
        tuple(zip('77AKQ', non_flush_suit)),
    ),
}

def cases(*rankings) :
    if not rankings:
        rankings = test_cases.keys()
    return \
        [ ([r+s for r, s in case], ranking)
                    for ranking in rankings
                        for case in test_cases[ranking]
        ]
@pytest.mark.parametrize("faces, expected", cases(Ranking.STRAIGHT))
def test_is_straight(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.is_straight(hand)
    assert result == True
    assert sorted(hand) == sorted(hand_org)

@pytest.mark.parametrize("faces, expected", cases(Ranking.FLUSH))
def test_is_flush(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.is_flush(hand)
    assert result == True

@pytest.mark.parametrize("faces, expected", cases(Ranking.FOUR_OF_A_KIND))
def test_is_find_a_kind(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.find_a_kind(hand)
    assert result == 'four card'

@pytest.mark.parametrize("faces, expected", cases(Ranking.THREE_OF_A_KIND))
def test_is_find_a_kind(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.find_a_kind(hand)
    assert result == 'three card'

@pytest.mark.parametrize("faces, expected", cases(Ranking.TWO_PAIRS))
def test_is_find_a_kind(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.find_a_kind(hand)
    assert result == 'two pairs'

@pytest.mark.parametrize("faces, expected", cases(Ranking.ONE_PAIR))
def test_is_find_a_kind(faces, expected):
    hand_org = [c for c in faces]
    random.shuffle(faces)
    hand = ([c for c in faces])
    result = Hands.find_a_kind(hand)
    assert result == 'one pair'



@pytest.mark.parametrize("faces, expected", cases())
def test_rank(faces, expected):
    hand_dict = {"royal straight flush":23, "straight flush": 22,"back straight":21, "four card":20, "full house":19, "flush":18, "straight":17, "three card":16, "two pairs":15, "one pair":14,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'T':9,'J':10,'Q':11,'K':12,'A':13}
    random.shuffle(faces)
    hand = ([c for c in faces])
    a = Hands.rank((hand))
    assert a == hand_dict[Hands.tell_hand_ranking(hand)]

def test_who_wins():
    hand_cases = [(faces) for faces, ranking in cases()]
    for hand in hand_cases:
        Hands.rank(hand)
    sorted_cases = sorted(hand_cases, reverse = True)
    assert sorted(sorted_cases) == sorted(hand_cases)
    print('\nHigh to low order:')
    for i, hand in enumerate(hand_cases):
        print(i, hand)