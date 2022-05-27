import random
if __name__ != "__main__":
    from classes.Card import *
else:
    from Card import *

def perfect_shuffle(cards):
    """(Deck)->Deck
    Given a deck of cards, preforms a perfect
    shuffle. Not an ideal shuffle.
    """
    #Split deck in half
    a = cards[:len(cards)//2]
    b = cards[len(cards)//2:]
    #Initialize a new deck
    newDeck = []
    #Iterate through two halfs
    i = 0
    while i < 26:
        #Add item from first half then second half
        newDeck.append(a[i])
        newDeck.append(b[i])
        i+=1
    #Return new shuffled deck
    return(newDeck)

def split_shuffle(cards):
    """(Deck)->Deck
    Given a deck of cards, continously split the Deck
    until you have
    """
    if(len(cards)>2):
        a = cards[:len(cards)//2]
        b = cards[len(cards)//2:]
        a = split_shuffle(a)
        b = split_shuffle(b)
        return a + b
    elif(len(cards)==1):
        return cards
    else:
        a=cards[1]
        b=cards[0]
        return([a,b])

def fisher_yates_shuffle(cards):
    i = 0
    while(i < len(cards)):
        index = random.randint(0,51)
        temp = cards[index]
        cards[index]=cards[i]
        cards[i]=temp
        i+=1
    return cards

class Deck:
    def perfectShuffle(self):
        self.cards = perfect_shuffle(self.cards)

    def splitShuffle(self):
        self.cards = split_shuffle(self.cards)

    def fisherYatesShuffle(self):
        self.cards = fisher_yates_shuffle(self.cards)

    def shuffle(self):
        self.fisherYatesShuffle()
        self.splitShuffle()
        self.perfectShuffle()

    def __init__(self):
        self.cards=[]
        i=0
        while(i<52):
            card = Card(i)
            self.cards.append(card)
            i+=1
