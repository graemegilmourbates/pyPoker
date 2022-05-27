from classes.Deck import *
from classes.Card import *
from classes.Hand import *
from classes.Player import *
from classes.Poker import *


def generate_players(number):
    i = 0
    players = []
    while i < number:
        players.append(Player(i))
        i += 1
    return players

if __name__ == "__main__":
    players = generate_players(4)
    testGame = FiveCardDraw(players)
    games = 0
    while games < 1:
        testGame.newRound()
        testGame.deal()
        testGame.takeBets()

        i = 0
        while i < len(players):
            #testGame.players[i].displayHand()
            i += 1
        games += 1
        testGame.presentWinner()
