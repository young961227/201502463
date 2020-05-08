from abc import ABCMeta, abstractmethod

suits = 'CDHS'
ranks = '23456789TJQKA'

class Card(metaclass=ABCMeta):
    """Abstact class for playing cards
    """
    def __init__(self, rank_suit):
        if rank_suit[0] not in ranks or rank_suit[1] not in suits:
            raise ValueError(f'{rank_suit}: illegal card')
        self.card = rank_suit
        
    def __repr__(self):
        return self.card
    
    @abstractmethod
    def value(self):
        """Subclasses should implement this method
        """
        raise NotImplementedError("value method not implemented")

    # card comparison operators
    def __gt__(self, other): return self.value() > other.value()
    def __ge__(self, other): return self.value() >= other.value()
    def __lt__(self, other): return self.value() < other.value()
    def __le__(self, other): return self.value() <= other.value()
    def __eq__(self, other): return self.value() == other.value()
    def __ne__(self, other): return self.value() != other.value()


# ## Poker Card class
# 단, Poker game에서 두 카드를 비교할 때 suit과 무관하게 rank로만 결정한다. 오름차 순서로 나열하면 다음과 같다. 
# 
#     '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'
# 
# Q. `Card` class를 상속받아 Poker game용 `PKCard` class를 정의하라. 
# >Hint: 위 순서대로 정수를 return하는 value() method를 implementation해야 한다.

# In[2]:


class PKCard(Card):
    """Card for Poker game
    """
    VALUE={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}    
    
    
    def __init__(self, rank):
        Card.__init__(self, rank)
        self.point=PKCard.VALUE.get(rank[0])
    
    def value(self):
        return self.point



if __name__ == '__main__':
    c1 = PKCard('QC')
    c2 = PKCard('9D')
    c3 = PKCard('9C')
    print(f'{c1} {c2} {c3}')

    # comparison
    print(c1 > c2 == c3)

    # sorting
    cards = [c1, c2, c3, PKCard('AS'), PKCard('2D')]
    sorted_cards = sorted(cards)
    print(sorted_cards)
    cards.sort()
    print(cards)


# ## Deck class
# Q. 다음 methods를 갖는 `Deck` class를 작성하라.
# 
# Methods:
# - `__init__(self, cls)`: `cls`는 card class name
# - shuffle
# - pop
# - `__str__`
# - `__len__(self)` to enable `len` builtin function
# - `__getitem__(self, index)` to enable indexing and slicing as well as iteration

# In[3]:


import random
class Deck:
    def __init__(self, cls):
        """Create a deck of 'cls' card class
        """ 
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append((cls(rank + suit)))
        self.mix = random.Random()
        
    def shuffle(self):
        self.mix.shuffle(self.cards)

    def pop(self):
        if not self.cards:
            raise ValueError("no card")
        return self.cards.pop()

    def __str__(self):
        return str(self.cards[:])

    def __getitem__(self, index):
        return self.cards[index]

    def __len__(self):
        return len(self.cards)
        pass

if __name__ == '__main__':
    deck = Deck(PKCard)  # deck of poker cards
    deck.shuffle()
    c = deck[0]
    print('A deck of', c.__class__.__name__)
    print(deck)
    # testing __getitem__ method
    print(deck[-5:])

    while len(deck) >= 10:
        my_hand = []
        your_hand = []
        for i in range(5):
            for hand in (my_hand, your_hand):
                card = deck.pop()
                hand.append(card)
        my_hand.sort(reverse=True)
        your_hand.sort(reverse=True)
        print(my_hand, '>', your_hand, '?', my_hand > your_hand)


