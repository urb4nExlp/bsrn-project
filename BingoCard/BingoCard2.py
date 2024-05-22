import random
import os

# Klasse für die Bingo-Karte
class BingoCard:
    # Initialisierung der Bingo-Karte mit Reihen, Spalten und der Wortdatei
    def __init__(self, rows, cols, word_file):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card(word_file)

    # Methode zum Erstellen der Bingo-Karte
    def create_card(self, word_file):
        try:
            # Wörter aus der Datei lesen
            words = self.read_words_from_file(word_file)
        except FileNotFoundError:
            print("Es gab einen Fehler mit dem Dateipfad. Das Spiel kann nicht gestartet werden. Bitte prüfen Sie ob der angegebene Dateipfad richtig ist.")
            return None

        card = []
        used_words = set()  # Verwendete Wörter speichern, um Duplikate zu vermeiden

        # Zufällige Wörter in die Karte einfügen
        for _ in range(self.rows):
            row = []
            while len(row) < self.cols:
                word = random.choice(words)
                if word not in used_words:
                    row.append(word)
                    used_words.add(word)
            card.append(row)
        return card

    # Methode zum Lesen von Wörtern aus einer Textdatei
    def read_words_from_file(self, word_file):
        with open(word_file, 'r', encoding='utf-8') as file:
            words = file.read().split()  # Wörter durch Leerzeichen getrennt einlesen
        return words

    # Methode zum Markieren eines korrekten Feldes
    def mark_correct(self, row, col):
        self.card[row - 1][col - 1] = '❎'  # Markieren mit einem grünen Kreuz

    # Methode zum Überprüfen, ob der Benutzer gewonnen hat
    def check_win(self):
        # Horizontale Überprüfung
        for row in self.card:
            if all(cell == '❎' for cell in row):
                return True

        # Vertikale Überprüfung
        for col in range(self.cols):
            if all(self.card[row][col] == '❎' for row in range(self.rows)):
                return True

        # Diagonale Überprüfung (von links oben nach rechts unten)
        if all(self.card[i][i] == '❎' for i in range(min(self.rows, self.cols))):
            return True

        # Diagonale Überprüfung (von rechts oben nach links unten)
        if all(self.card[i][self.cols - i - 1] == '❎' for i in range(min(self.rows, self.cols))):
            return True

        return False

    # Methode zur Darstellung der Bingo-Karte
    def __str__(self):
        card_str = ""
        for row in self.card:
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        return card_str


# Funktion zur Anzeige eines Gewinner-Designs
def display_winner_design():
    design = """
__     ______  _    _   __          _______ _   _ 
\ \   / / __ \| |  | |  \ \        / /_   _| \ | |
 \ \_/ / |  | | |  | |   \ \  /\  / /  | | |  \| |
  \   /| |  | | |  | |    \ \/  \/ /   | | | . ` |
   | | | |__| | |__| |     \  /\  /   _| |_| |\  |
   |_|  \____/ \____/       \/  \/   |_____|_| \_|

"""
    print(design)


# Hauptfunktion des Programms
def main():
    try:
        # Eingabe der Anzahl der Zeilen und Spalten für die Bingo-Karte
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")

        # Pfad zur Textdatei mit den Wörtern
        word_file = os.path.join(os.path.dirname(__file__), "buzzwoeter.txt")

        # Erstellung der Bingo-Karte
        bingo_card = BingoCard(rows, cols, word_file)
        if bingo_card.card is None:
            return  # Beende das Spiel, wenn die Karte nicht erstellt werden konnte

        print("Hier ist Ihre Bingo-Karte:")
        print(bingo_card)

        # Spielschleife
        while True:
            row = int(input(
                "Geben Sie die Zeilennummer des korrekten Elements ein (1 bis {}), oder geben Sie 0 ein, um zu beenden: ".format(
                    rows)))
            if row == 0:
                print("Spiel beendet.")
                break

            col = int(input("Geben Sie die Spaltennummer des korrekten Elements ein (1 bis {}): ".format(cols)))

            # Überprüfung, ob die Eingaben innerhalb des gültigen Bereichs liegen
            if row < 1 or row > rows or col < 1 or col > cols:
                print("Ungültige Zeilen- oder Spaltennummer. Bitte erneut eingeben.")
                continue

            # Markierung des ausgewählten Elements
            bingo_card.mark_correct(row, col)
            print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
            print(bingo_card)

            # Überprüfung, ob der Benutzer gewonnen hat
            if bingo_card.check_win():
                print("Herzlichen Glückwunsch, Sie haben gewonnen!")
                display_winner_design()  # Gewinner-Design anzeigen
                break

    except ValueError as e:
        # Fehlerbehandlung für ungültige Eingaben
        print("Fehler:", e)


# Überprüfung, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()


