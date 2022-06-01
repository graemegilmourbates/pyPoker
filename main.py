from classes.Deck import *
from classes.Card import *
from classes.Hand import *
from classes.Player import *
from classes.Poker import *

import os

PLAYER_NAMES = {
    0: "Mary",
    1: "Thor",
    2: "Bruce",
    3: "Clark",
    4: "Jeane",
    6: "Beatrice",
    7: "Shaggy",
    8: "Snoop",
    9: "Leia"
}

def generate_players(number):
    i = 0
    players = []
    while i < number:
        players.append(Player(PLAYER_NAMES[i]))
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
        for player in testGame.players:
            print("%s: %s Chips."%(player.name, player.chips))
        print("You have %s Chips." % newHuman.chips)
        toPlay = input("Want to play a round?\n")
        if toPlay.upper() == "YES":
            play_round(testGame)
        else:
            break
