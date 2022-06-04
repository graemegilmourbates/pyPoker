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

class FiveCardStud:
    def deal(self):
        self.currentPlayers = []
        for player in self.players:
            if player.chips > 4:
                self.currentPlayers.append(player)
                player.chips -= 5
                self.pot += 5
        self.deck.shuffle()
        i = 0
        while(i<5):
            for player in self.currentPlayers:
                card = self.deck.cards.pop(0)
                player.hand.append(card)
            i+=1
        for player in self.currentPlayers:
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
                if bet < to_play:
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

    def takeGuiBets(self, player):
        if self.hiBet == player.currentBet:
            to_play = 0
        else:
            to_play = self.hiBet - player.currentBet
        print("To play: %s"%to_play)
        bet = player.calculateBet(to_play)
        print("Bet %s"%bet)
        if bet < to_play:
            return(-1)
        else:
            self.pot += bet
            if bet < 0:
                return(-1)
            if bet > to_play:
                self.hiBet = player.currentBet
            if bet == 0:
                return(0)
            elif bet == to_play:
                return(1)
            else:
                return(2)

    def takeUserGuiBet(self, user, bet):
        if user.currentBet == self.hiBet:
            to_play = 0
        else:
            to_play = self.hiBet - user.currentBet
        if bet < to_play:
            return(-1)
        else:
            self.pot += bet
            user.chips -= bet
            if bet > to_play:
                self.hiBet = user.currentBet + bet
            if bet == 0:
                return(0)
            elif bet == to_play:
                user.currentBet += bet
                return(1)
            else:
                user.currentBet += bet
                return(2)

    def presentGuiWinner(self):
        currentWinner = None
        currentWinners = []
        for player in self.currentPlayers:
            if not currentWinner:
                currentWinner = player.hand.rank
                currentWinners = [player]
            elif currentWinner < player.hand.rank:
                currentWinner = player.hand.rank
                currentWinners = [player]
            elif currentWinner == player.hand.rank:
                currentWinners.append(player)
        if len(currentWinners) == 1:
            winner = currentWinners[0]
            winner.chips += self.pot
            return winner
        else:
            print("Split Pot!!!")
            splits = len(currentWinners)
            pot_split = self.pot/splits
            for player in currentWinners:
                player.chips += pot_split
            return currentWinners
        input("Press enter to continue: ")

    def presentWinner(self):
        currentWinner = None
        currentWinners = []
        for player in self.currentPlayers:
            if not currentWinner:
                currentWinner = player.hand.rank
                currentWinners = [player]
            elif currentWinner < player.hand.rank:
                currentWinner = player.hand.rank
                currentWinners = [player]
            elif currentWinner == player.hand.rank:
                currentWinners.append(player)
        if len(currentWinners) == 1:
            winner = currentWinners[0]
            winner.chips += self.pot
            print("%s wins pot of %s and now has %s chips"%
                (winner.name,self.pot, winner.chips))
            print("Winners Hand:")
            winner.displayHand()
        else:
            print("Split Pot!!!")
            splits = len(currentWinners)
            pot_split = self.pot/splits
            for player in currentWinners:
                print("%s wins %s"%(player.name, pot_split))
                print("%s hand:"%player.name)
                player.displayHand()
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
