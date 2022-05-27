from classes.Deck import *
from classes.Card import *
from classes.Hand import *
from classes.Player import *
from classes.Poker import *

import os

def generate_players(number):
    i = 0
    players = []
    while i < number:
        players.append(Player(i))
        i += 1
    return players

def play_round(game):
    testGame.newRound()
    testGame.deal()
    testGame.takeBets()
    testGame.presentWinner()

if __name__ == "__main__":
    players = generate_players(3)
    newHuman = HumanPlayer()
    players.append(newHuman)
    testGame = FiveCardDraw(players)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("You have %s Chips." % newHuman.chips)
        toPlay = input("Want to play a round?\n")
        if toPlay.upper() == "YES":
            play_round(testGame)
        else:
            break
