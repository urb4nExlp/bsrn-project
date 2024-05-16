import random
from docx import Document
import os
#Hinweis: man braucht das package python-docx
#Hinweis: die worddatei muss in gleichen Ordner sein wie die Pythondatei soweit ich weiß

class BingoCard:
    def __init__(self, rows, cols, word_file):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card(word_file)

    def create_card(self, word_file):
        # Lese Wörter aus der Word-Datei
        words = self.read_words_from_file(word_file)

        # Erstelle eine leere Bingo-Karte
        card = []

        # Fülle die Karte mit zufälligen Wörtern
        for _ in range(self.rows):
            column = random.sample(words, self.cols)
            card.append(column)
        return card

    def read_words_from_file(self, word_file):
        doc = Document(word_file)
        words = []
        for paragraph in doc.paragraphs:
            words.extend(paragraph.text.split())
        return words

    # Markiere das angegebene Feld als korrekt
    def mark_correct(self, row, col):
        self.card[row - 1][col - 1] = '✔️'

    # Überprüfe, ob der Benutzer gewonnen hat
    def check_win(self):
        # Horizontal überprüfen
        for row in self.card:
            if all(cell == '✔️' for cell in row):
                return True

        # Vertikal überprüfen
        for col in range(self.cols):
            if all(self.card[row][col] == '✔️' for row in range(self.rows)):
                return True

        # Diagonal überprüfen (von links oben nach rechts unten)
        if all(self.card[i][i] == '✔️' for i in range(min(self.rows, self.cols))):
            return True

        # Diagonal überprüfen (von rechts oben nach links unten)
        if all(self.card[i][self.cols - i - 1] == '✔️' for i in range(min(self.rows, self.cols))):
            return True

        return False

    # Methode zur Darstellung der Bingo-Karte
    def __str__(self):
        card_str = ""
        for row in self.card:
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        return card_str

def main():
    try:
        # Benutzereingabe für die Anzahl der Zeilen und Spalten der Bingo-Karte
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")

        # Öffne die Word-Datei im Programmverzeichnis
        word_file = os.path.join(os.path.dirname(__file__), "buzzwörter.docx")

        # Erstelle eine Bingo-Karte
        bingo_card = BingoCard(rows, cols, word_file)
        print("Hier ist Ihre Bingo-Karte:")
        print(bingo_card)

        # Spielschleife
        while True:
            row = int(input("Geben Sie die Zeilennummer des korrekten Elements ein (1 bis {}), oder geben Sie 0 ein, um zu beenden: ".format(rows)))
            if row == 0:
                break

            col = int(input("Geben Sie die Spaltennummer des korrekten Elements ein (1 bis {}): ".format(cols)))

            # Überprüfen, ob die eingegebenen Werte innerhalb des gültigen Bereichs liegen
            if row < 1 or row > rows or col < 1 or col > cols:
                raise ValueError("Ungültige Zeilen- oder Spaltennummer.")

            # Das Element auf der Bingo-Karte als korrekt markieren
            bingo_card.mark_correct(row, col)
            print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
            print(bingo_card)

            # Überprüfen, ob der Benutzer gewonnen hat
            if bingo_card.check_win():
                print("Herzlichen Glückwunsch, Sie haben gewonnen!")
                break

    except ValueError as e:
        # Fehlerbehandlung für ungültige Eingaben
        print("Fehler:", e)

if __name__ == "__main__":
    main()