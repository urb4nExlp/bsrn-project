import random
import curses
from curses import textpad

# random um Wörter auszusuchen, curses um textbasierte Benutzeroberfläche in der Kommandozeile zu erzeugen

# Einlesen der Wörter aus der Wordfile, Dateipfad muss als Parameter übergeben werden
# Wörter als Liste gespeichert
#Schlüüselwort def für Funktion, Funktionsbezeichnung read_words
def read_words(file_path):
    #datei wird geöffnet und gelesen durch 'r', codiert in utf-8
    with open(file_path, 'r', encoding='utf-8') as file:
        #list words spechert die Wörter, iteriert über jede Zeile
        words = [line.strip() for line in file]
    return words
#hier Exception noch einbauen

# Basierend auf den übergebenen Dimensionen wird die Bingokarte als Liste in einer Liste erstellt
# Wörter werden gemischelt und in die Listen befüllt
def create_bingo_card(words, xaxis, yaxis):
    random.shuffle(words)
    return [words[i*yaxis:(i+1)*yaxis] for i in range(xaxis)]

# Karte wird auf dem Bildschirm gezeichnet.
# Bedingung: Wenn markiert, dann 'X'
def draw_card(stdscr, card, marked, xaxis, yaxis, field_width, field_height):
    stdscr.clear()
    for i, row in enumerate(card):
        for j, word in enumerate(row):
            x1, y1 = 2 + j * (field_width + 1), 2 + i * (field_height + 1)
            x2, y2 = x1 + field_width, y1 + field_height
            textpad.rectangle(stdscr, y1, x1, y2, x2)  # Zeichnet eine Umrandung um jedes Feld
            if (i, j) in marked:
                stdscr.addstr(y1 + field_height // 2, x1 + 1, "X".center(field_width - 1), curses.A_REVERSE)  # Wenn markiert, dann 'X'
            else:
                stdscr.addstr(y1 + field_height // 2, x1 + 1, word.center(field_width - 1))  # Andernfalls das Wort
    stdscr.refresh()

# Schleifen, um zu checken, ob die Bingo-Bedingung erfüllt ist
def check_bingo(marked, xaxis, yaxis):
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

# Main-Methode, Bingo-Karte wird erstellt und gezeichnet
# Regelt das Klicken mit der Maus
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
                    stdscr.addstr(2 + xaxis * (field_height + 1), 2, "BINGO! Du hast gewonnen!".center((field_width + 1) * yaxis))
                    stdscr.refresh()
                    stdscr.getch()
                    break

# Startet das Hauptprogramm in der Curses-Umgebung, lädt Wörter aus der Datei
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
