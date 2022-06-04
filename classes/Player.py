if __name__ != "__main__":
    from classes.Card import *
    from classes.Deck import *
    from classes.Hand import *
else:
    from Card import *
    from Deck import *
    from Hand import *

import random
import math

class HumanPlayer:
    def observeHand(self):
        self.hand = Hand(self.hand)

    def displayHand(self):
        hand = ""
        for card in self.hand.hand:
            hand += str(card)
            hand += " | "
        print("You have %s Chips. Your Hand:"%(self.chips))
        print(hand)

    def calculateBet(self, toCall):
        print("\n")
        self.displayHand()
        print("\n")
        bet = input("Your bet: ")
        try:
            bet = int(bet)
            if(bet < toCall):
                return -1
        except ValueError:
            if bet.upper() == "CHECK":
                bet = 0
            elif bet.upper() == "FOLD":
                bet = -1
                return -1
            elif bet.upper() == "CALL":
                bet = toCall
            else:
                bet = toCall
        self.chips -= bet
        self.currentBet += bet
        return bet


    def __init__(self,name):
        self.currentBet=0
        self.chips=250
        self.hand = []
        self.name = name

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
        r = (self.hand.rank/124)
        max = round((self.chips) * r)
        if self.playStyle == "Confident":
            max_bet = max
        elif self.playStyle == "Mid":
            if r > 0.75:
                max_bet = round(max * r)
            elif r > 0.4:
                max_bet = abs(round(max * (math.cos(90-r))))
            else:
                max_bet = max//3
        else:
            max_bet = round(max*r)

        # Doesnt bet on just hi card
        if round(r*100) < 9:
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
            elif self.currentBet/toCall > 1:
                bet = toCall
                self.currentBet += bet
                self.chips -= bet
            else:
                bet = -1
            return bet

    def __init__(self, name):
        #Define play styles
        #Confident, Conservative, Mid
        confidence = random.randint(0, 100)
        if confidence < 20:
            self.playStyle = "Conservative"
        elif confidence < 80 :
            self.playStyle = "Mid"
        else:
            self.playStyle = "Confident"
        self.currentBet=0
        self.chips=250
        self.hand = []
        self.name = name

    def __str__(self):
        return("Player %s" % self.name)
