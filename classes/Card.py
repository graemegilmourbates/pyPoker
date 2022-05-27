class Card:
    def __init__(self, value):
        if(value<13):
            self.value = value
            self.suite = "Diamonds"
        elif(value<26):
            self.value = value%13
            self.suite = "Hearts"
        elif(value<39):
            self.value = value%13
            self.suite = "Clubs"
        else:
            self.value = value%13
            self.suite = "Spades"
        self.value += 1
        if self.value==1:
            self.value=14
    def __str__(self):
        if(self.value==14):
            card="A"
        elif(self.value==11):
            card="J"
        elif(self.value==12):
            card="Q"
        elif(self.value==13):
            card="K"
        else:
            card=self.value
        return ("%s of %s"% (card, self.suite))
