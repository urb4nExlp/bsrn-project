import random
import os

# Klasse für die Bingo-Karte
class BingoCard:
    # Initialisierung der Bingo-Karte mit Reihen, Spalten und der Wortdatei
    def __init__(self, rows, cols, word_file):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card(word_file)
        self.original_card = [row[:] for row in self.card]  # Kopie der Originalkarte

    # Methode zum Erstellen der Bingo-Karte
    def create_card(self, word_file):
        # Wörter aus der Datei lesen
        words = self.read_words_from_file(word_file)
        if len(words) < self.rows * self.cols - 1:  # Berücksichtigung des Jokerfelds
            raise ValueError("Die Wortdatei enthält nicht genügend Wörter für die Bingo-Karte.")

        card = []
        used_words = set()  # Verwendete Wörter speichern, um Duplikate zu vermeiden

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.rows % 2 != 0 and self.cols % 2 != 0 and i == self.rows // 2 and j == self.cols // 2:
                    row.append('JOKER')  # Mittleres Feld als Joker
                else:
                    word = random.choice(words)
                    while word in used_words:
                        word = random.choice(words)
                    row.append(word)
                    used_words.add(word)
            card.append(row)
        return card

    # Methode zum Lesen von Wörtern aus einer Textdatei
    def read_words_from_file(self, word_file):
        try:
            with open(word_file, 'r', encoding='utf-8') as file:
                words = file.read().split()  # Wörter durch Leerzeichen getrennt einlesen
            return words
        except FileNotFoundError:
            raise FileNotFoundError(f"Die Datei {word_file} wurde nicht gefunden.")
        except Exception as e:
            raise Exception(f"Fehler beim Lesen der Datei {word_file}: {e}")

    # Methode zum Markieren eines korrekten Feldes
    def mark_correct(self, row, col):
        self.card[row - 1][col - 1] = '❎'  # Markieren mit einem grünen Kreuz

    # Methode zum Entfernen der Markierung eines fehlerhaften Feldes
    def unmark_correct(self, row, col):
        if self.card[row - 1][col - 1] != 'JOKER':  # Nur wenn es sich nicht um das Jokerfeld handelt
            self.card[row - 1][col - 1] = self.original_card[row - 1][col - 1]  # Rücksetzen auf das Originalwort

    # Methode zum Überprüfen, ob der Benutzer gewonnen hat
    def check_win(self):
        # Horizontale Überprüfung
        for row in self.card:
            if all(cell == '❎' or cell == 'JOKER' for cell in row) and 'JOKER' not in row:
                return True

        # Vertikale Überprüfung
        for col in range(self.cols):
            col_cells = [self.card[row][col] for row in range(self.rows)]
            if all(cell == '❎' or cell == 'JOKER' for cell in col_cells) and 'JOKER' not in col_cells:
                return True

        # Diagonale Überprüfung (von links oben nach rechts unten)
        diagonal1 = [self.card[i][i] for i in range(min(self.rows, self.cols))]
        if all(cell == '❎' or cell == 'JOKER' for cell in diagonal1) and 'JOKER' not in diagonal1:
            return True

        # Diagonale Überprüfung (von rechts oben nach links unten)
        diagonal2 = [self.card[i][self.cols - i - 1] for i in range(min(self.rows, self.cols))]
        if all(cell == '❎' or cell == 'JOKER' for cell in diagonal2) and 'JOKER' not in diagonal2:
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
        # Pfad zur Textdatei mit den Wörtern eingeben
        word_file = input("Geben Sie den Namen der Textdatei mit den Buzzwörtern ein: ").strip()
        if not os.path.isfile(word_file):
            raise FileNotFoundError(f"Die Datei {word_file} wurde nicht gefunden.")

        # Eingabe der Anzahl der Zeilen und Spalten für die Bingo-Karte
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")

        # Erstellung der Bingo-Karte
        bingo_card = BingoCard(rows, cols, word_file)
        print("Hier ist Ihre Bingo-Karte:")
        print(bingo_card)

        # Spielschleife
        while True:
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

            # Überprüfung, ob die Eingaben innerhalb des gültigen Bereichs liegen
            if row < 1 or row > rows or col < 1 or col > cols:
                print("Ungültige Zeilen- oder Spaltennummer. Bitte erneut eingeben.")
                continue

            # Markierung oder Rücksetzung des ausgewählten Elements
            if action == 'mark':
                bingo_card.mark_correct(row, col)
                print("Element ({}, {}) wurde als korrekt markiert.".format(row, col))
            elif action == 'unmark':
                bingo_card.unmark_correct(row, col)
                print("Markierung des Elements ({}, {}) wurde entfernt.".format(row, col))

            print(bingo_card)

            # Überprüfung, ob der Benutzer gewonnen hat
            if bingo_card.check_win():
                print("Herzlichen Glückwunsch, Sie haben gewonnen!")
                display_winner_design()  # Gewinner-Design anzeigen
                break

    except ValueError as e:
        # Fehlerbehandlung für ungültige Eingaben
        print("Fehler:", e)
    except FileNotFoundError as e:
        # Fehlerbehandlung für fehlende Datei
        print("Fehler:", e)
    except Exception as e:
        # Allgemeine Fehlerbehandlung
        print("Ein unerwarteter Fehler ist aufgetreten:", e)


# Überprüfung, ob das Skript direkt ausgeführt wird
if __name__ == "__main__":
    main()