# 위의 예에서 my_hand와 your_hand는 단순히 rank value가 가장 큰 것이 이긴다는 'high card' 족보만으로 따졌을 때이다. Poker의 패는 [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)에서 보듯이 다양한 족보가 있다.
# 
# ## Poker Hands
# 지난 Programming Assignement를 object-oriented로 설계 구현해 보자.
# 
# [List of poker hands](https://en.wikipedia.org/wiki/List_of_poker_hands)의 Hand rank category 표에 열거된 패의 rank 0..9 을 역순으로 9..0의 integer로 나열하면 hand ranking의 높고 낮음을 알수 있다. 이 수를 혼동하지 않도록 이라 하자.
# 
# Straight, flush, straight flush와 같이 rank가 다른 5장으로 패가 이뤄지는 경우, 
# hand ranking이 같으면
# 1. 5장끼리 rank value를 비교해서 판단해야 한다. 즉, reverse(decreading) order로 sorting하여 rank value를 비교하면 된다.
# 
# Hand ranking이 같다면, 예를 들어 둘 다 two pair로 동률 이루고 있다면
# 1. 높은 수 one pair의 rank value를 비교하고
# 2. 같으면, 낮은 one pair의 rank value를 비교하고
# 3. 같으면, 나머지 1장 끼리 value를 비교해서 승부를 가른다. 
# 
# 따라서, 패가 이뤄지는지 찾는 method들은 (hand_ranking, five_cards) tuple로 return한다면
# tuple 비교하는 Python rule에 따라 행하면 충분하게 된다.
# 이때, 이어지는 five_cards는 rank가 높은 순서로 sorting하거나, rank가 같은 것이 있다면(find_a_kind의 경우)
# tie-breaking이 먼저 일어날 카드들을 앞으로 배치해야 list간 비교로 간편히 비교 가능히다. (four cards, tripple cards, high pair)
# 
# Q. *PA. Find poker hands* 문제에서 function으로 구현한 것들을 OOP로 rewriting하라.
# 
# 중요: hand ranking 찾기, hand ranking이 같을 때 tie-break이 제대로 적용되는지를 검증하기 위한
# 가능한 모든 test case를 20개 이상을 작성함으로써, unit test가 *거의* 모든 경우를 포함하고 있음을
# 보여야 한다.

# In[4]:


