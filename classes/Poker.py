if __name__ != "__main__":
    from classes.Card import *
    from classes.Deck import *
    from classes.Hand import *
    from classes.Player import *
else:
    from Card import *
    from Deck import *
    from Hand import *
    from Player import *

import os
import time

class FiveCardDraw:
    def deal(self):
        self.deck.shuffle()
        i = 0
        self.currentPlayers = []
        while(i<5):
            for player in self.players:
                card = self.deck.cards.pop(0)
                player.hand.append(card)
            i+=1
        for player in self.players:
            self.currentPlayers.append(player)
            player.chips -= 5
            self.pot += 5
            player.observeHand()

    def takeBets(self):
        if len(self.currentPlayers) > 1:
            i = 0
            while i < len(self.currentPlayers):
                player = self.currentPlayers[i]
                if self.hiBet == player.currentBet:
                    to_play = 0
                else:
                    to_play = self.hiBet - player.currentBet
                    print("%s must call %s to stay in"%(player.name, to_play))
                bet = player.calculateBet(to_play)
                if bet < 0:
                    self.currentPlayers.pop(i)
                    #player folds
                    print("%s folds\n"%player.name)
                    time.sleep(1)
                else:
                    if bet == 0:
                        print("%s Checks\n"%(player.name))
                        time.sleep(1)
                    elif bet == to_play:
                        print("%s Calls\n"%player.name)
                        time.sleep(1)
                    else:
                        print("%s bets %s\n"%(player.name, bet))
                        time.sleep(1)
                    if bet > 0:
                        self.hiBet = player.currentBet
                    self.pot += bet
                    i += 1

        for player in self.currentPlayers:
            if player.currentBet == self.hiBet:
                pass
            else:
                self.takeBets()

    def presentWinner(self):
        currentWinner = None
        for player in self.currentPlayers:
            if not currentWinner:
                currentWinner = player
            elif currentWinner.hand.rank < player.hand.rank:
                currentWinner = player
        currentWinner.chips += self.pot
        print("%s wins pot of %s and now has %s chips"%
            (currentWinner.name,self.pot, currentWinner.chips))
        print("Winners Hand:")
        currentWinner.displayHand()
        input("Press enter to continue: ")

    def newRound(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.pot = 0
        self.hiBet = 0
        self.deck = Deck()
        for player in self.players:
            player.currentBet = 0
            player.hand=[]

    def __init__(self, players):
        os.system('cls' if os.name == 'nt' else 'clear')
        self.hiBet = 0
        self.pot = 0
        self.deck = Deck()
        self.players = players
        self.currentPlayers = []
