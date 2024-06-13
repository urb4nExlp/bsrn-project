#kleiner Bingo Code zum Herumspielen
import random

class Bingo:
    #Konstruktor immer mit __init__
    def __init__(self, players):
        self.players = players
        self.cards = {player: self.generate_card() for player in players}
        self.called_numbers = set()

    #generieren von ausgefüllten Matrizen für jeden Spieler
    def generate_card(self):
        card = []
        for _ in range(5):
            row = random.sample(range(1, 11), 5)
            card.append(row)
        return card

    #Funktion zur Ausgabe durch for-Schleife in MAtrix card
    def display_card(self, player):
        print(f"\nBingo card for Player {player}:")
        card = self.cards[player]
        for row in card:
            print(row)

    #Zufällige Zahl wird ausgerufen
    def call_number(self):
        number = random.randint(1, 10)
        self.called_numbers.add(number)
        print(f"\nCalled number: {number}")

    #Spieler checken mit Schleife, ob Zahl in MAtrix vorkommt
    def check_card(self, player):
        card = self.cards[player]
        for row in card:
            if all(num in self.called_numbers for num in row):
                return True
        return False

    #"Hauptmethode": Spiel wird gespielt und Gewinner ausgemacht
    def play(self):
        while True:
            self.call_number()
            for player in self.players:
                self.display_card(player)
                if self.check_card(player):
                    print(f"\nPlayer {player} wins!")
                    return

# Beispiel: Spiel mit zwei Spielern
players = ["Robal", "Bemie"]
bingo_game = Bingo(players)
bingo_game.play()



def createlog (spielername):
    ############
    #erstelle log mit spielername und dem aktuellen datum + zeit
    ############

def addlog (bezeichnung)
    ############
    #Füge eine Zeile mit Datum Zeit tag etc + bezeichnung zur logfile hinzu
    ############

def create_roundfile(rundendatei, xachse, yachse, maxspieler):
    #hier soll eine datei erzeugt werden (Schema der Datei hab ich dir geschickt)

def getrundendatei():
    #return STRING der rundendatei

def getxachse(rundendatei):
    #return INT DER X ACHSE

def getyachse(rundendatei):
    #return INT DER Y ACHSE

def getspielerzahl(rundendatei):
    #return INT MAXPALYER