class Hands:
    def __init__(self, cards):
        if len(cards) != 5:
            raise ValueError('not 5 cards')
        self.cards = sorted(self, reverse=True)
        
    def is_flush(self):
        
        a = self[0][1]
        count = 0
        for i in self:
            if i[-1] == a:
                count+=1
        if count == 5: return True
        else : return False
        
    def is_straight(self):
        values = dict(zip(ranks, range(2, 2+len(ranks))))
        a = []
        for i in self:
            a.append(values[i[0]])
        b = sorted(a)
        if (b[0]+1 == b[1]) and (b[1]+1 == b[2]) and (b[2]+1 == b[3]) and (b[3]+1 == b[4]):
            return True
        else: return False
    
    def classify_by_rank(self):  
        rank_dic = {}
        for i in ranks:
            a = []
            for j in self:
                if j[0] == i:
                    a.append(j)
            rank_dic[i] = a
        return rank_dic
        pass
    
    def find_a_kind(self):
        """Find if one pair, two pair, or three, four of a kind, or full house
    
        :return: hand-ranking name including 'Full house'
        """
        values = dict(zip(ranks, range(2, 2+len(ranks))))
        cards_by_ranks = Hands.classify_by_rank(self)
        twocount = 0
        threecount = 0
        for key in cards_by_ranks.keys() :
            if len(cards_by_ranks[key]) == 2 :
                twocount += 1
            elif len(cards_by_ranks[key]) == 3 :
                threecount += 1
            elif len(cards_by_ranks[key]) == 4 :
                return 'four card'
        if (twocount == 1) and (threecount == 1) :
            return 'full house'
        elif (twocount == 0) and (threecount == 1) :
            return 'three card'
        elif (twocount == 1) and (threecount == 0) :
            return 'one pair'
        elif(twocount == 2) and (threecount == 0) :
            return 'two pairs'
        else:
            a = []
            for i in cards_by_ranks.keys():
                if len(cards_by_ranks[i]) > 0:
                    a.append(values.get(i))
            sorted(a)
            b = a[4]
            for key, value in values.items():
                if value == b:
                    return key            
        pass

    def tell_hand_ranking(self):
        values = dict(zip(ranks, range(2, 2+len(ranks))))
        countf, counts, countr, countb = 0, 0, 0, 0
        if Hands.is_flush(self)== True :
            countf += 1
            countr += 1
        if (Hands.is_straight(self)) :
            counts += 1
        if countr == 2 :
            return 'royal straight flush'
        elif (countf == 1) and (counts == 1) :
            return 'straight flush'
        elif (countf == 1):
            return 'flush'
        elif (counts == 1):
            return 'straight'
        
        if (Hands.is_flush(self) == False) and (Hands.is_straight(self)==False) and (Hands.find_a_kind(self) == None):
            a = []
            for i in cards_by_ranks.keys():
                if len(cards_by_ranks[i]) > 0:
                    a.append(values.get(i))
            sorted(a)
            b = a[4]
            for key, value in values.items():
                if value == b:
                    return key
        else:
            return Hands.find_a_kind(self)
        
    def rank(self):
        hand_dict = {"royal straight flush":23, "straight flush": 22,"back straight":21, "four card":20, "full house":19, "flush":18, "straight":17, "three card":16, "two pairs":15, "one pair":14,'2':1,'3':2,'4':3,'5':4,'6':5,'7':6,'8':7,'9':8,'T':9,'J':10,'Q':11,'K':12,'A':13}
        a = hand_dict[Hands.tell_hand_ranking(self)]
        return a
    def detail_rank(self):
        VALUE={'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'T':10,'J':11,'Q':12,'K':13,'A':14}
        a=[]
        rank = []
        count = []
        for i in self:
            a.append(i[0])
            b = sorted(list(set(a)))
        sum=0
        for x in range(len(b)):
            count.append(a.count(b[x])*VALUE.get(b[sum]))
            sum +=1
        return sorted(count)

    def compare(self, other):
        if Hands.rank(self) > Hands.rank(other):
            return 'player1 win!' 
        elif Hands.rank(self) < Hands.rank(other):
            return 'player2 win!'
        elif Hands.rank(self) == Hands.rank(other):
            x,y = Hands.detail_rank(self), Hands.detail_rank(other)
            if max(x) > max(y):
                    return 'player1 win!'
            elif max(x) < max(y):
                    return 'player2 win!' 
            elif max(x) == max(y):
                if x[-2] > y[-2]:
                        return 'player1 win!'
                elif x[-2] < y[-2]:
                        return 'player2 win!'
                elif x[-2] == y[-2]:
                    if x[-3] > y[-3]:
                        return 'player1 win!'
                    elif x[-3] < y[-3]:
                        return 'player2 win!'
                    elif x[-3] == y[-3]:
                        return 'same rank'
    
if __name__ == '__main__':
    import sys
    def test(did_pass):
        """  Print the result of a test.  """
        linenum = sys._getframe(1).f_lineno   # Get the caller's line number.
        if did_pass:
            msg = "Test at line {0} ok.".format(linenum)
        else:
            msg = ("Test at line {0} FAILED.".format(linenum))
        print(msg)

    # your test cases here
    a=['JC', 'JS', '3S', '3S', 'JH']
    b=['JD', 'JC', 'JH', '7C', '7S']
    print("1--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')
    
    a=['JC', '6S', 'KS', '3S', 'JH']
    b=['AD', 'KS', 'JD', 'JC', '7S']
    print("2--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')
    
    a=['JC', '6S', '6H', '5S', 'JH']
    b=['5D', 'JS', 'JD', '6C', '5C']
    print("3--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['8C', '9S', 'TS', 'JS', 'QH']
    b=['AD', '7S', 'JH', 'JC', '7S']
    print("4--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['AD', 'KD', 'JD', '3D', '7D']
    b=['5C', 'TS', 'QS', 'KS', 'JH']
    print("5--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['4C', '6H', '5S', '8D', '7D']
    b=['9D', '9H', '8S', '5D', '9C']
    print("6--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['4D', '6D', '5D', '9D', '8D']
    b=['2D', '3D', '4D', '5D', '6D']
    print("7--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')
    
    a=['JD', 'AD', 'KD', 'QD', 'TD']
    b=['6D', '2S', '4H', '5C', '3S']
    print("8--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['JC', '6S', 'KS', '3S', 'JH']
    b=['AD', 'KS', 'JH', 'JC', '7S']
    print("9--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')
    
    a=['JC', '6S', 'KS', '3S', 'JH']
    b=['KD', 'KS', 'JH', 'JC', '7S']
    print("10--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')

    a=['3S','4S','5S','6S','7S']
    b=['3D','4H','KD','6C','7D']
    print("11--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['2D','2D','4D','6H','7D']
    b=['2S','2H','8C','7S','6S']
    print("12--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player2 win!')

    a=['3S','3H','3C','3D','7S']
    b=['7H','7D','3D','TS','KS']
    print("13--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')

    a=['3S','5S','8S','KS','6S']
    b=['QS','7C','KS','5H','8H']
    print("14--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')

    a=['3S','2H','4C','6D','5S']
    b=['3H','QH','6S','7D','2S']
    print("15--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')

    a=['3S','3H','3C','2D','2S']
    b=['4S','6H','QC','2D','JS']
    print("16--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['2S','2H','3C','3D','7S']
    b=['4H','7H','2C','3H','KC']
    print("17--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['3S','3H','6C','8A','TC']
    b=['4S','4H','3C','2D','7S']
    print("18--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['3S','5H','2C','KD','AS']
    b=['4S','2H','5C','QD','TS']
    print("19--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    
    a=['3S','3H','7C','6D','KS']
    b=['3D','3C','6C','2D','7S']
    print("20--------------------")
    print(Hands.tell_hand_ranking(a))
    print(Hands.tell_hand_ranking(b))
    test(Hands.compare(a,b) == 'player1 win!')
    pass
