if __name__ != "__main__":
    from classes.Card import *
    from classes.Deck import *
else:
    from Card import *
    from Deck import *

SUITE_VALUES = {
    "Disamonds": 4,
    "Hearts": 3,
    "Clubs": 2,
    "Spades": 1
}

def merge_hand(a, b):
    if not len(a) or not len(b):
        return a or b
    merged=[]
    i,j=0,0
    while(len(merged)<len(a)+len(b)):
        if(a[i].value < b[j].value):
            merged.append(a[i])
            i+=1
        else:
            merged.append(b[j])
            j+=1
        if i == len(a) or j == len(b):
            merged.extend(a[i:]) or merged.extend(b[j:])
            break
    return merged

def sort_hand(hand):
    if len(hand)<2:
        return hand
    a = sort_hand(hand[:len(hand)//2])
    b = sort_hand(hand[len(hand)//2:])
    return merge_hand(a,b)

def count_matches(hand, currentMatches):
    """(hand, int)-> [[]]
    """
    if len(hand) < 2:
        return(currentMatches)
    hand=sort_hand(hand)
    count=1
    card=hand.pop(0)
    i = 0
    while i < len(hand):
        if card.value == hand[i].value:
            hand.pop(i)
            count += 1
        i+=1
    if count > 1:
        currentMatches.append([card.value, count])
    return count_matches(hand, currentMatches)

class Hand:
    def hasFlush(self):
        i = 0
        hand = self.hand
        card = hand[i]
        suite = card.suite
        while i < len(hand):
            if suite != hand[i].suite:
                return False
            i += 1
        return True

    def hasStraight(self):
        i = 0
        hand = self.hand
        while i < (len(hand)-1):
            temp = hand[i]
            if temp.value != (hand[i+1].value - 1):
                return False
            i += 1
        return True

    def hasFourOfAKind(self):
        i = 0
        while i < len(self.matches):
            if self.matches[i][1] == 4:
                return True
            i += 1
        return False

    def hasFullHouse(self):
        if len(self.matches) == 2:
            if self.matches[0][1] == 3 and self.matches[1][1] == 2:
                return True
            elif self.matches[0][1] == 2 and self.matches[1][1] == 3:
                return True
            else:
                return False
        else:
            return False

    def hasThreeofAKind(self):
        if len(self.matches) > 0:
            i = 0
            while i < len(self.matches):
                if self.matches[i][1] == 3:
                    return True
                i += 1
        return False

    def hasTwoPair(self):
        if len(self.matches) == 2:
            return True
        return False

    def hasPair(self):
        if len(self.matches) > 0:
            return True
        return False

    def rankHand(self):
        """(Hand)->int
        Given a five card hand this function will return an integer value
        rank of the poker hand.

        Idea:
        Define fixed values for
        Royal flush 120 bonus range 121-124
        Straight flush 102 bonus range 103-120
        Four of a kind 88 bonus range 89-102
        Full house 74 bonus range 75-88
        Flush 70 bonus range 71-74
        Straight 56 bonus range 57-70
        Three of a kind 42 bonus range 43-56
        Two Pair 28 bonus range 29-42
        Pair 14 bonus range 15-28
        High Card-nill range 1-14
        """
        if self.hasStraight() and self.hasFlush():
            #check for royal flush
            if self.hand[4].value == 14:
                self.got = "ROYAL FLUSH"
                self.rank += 120
                suite = self.hand[1].suite
                self.rank += SUITE_VALUES[suite]
            else:
                self.got = "SRAIGHT FLUSH"
                self.rank += 102
                suite = self.hand[1].suite
                self.rank += SUITE_VALUES[suite]
                self.rank += self.hand[4].value
        elif self.hasFourOfAKind():
            self.got = "4 OF A KIND"
            self.rank += 88
            self.rank += self.matches[0][0]
        elif self.hasFullHouse():
            self.got = "FULL HOUSE"
            self.rank += 74
            if self.matches[0][1] == 3:
                self.rank += self.matches[0][0]
            else:
                self.rank += self.matches[1][0]
        elif self.hasFlush():
            self.got = "FLUSH"
            self.rank += 70
            suite = self.hand[1].suite
            self.rank += SUITE_VALUES[suite]
        elif self.hasStraight():
            self.got = "STRAIGHT"
            self.rank += 56
            self.rank += self.hand[4].value
        elif self.hasThreeofAKind():
            self.got = "3 OF A KIND"
            self.rank += 42
            self.rank += self.matches[0][0]
        elif self.hasTwoPair():
            self.got = "Two PAIR"
            self.rank = 28
            if self.matches[0][0] > self.matches[1][0]:
                self.rank += self.matches[0][0]
            else:
                self.rank += self.matches[1][0]
        elif self.hasPair():
            self.got = "PAIR"
            self.rank = 14
            self.rank += self.matches[0][0]
        else:
            self.got = "HIGH CARD"
            self.rank = self.hand[4].value

    def __init__(self, hand):
        self.hand = sort_hand(hand)
        self.matches = count_matches(hand, [])
        self.got = "Ranking"
        self.rank = 0
        self.rankHand()
        if len(self.hand) != 5:
            print("Hand is too small")

if __name__ == "__main__":
    testDeck = Deck()
    testDeck.shuffle()
    hand = testDeck.cards[:5]
    testHand = Hand(hand)
    print("\nHand got %s: rank:%s"%(testHand.got,testHand.rank))
    for card in testHand.hand:
        print(card)
