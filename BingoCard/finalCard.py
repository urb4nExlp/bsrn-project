import random
import curses
from curses import textpad
import os


class BingoCard:

    def __init__(self, rows, cols, word_file):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card(word_file)
        self.original_card = [row[:] for row in self.card]  # Kopie der Originalkarte um später die Klicks auch rückgänig machen zu können
    def read_words_final(file_path):
        #datei wird geöffnet und gelesen durch 'r', codiert in utf-8
        with open(file_path, 'r', encoding='utf-8') as file:
        #list words spechert die Wörter, iteriert über jede Zeile
        words = [line.strip() for line in file]
        return words

    def create_card_jr(self, word_file):
        try:
            # Wörter aus der Datei lesen
            words = self.read_words_from_file(word_file)
        except FileNotFoundError:
            print("Es gab einen Fehler mit dem Dateipfad.")
            choice = input("Möchten Sie zufällige Wörter verwenden (1) oder das Spiel abbrechen und die Datei korrigieren (2)? ")
            if choice == '1':
                use_random_words = True
            elif choice == '2':
                print("Das Spiel wird abgebrochen. Bitte prüfen Sie den Dateipfad und korrigieren Sie die Datei, um das Spiel erneut zu starten.")
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

        card = []
        used_words = set()  # Verwendete Wörter speichern, um Duplikate zu vermeiden

        # Zufällige Wörter in die Karte einfügen
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.rows % 2 != 0 and self.cols % 2 != 0 and i == self.rows // 2 and j == self.cols // 2:
                    row.append('❎')  # Mittleres Feld als Joker
                else:
                    word = random.choice(words)
                    while word in used_words:
                        word = random.choice(words)
                    row.append(word)
                    used_words.add(word)
            card.append(row)
        return card

    def create_bingo_card_m(words, xaxis, yaxis):
        random.shuffle(words)
        return [words[i*yaxis:(i+1)*yaxis] for i in range(xaxis)]

    def check_bingo_jr(self):
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


    def check_win_jr(self):
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

    def draw_card_m(stdscr, card, marked, xaxis, yaxis, field_width, field_height):
        stdscr.clear()
        for i, row in enumerate(card):
            for j, word in enumerate(row):
                x1, y1 = 2 + j * (field_width + 1), 2 + i * (field_height + 1)
                x2, y2 = x1 + field_width, y1 + field_height
                textpad.rectangle(stdscr, y1, x1, y2, x2)  # Zeichnet eine Umrandung um jedes Feld
                if (i, j) in marked:
                    stdscr.addstr(y1 + field_height // 2, x1 + 1, "X".center(field_width - 1),
                                  curses.A_REVERSE)  # Wenn markiert, dann 'X'
                else:
                    stdscr.addstr(y1 + field_height // 2, x1 + 1, word.center(field_width - 1))  # Andernfalls das Wort
        stdscr.refresh()

    def check_bingo_m(marked, xaxis, yaxis):
        # Überprüft Reihen
        for i in range(xaxis):
            if all((i, j) in marked for j in range(yaxis)):
                return True
        # Überprüft Spalten
        for j in range(yaxis):
            if all((i, j) in marked for i in range(xaxis)):
                return True
        # Überprüft Diagonalen
        if all((i, i) in marked for i in range(xaxis)):
            return True
        if all((i, yaxis - 1 - i) in marked for i in range(xaxis)):
            return True
        return False

    #main Marvin
    def main(stdscr, xaxis, yaxis, words):
        card = create_bingo_card(words, xaxis, yaxis)
        marked = set()

        # Automatisches Markieren des mittleren Feldes, wenn xaxis und yaxis gleich und ungerade sind
        if xaxis == yaxis and xaxis % 2 == 1:
            middle = xaxis // 2
            marked.add((middle, middle))

        # Berechnen der Feldgröße basierend auf der Länge des längsten Wortes
        longest_word_length = max(len(word) for word in words)
        field_width = longest_word_length + 2  # Platz für das Wort und die Ränder
        field_height = 3  # Höhe des Feldes

        # Folgende Zeilen stellen sicher, dass Mausereignisse von curses erkannt werden:
        curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
        curses.curs_set(0)

        draw_card(stdscr, card, marked, xaxis, yaxis, field_width, field_height)

        while True:
            key = stdscr.getch()
            if key == ord('x'):
                break
            # Klick ist ein Mausereignis
            if key == curses.KEY_MOUSE:  # Überprüft, ob das Ereignis key ein Mausereignis ist
                _, mx, my, _, _ = curses.getmouse()  # Mausposition wird abgerufen
                col = (mx - 2) // (field_width + 1)
                row = (my - 2) // (field_height + 1)
                if 0 <= row < xaxis and 0 <= col < yaxis:
                    if (row, col) in marked:
                        marked.remove((row, col))
                    else:
                        marked.add((row, col))
                    draw_card(stdscr, card, marked, xaxis, yaxis, field_width, field_height)
                    if check_bingo(marked, xaxis, yaxis):
                        stdscr.addstr(2 + xaxis * (field_height + 1), 2,
                                      "BINGO! Du hast gewonnen!".center((field_width + 1) * yaxis))
                        stdscr.refresh()
                        stdscr.getch()
                        break

    def mark_jr(self, row, col):
        self.card[row - 1][col - 1] = '❎'  # Markieren mit einem grünen Kreuz

    def unmark_jr(self, row, col):
        if self.card[row - 1][col - 1] != '❎':  # Nur wenn es sich nicht um das Jokerfeld handelt
            self.card[row - 1][col - 1] = self.original_card[row - 1][col - 1]  # Rücksetzen auf das Originalwort

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

    #main Jamie Robin
    def main_():
        try:
            # Eingabe der Anzahl der Zeilen und Spalten für die Bingo-Karte
            rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
            cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
            # Überprüfen dass die Anzahl größer als Null ist
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


    def __str__(self):
        card_str = ""
        for row in self.card:
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        return card_str


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bingo-Spiel")
    parser.add_argument('-xaxis', type=int, default=5, help='Anzahl der Felder in der Breite')
    parser.add_argument('-yaxis', type=int, default=5, help='Anzahl der Felder in der Höhe')
    parser.add_argument('-wordfile', type=str, default='wordfile.txt', help='Pfad zur Datei mit den Wörtern')
    args = parser.parse_args()

    words = load_words(args.wordfile)
    if len(words) < args.xaxis * args.yaxis:
        raise ValueError("Nicht genügend Wörter in der Datei, um die Bingo-Karte zu füllen.")

    curses.wrapper(main, args.xaxis, args.yaxis, words)
