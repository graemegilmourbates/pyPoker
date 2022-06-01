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
    5: "Billy",
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
    os.system('cls' if os.name == 'nt' else 'clear')
    player_count = input("How many players? 1-9:  ")
    player_count = int(player_count)
    players = generate_players(player_count)
    newHuman = HumanPlayer()
    players.append(newHuman)
    testGame = FiveCardDraw(players)
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        for player in testGame.players:
            print("-- %s: %s Chips."%(player.name, player.chips))
        toPlay = input("Want to play a round?\n")
        if toPlay[0].upper() == "Y":
            play_round(testGame)
        else:
            break
