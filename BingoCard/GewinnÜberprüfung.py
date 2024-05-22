import random

class BingoCard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card()

    def create_card(self):
        # Erstelle eine leere Bingo-Karte
        card = []
        # Liste von Wörtern für die Bingo-Karte
        words = ["Apple", "Banana", "Cat", "Dog", "Elephant", "Fish"]
        # Fülle die Karte mit zufälligen Wörtern
        for _ in range(self.rows):
            column = random.sample(words, self.cols)
            card.append(column)
        return card

    def mark_correct(self):
        try:
            while True:
                # Benutzer eingabe für die Zeilennummer
                row = int(input("Geben Sie die Zeilennummer des korrekten Elements ein (1 bis {}), oder geben Sie 0 ein, um zu beenden: ".format(self.rows)))
                if row == 0:
                    break

                # Benutzer eingabe für die Spaltennummer
                col = int(input("Geben Sie die Spaltennummer des korrekten Elements ein (1 bis {}): ".format(self.cols)))

                # Überprüfen, ob die eingegebenen Werte innerhalb des gültigen Bereichs liegen
                if row < 1 or row > self.rows or col < 1 or col > self.cols:
                    raise ValueError("Ungültige Zeilen- oder Spaltennummer.")

                # Das Element auf der Bingo-Karte als korrekt markieren
                self.card[row - 1][col - 1] = '✔️'  # Verwenden Sie ein anderes Symbol, um ein korrektes Feld zu markieren

                # Bestätigungsmeldung für den Benutzer
                print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
                # Die aktualisierte Bingo-Karte ausgeben
                print(self)

                # Überprüfe, ob der Benutzer gewonnen hat
                if self.check_win():
                    print("Herzlichen Glückwunsch, Sie haben gewonnen!")
                    return

        except ValueError as e:
            # Fehlerbehandlung für ungültige Eingaben
            print("Fehler:", e)

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

    def __str__(self):
        # Erstelle eine Zeichenfolge, um die Bingo-Karte anzuzeigen
        card_str = ""
        for row in self.card:
            # Füge jede Zeile der Bingo-Karte der Zeichenfolge hinzu
            card_str += " ".join(f"{cell:8}" for cell in row) + "\n"
        return card_str

def main():
    try:
        # Benutzereingabe für die Anzahl der Zeilen und Spalten der Bingo-Karte
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")

        # Erstelle eine Bingo-Karte
        bingo_card = BingoCard(rows, cols)
        print("Hier ist Ihre Bingo-Karte:")
        print(bingo_card)

        # Markiere korrekte Felder, bis der Benutzer gewinnt oder das Spiel beendet
        bingo_card.mark_correct()

    except ValueError as e:
        # Fehlerbehandlung für ungültige Eingaben
        print("Fehler:", e)

if __name__ == "__main__":
    main()