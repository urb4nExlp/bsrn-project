import random
import os

# Klasse für die Bingo-Karte
class BingoCard:
    # Initialisierung der Bingo-Karte mit Reihen, Spalten und der Wortdatei
    def __init__(self, rows, cols, word_file):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card(word_file)
<<<<<<< HEAD
        self.original_card = [row[:] for row in self.card]  # Kopie der Originalkarte um später die Klicks auch rückgänig machen zu können

=======

    # Methode zum Erstellen der Bingo-Karte
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
    def create_card(self, word_file):
        try:
            # Wörter aus der Datei lesen
            words = self.read_words_from_file(word_file)
<<<<<<< HEAD
        except FileNotFoundError:
            print("Es gab einen Fehler mit dem Dateipfad.")
            choice = input(
                "Möchten Sie zufällige Wörter verwenden (1) oder das Spiel abbrechen und die Datei korrigieren (2)? ")
            if choice == '1':
                use_random_words = True
            elif choice == '2':
                print(
                    "Das Spiel wird abgebrochen. Bitte prüfen Sie den Dateipfad und korrigieren Sie die Datei, um das Spiel erneut zu starten.")
                return None
            else:
                print(
                    "Ungültige Eingabe. Bitte wählen Sie '1' für zufällige Wörter oder '2', um das Spiel abzubrechen.")
                return None

        if use_random_words:
            # Hier könnten wir Code einfügen, um zufällige Wörter zu generieren
            pass
        else:
            if len(words) < self.rows * self.cols - 1:  # Berücksichtigung des Jokerfelds
                raise ValueError("Die Wortdatei enthält nicht genügend Wörter für die Bingo-Karte.")
=======
            #Exception falls der Dateipfad nicht gefunden wird
        except FileNotFoundError:
            print("Es gab einen Fehler mit dem Dateipfad. Das Spiel kann nicht gestartet werden. Bitte prüfen Sie ob der angegebene Dateipfad richtig ist.")
            return None
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d

        card = []
        used_words = set()  # Verwendete Wörter speichern, um Duplikate zu vermeiden

        # Zufällige Wörter in die Karte einfügen
<<<<<<< HEAD
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.rows % 2 != 0 and self.cols % 2 != 0 and i == self.rows // 2 and j == self.cols // 2:
                    row.append('❎')  # Mittleres Feld als Joker
                else:
                    word = random.choice(words)
                    while word in used_words:
                        word = random.choice(words)
=======
        for _ in range(self.rows):
            row = []
            while len(row) < self.cols:
                word = random.choice(words)
                if word not in used_words:
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
                    row.append(word)
                    used_words.add(word)
            card.append(row)
        return card

    # Methode zum Lesen von Wörtern aus einer Textdatei
    def read_words_from_file(self, word_file):
<<<<<<< HEAD
        # 'r'= Lesemodus, encoding='utf-8' = stellt sicher dass die Datei als UTF-8 Coidert wird(gut für Behandlung Sonderzeichen)
=======
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
        with open(word_file, 'r', encoding='utf-8') as file:
            words = file.read().split()  # Wörter durch Leerzeichen getrennt einlesen
        return words

    # Methode zum Markieren eines korrekten Feldes mit einem grünen Kreuz(Symbolisiert dass es abgehakt ist)
<<<<<<< HEAD
    def mark(self, row, col):
        self.card[row - 1][col - 1] = '❎'  # Markieren mit einem grünen Kreuz

    def unmark(self, row, col):
        if self.card[row - 1][col - 1] != '❎':  # Nur wenn es sich nicht um das Jokerfeld handelt
            self.card[row - 1][col - 1] = self.original_card[row - 1][col - 1]  # Rücksetzen auf das Originalwort

=======
    def mark_correct(self, row, col):
        self.card[row - 1][col - 1] = '❎'  # Markieren mit einem grünen Kreuz

>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
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
<<<<<<< HEAD
    #Hier vermutlich mit den Bibliotheken arbeiten
=======
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
    def __str__(self):
        card_str = ""
        for row in self.card:
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        return card_str


# Funktion zur Anzeige eines Gewinner-Designs
<<<<<<< HEAD
#Eventuell auch mit Bibliotek schöner machen
=======
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
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


# Hauptfunktion des Programms (Die Main-Funktion)
def main():
    try:
        # Eingabe der Anzahl der Zeilen und Spalten für die Bingo-Karte
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        #Überprüfen dass die Anzahl größer als Null ist
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
<<<<<<< HEAD
            action = input(
                "Geben Sie 'mark' ein, um ein Feld zu markieren, 'unmark', um die Markierung eines Feldes zu entfernen, oder '0', um zu beenden: ").strip().lower()
            if action == '0':
                print("Spiel beendet.")
                break

            if action not in ['mark', 'unmark']:
                print("Ungültige Aktion. Bitte 'mark', 'unmark' oder '0' eingeben.")
                continue

            row = int(input("Geben Sie die Zeilennummer des Elements ein (1 bis {}): ".format(rows)))
            col = int(input("Geben Sie die Spaltennummer des Elements ein (1 bis {}): ".format(cols)))
=======
            row = int(input(
                "Geben Sie die Zeilennummer des korrekten Elements ein (1 bis {}), oder geben Sie 0 ein, um zu beenden: ".format(
                    rows)))
            if row == 0:
                print("Spiel beendet.")
                break

            col = int(input("Geben Sie die Spaltennummer des korrekten Elements ein (1 bis {}): ".format(cols)))
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d

            # Überprüfung, ob die Eingaben innerhalb des gültigen Bereichs liegen
            if row < 1 or row > rows or col < 1 or col > cols:
                print("Ungültige Zeilen- oder Spaltennummer. Bitte erneut eingeben.")
                continue

<<<<<<< HEAD
            # Markierung oder Rücksetzung des ausgewählten Elements
            if action == 'mark':
                bingo_card.mark_correct(row, col)
                print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
            elif action == 'unmark':
                bingo_card.unmark_correct(row, col)
                print("Markierung des Elements ({}, {}) wurde entfernt.".format(row, col))

=======
            # Markierung des ausgewählten Elements
            bingo_card.mark_correct(row, col)
            print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
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
<<<<<<< HEAD
    main()
=======
    main()


>>>>>>> fb1f0f3bcd3d328c8374e281fb812ce66dced97d
