import tkinter as tk
import tkinter.messagebox as messagebox
from tkinter import ttk
from PIL import Image, ImageTk

from classes.Deck import *
from classes.Card import *
from classes.Hand import *
from classes.Player import *
from classes.Poker import *

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


def get_card_image(card):
    image_src = ("cards/%s_%s.png"%(card.value, card.suite))
    card_image = Image.open(image_src)
    card_image = card_image.resize((150, 240), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(card_image)
    return img

def generate_players(number):
    i = 0
    players = []
    while i < number:
        players.append(Player(PLAYER_NAMES[i]))
        i += 1
    return players

class Game(tk.Tk):

    def __init__(self):
        self.userBet = 0
        tk.Tk.__init__(self)
        self.title("Five Card Draw")
        self.geometry("1000x550")
        self.resizable(False, False)
        #### Init Menu
        menu = tk.Menu(self)
        game = tk.Menu(menu)
        game.add_command(label="New Game")
        game.add_command(label="New Hand")
        menu.add_cascade(label="Game", menu=game)
        self.config(menu=menu)

    def onPlayerCountClick(self, option, playerName):
        self.introFrame.destroy()
        self.gameFrame(option, playerName)

    def introFrame(self):
        self.introFrame = tk.Frame(self)
        self.introFrame.pack()

        options=[1,2,3,4,5,6,7,8,9]
        var = tk.StringVar(value=options)
        intro_label = tk.Label(self.introFrame, text="Number of Players:")
        intro_label.grid(column=0, row=0)
        clicked=tk.IntVar()
        clicked.set(1)
        number_players = tk.OptionMenu(
            self.introFrame,
            clicked,
            *options
        )
        number_players.grid(column=1,row=0)

        player_name_label = tk.Label(self.introFrame, text="Your Name:")
        player_name_label.grid(column=0, row=2)
        player_name_input = tk.Entry(self.introFrame)
        player_name_input.grid(column=1, row=2)
        done_button = tk.Button(
            self.introFrame, text="Ready!",
            command=lambda: self.onPlayerCountClick(
                clicked.get(), player_name_input.get()
            )
        )
        done_button.grid(column=0,row=3)

    def gameFrame(self, player_count, user_name):
        self.game_frame = tk.Frame(self)
        self.game_frame.pack()
        self.ai_players = generate_players(player_count)
        self.user = HumanPlayer(user_name)
        self.players = []
        for player in self.ai_players:
            self.players.append(player)
        self.players.append(self.user)
        self.game = FiveCardStud(self.players)
        self.game.deal()
        self.temp_bet = 0
        self.tableDisplay()

    def tableDisplay(self):
        self.table_frame = tk.Frame(self.game_frame)
        self.table_frame.pack()
        # Display players at the top
        self.players_frame = tk.Frame(self.table_frame)
        self.players_frame.grid(column=0, row=0)
        i = 0
        for player in self.ai_players:
            player.player_frame = tk.Frame(self.players_frame)
            player.player_frame.grid(
                column=i, row=0,
                padx=10, pady=10
            )
            player.name_label = tk.Label(player.player_frame, text=player.name)
            player.name_label.grid(column=0, row=0)
            player.chips_label = tk.Label(
                player.player_frame, text="Chips: %s"%player.chips
            )
            player.chips_label.grid(column=0, row=1)
            player.bet_label = tk.Label(
                player.player_frame, text="Current Bet: %s"%player.currentBet
            )
            player.bet_label.grid(column=0, row=2)
            i += 1
        # Display pot in the middle
        self.pot_frame = tk.Frame(self.table_frame)
        self.pot_frame.grid(column=0, row=1)
        self.pot_label = tk.Label(
            self.pot_frame, text="Current Pot: %s"%self.game.pot
        )
        self.pot_label.grid(column=0, row=1)
        # Display User at the bottom
        self.user_frame = tk.Frame(self.table_frame)
        self.user_frame.grid(column=0, row=2)
        self.user_name_label = tk.Label(self.user_frame, text=self.user.name)
        self.user_name_label.grid(column=0, row=0)
        self.user_chip_label = tk.Label(
            self.user_frame, text="Your Chips: %s"%self.user.chips
        )
        self.user_chip_label.grid(column=1, row=0)
        self.user_bet_label = tk.Label(
            self.user_frame, text="Current Bet: %s"%self.user.currentBet
        )
        self.user_bet_label.grid(column=2, row=0)
        # Display bet controls
        self.bet_control_frame = tk.Frame(self.table_frame)
        self.bet_control_frame.grid(column=0, row=3)


        self.fold_button = tk.Button(self.bet_control_frame, text="Fold")
        self.fold_button.grid(column=0, row=0)
        self.check_button = tk.Button(self.bet_control_frame, text="Check")
        self.check_button.grid(column=1, row=0)
        self.call_button = tk.Button(self.bet_control_frame, text="Call")
        self.call_button.grid(column=2, row=0)

        self.increase_bet_1 = tk.Button(
            self.bet_control_frame, text="+1",
            command=lambda: self.handleBetChange(1)
        )
        self.increase_bet_1.grid(column=0, row=1)
        self.decrease_bet_1 = tk.Button(
            self.bet_control_frame, text="-1",
            command=lambda: self.handleBetChange(-1)
        )
        self.decrease_bet_1.grid(column=0, row=2)
        self.increase_bet_5 = tk.Button(
            self.bet_control_frame, text="+5",
            command=lambda: self.handleBetChange(5)
        )
        self.increase_bet_5.grid(column=1, row=1)
        self.decrease_bet_5 = tk.Button(
            self.bet_control_frame, text="-5",
            command=lambda: self.handleBetChange(-5)
        )
        self.decrease_bet_5.grid(column=1, row=2)
        self.increase_bet_10 = tk.Button(
            self.bet_control_frame, text="+10",
            command=lambda: self.handleBetChange(10)
        )
        self.increase_bet_10.grid(column=2, row=1)
        self.decrease_bet_10 = tk.Button(
            self.bet_control_frame, text="-10",
            command=lambda: self.handleBetChange(-10)
        )
        self.decrease_bet_10.grid(column=2, row=2)

        self.bet_button = tk.Button(
            self.bet_control_frame, text="Bet:%s"%self.temp_bet,
            command=lambda: self.betHandle()
        )
        self.bet_button.grid(column=0, row=3, columnspan=3)

        # Display user hand at the btoom
        self.user_hand_frame = tk.Frame(self.table_frame)
        self.user_hand_frame.grid(column=0, row=4)
        i=0
        print(self.user.hand)
        for card in self.user.hand.hand:
            img = get_card_image(card)
            card_label = tk.Label(self.user_hand_frame, image=img)
            card_label.image = img
            card_label.grid(column=i, row=0)
            i+=1

    def newRound(self):
        self.winner_frame.destroy()
        self.game.newRound()
        self.game.deal()
        self.tableDisplay()

    def handleBetChange(self, change):
        self.temp_bet += change
        if self.temp_bet < 0:
            self.temp_bet = 0
        self.bet_button["text"] = "Bet: %s"%self.temp_bet

    def handleCall(self):
        pass

    def handleFold(self):
        pass

    def handleCheck(self):
        pass

    def betHandle(self):
        print("Hi Bet: %s"%self.game.hiBet)
        if (self.temp_bet + self.user.currentBet) < self.game.hiBet:
            temp = self.game.hiBet - self.user.currentBet
            messagebox.showwarning(
                "showwarning",
                "Bet is too low to call. Must bet %s or more"%temp
            )
        else:
            #self.user.currentBet += self.temp_bet
            #self.user.chips -= self.temp_bet
            self.game.takeUserGuiBet(self.user, self.temp_bet)
            self.temp_bet = 0
            self.bet_button["text"] = "Bet: %s"%self.temp_bet
            self.user_chip_label["text"] = "Chips: %s"%self.user.chips
            self.user_bet_label["text"] = "Current Bet: %s"%self.user.currentBet
            self.pot_label["text"] = "Current Pot: %s"%self.game.pot
            self.takeBets()

    def userBets(self):
        pass

    def takeBets(self):
        i = 1
        while i < len(self.game.currentPlayers):
            player = self.game.currentPlayers[i-1]
            response = self.game.takeGuiBets(player)
            if response < 0:
                player.bet_label["text"] = "Folds"
                self.game.currentPlayers.pop(i-1)
            else:
                player.bet_label["text"] = "Current Bet: %s"%player.currentBet
                i += 1
            player.chips_label["text"] = "Chips: %s"%player.chips
        if self.user.currentBet == self.game.hiBet:
            self.displayWinner()


    def displayWinner(self):
        self.table_frame.destroy()
        winner = self.game.presentGuiWinner()
        self.winner_frame = tk.Frame(self.game_frame)
        self.winner_frame.pack()
        if isinstance(winner, list):
            pass
        else:
            self.winner_label = tk.Label(
                self.winner_frame, text="%s Wins!"%winner.name
            )
            self.winner_label.grid(column=0, row=0)
            self.winner_hand = tk.Frame(self.winner_frame)
            self.winner_hand.grid(column=0, row=1)
            i = 0
            for card in winner.hand.hand:
                img = get_card_image(card)
                card_label = tk.Label(self.winner_hand, image=img)
                card_label.image = img
                card_label.grid(column=i, row=0)
                i+=1
        self.new_round_button = tk.Button(
            self.winner_frame, text="New Round",
            command=lambda: self.newRound()
        )
        self.new_round_button.grid(column=0, row=10)

    def run(self):
        self.introFrame()
        while True:
            self.update_idletasks()
            self.update()
        #self.mainloop()

def generate_players(number):
    i = 0
    players = []
    while i < number:
        players.append(Player(PLAYER_NAMES[i]))
        i += 1
    return players

if __name__ == "__main__":
    testHand = [
        Card(10),
        Card(30),
        Card(42),
        Card(25),
        Card(14)
    ]
    game = Game()
    game.run()
