if __name__ != "__main__":
    from classes.Card import *
    from classes.Deck import *
    from classes.Hand import *
else:
    from Card import *
    from Deck import *
    from Hand import *

import random

class HumanPlayer:
    def observeHand(self):
        self.hand = Hand(self.hand)

    def displayHand(self):
        hand = ""
        for card in self.hand.hand:
            hand += str(card)
            hand += " | "
        print(hand)

    def calculateBet(self, toCall):
        print("\n")
        self.displayHand()
        print("\n")
        bet = input("Your bet: ")
        try:
            bet = int(bet)
        except ValueError:
            if bet.upper() == "CHECK":
                bet = 0
            elif bet.upper() == "FOLD":
                bet = -1
                return -1
            elif bet.upper() == "CALL":
                bet = toCall
        self.chips -= bet
        self.currentBet += bet
        return bet


    def __init__(self):
        self.currentBet=0
        self.chips=250
        self.hand = []
        self.name = input("Enter Your Name: ")

class Player:
    def observeHand(self):
        self.hand = Hand(self.hand)

    def displayHand(self):
        hand = ""
        for card in self.hand.hand:
            hand += str(card)
            hand += " | "
        print(hand)

    def calculateBet(self, toCall):
        bet = -1
        if self.playStyle == "Confident":
            impulse = random.randrange(2,10)
        elif self.playStyle == "Mid":
            impulse = random.randrange(0,6)
        else:
            impulse = random.randrange(-2,5)
        max_bet = self.hand.rank // 3
        max_bet += impulse
        # Doesnt bet on just hi card
        if self.hand.rank < 14:
            if toCall == 0:
                bet = 0
                self.currentBet = bet
                self.chips -= bet
                return 0
            else:
                return -1
        else:
            if  (toCall + self.currentBet) < (max_bet):
                bet = (max_bet-self.currentBet)
                if bet > 0:
                    #flux bet
                    bet = random.randint(toCall, bet)
                elif bet < 0:
                    bet = 0
                self.currentBet += bet
                self.chips -= bet
            elif toCall == 0:
                bet = 0
            elif (max_bet) > (toCall-3):
                bet = toCall
                self.currentBet += bet
                self.chips -= bet
            else:
                bet = -1
            return bet

    def __init__(self, name):
        #Define play styles
        #Confident, Conservative, Mid
        confidence = random.randint(0,3)
        if confidence == 0:
            self.playStyle = "Conservative"
        elif confidence == 1:
            self.playStyle = "Mid"
        else:
            self.playStyle = "Confident"
        self.currentBet=0
        self.chips=250
        self.hand = []
        self.name = name

    def __str__(self):
        return("Player %s" % self.name)
