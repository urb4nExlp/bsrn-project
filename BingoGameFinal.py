import sys
import posix_ipc
import time
import os
import signal
import random
from functools import partial
import curses
from curses import textpad
import argparse
import datetime


# Erstellt einen Log-Dateinamen basierend auf dem aktuellen Zeitstempel und dem Spielernamen.
def create_log_file(player_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-bingo-{player_name}.txt"
    return filename


# Loggt ein Ereignis mit einem Zeitstempel in die angegebene Datei.
def log_event(filename, event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(filename, 'a') as file:
        file.write(f"{timestamp} {event}\n")


def getxachse(rundendatei):  # Liest die X-Achsenbreite aus der  Roundfile, die mit 'width:' beginnt. Rückgabewert = INT
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("width:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading x-axis from {rundendatei}: {e}")
        return None


def getyachse(rundendatei):  # Liest die Y-Achsenbreite aus der Roundfile, die mit 'width:' beginnt. Rückgabewert = INT
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("height:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading y-axis from {rundendatei}: {e}")
        return None


def get_pid_host(rundendatei):  # Attribute werden übernommen
    try:
        with open(rundendatei, 'r') as f:  # rundendatei wird im Lesemodus geöffnet
            for line in f:  # rundendatei wird durchlaufen
                if line.startswith("playername1:"):  # Überprüfen, ob die Zeile mit "playername1:" beginnt
                    parts = line.split(":")
                    if len(parts) == 3:
                        return int(parts[2].strip())  # Die PID extrahieren und als Integer zurückgeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Error reading PID from {rundendatei}: {e}")  # Fehlermeldung
        return None


def incplayer(rundendatei, spielername):
    try:
        player_count = None  # Initialisiere player_count mit None

        # Öffne die Datei im Lesemodus und lies alle Zeilen
        with open(rundendatei, 'r') as f:
            lines = f.readlines()

        # Durchlaufe die Zeilen und finde die Zeile mit 'players:'
        for i, line in enumerate(lines):
            if line.startswith("players:"):
                # Extrahiere die aktuelle Anzahl von Spielern und erhöhe sie um 1
                player_count = int(line.split(":")[1].strip())
                player_count += 1
                lines[i] = f"players: {player_count}\n"  # Aktualisiere die Zeile mit der neuen Spieleranzahl
                break  # Beende die Schleife, da wir die Zeile gefunden und aktualisiert haben

        # Falls keine Zeile mit 'players:' gefunden wurde, wird eine ValueError ausgelöst
        if player_count is None:
            raise ValueError("No 'players:' line found in the file.")

        # Erzeuge den neuen Spielerstring
        playerstring = "playername" + str(player_count)
        new_line = f"{playerstring}: {spielername}: {os.getpid()}\n"

        # Füge den neuen Spielerstring eine Zeile vor der aktualisierten 'players:'-Zeile ein
        lines.insert(i, new_line)

        # Öffne die Datei im Schreibmodus und schreibe die aktualisierten Zeilen zurück
        with open(rundendatei, 'w') as f:
            f.writelines(lines)

        # Gib die aktuelle Anzahl von Spielern zurück
        return player_count

    except Exception as e:
        # Falls ein Fehler auftritt, gebe eine Fehlermeldung aus und gib None zurück
        print(f"Error updating players in {rundendatei}: {e}")
        return None


def decrease_players(rundendatei):
    try:
        with open(rundendatei, 'r') as f:
            lines = f.readlines()

        with open(rundendatei, 'w') as f:
            for line in lines:
                if line.startswith("players:"):
                    current_players = int(line.split(":")[1].strip())
                    if current_players > 1:
                        new_players = current_players - 1
                        f.write(f"players: {new_players}\n")
                        continue  # Skip writing the original line
                    else:
                        f.write(line)  # Write the original line
                        return True
                else:
                    f.write(line)  # Write the original line

        return False

    except Exception as e:
        print(f"Error processing file {rundendatei}: {e}")
        return False


def check_gameover(rundendatei):
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("gameover:"):
                    return int(line.split(":")[1].strip()) == 1
    except Exception as e:
        print(f"Error reading gameover from {rundendatei}: {e}")
        return False


def set_gameover(rundendatei):
    try:
        lines = []
        with open(rundendatei, 'r') as f:
            lines = f.readlines()

        with open(rundendatei, 'w') as f:
            for line in lines:
                if line.startswith("gameover:"):
                    f.write("gameover: 1\n")
                else:
                    f.write(line)

        return True
    except Exception as e:
        print(f"Error setting gameover in {rundendatei}: {e}")
        return False


def create_roundfile(rundendatei, xachse, yachse, maxspieler, hostname, wordfile):
    try:
        with open(rundendatei, 'w') as f:
            f.write(f"maxplayer: {maxspieler}\n")
            f.write(f"gameover: {0}\n")
            f.write(f"wordfile: {wordfile}\n")
            f.write(f"height: {yachse}\n")
            f.write(f"width: {xachse}\n")
            f.write(f"playername1: {hostname}: {os.getpid()}\n")
            f.write(f"players: {1}\n")

        print("Roundfile created, initializing game start...")
    except Exception as e:
        print("Error creating round file:", e)


def read_roundfile(roundfile):
    players_data = []
    try:
        with open(roundfile, 'r') as f:
            for line in f:
                if line.startswith("playername"):
                    players_data.append(line.strip())
    except Exception as e:
        print(f"Error reading {roundfile}: {e}")
    return players_data


def draw_players_info(stdscr, players_data, color_pair):  # Attribute werden übernommen
    max_y, max_x = stdscr.getmaxyx()  # größe des Fensters wird ermittelt
    y_position = 1  # startposition der zu zeichnend Informationen
    stdscr.addstr(y_position, 2, "TEILNEHMER:",
                  color_pair)  # "TEILNEHMER" wird an Position (1,2) geschrieben in passender Farbe
    y_position += 1  # vertikale Position wird um eins erhöht, um die nächste Zeile vorzubereiten
    for player_info in players_data:  # Schleife geht durch jede Spielerinformation in der Liste players_data
        stdscr.addstr(y_position, 2, player_info, color_pair)  # Spielerinformation wird an aktueller Stelle ausgegeben
        y_position += 1  # Y-Position wird nach jedem Eintrag um eins erhöht, um die nächste Zeile vorzubereiten
    stdscr.refresh()  # Ausgaben werden angezeigt und aktuallisiert


# JAMIE
class BingoCard:
    def __init__(self, rows, cols, words, log_filename):  #Konstruktur der Klasse BingoCard
        self.rows = rows
        self.cols = cols
        self.log_filename = log_filename
        self.card = self.create_card(words)
        self.original_card = [row[:] for row in self.card]
        self.button_selected = False
        self.bingo_finish = False

    def create_card(self, words):   #Erstellung der BingoCard
        card = []                   #initialisert eine leere Liste wird welche später die Karte darstellen soll
        used_words = set()          #Wird erstellt für die Überprüfung, dass kein Wort doppelt vorkommt

        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                if self.rows % 2 != 0 and self.cols % 2 != 0 and i == self.rows // 2 and j == self.cols // 2: #Überprüfung ob man einen Joker für das mittlere Feld braucht
                    row.append('X')
                else:
                    word = random.choice(words)          #Random Wörter werden in die BingoCard eingetragen
                    while word in used_words:            #überprüfung ob das Wort schon in used_Words ist
                        word = random.choice(words)
                    row.append(word)
                    used_words.add(word)                 #Benutze Wort kommt in die Liste used-Words damit es nicht nochmal vorkommen kann
            card.append(row)
        return card



    def check_bingo(self):                               #Methode zur Überprüfung ob ein Bingo vorhanden ist
        for row in self.card:                            #Überprüfung der Reihen nach Bingo
            if all(cell == 'X' for cell in row):
                self.bingo_finish = True
                return True

        for col in range(self.cols):                     #Überprüfung der Spalten nach Bingo
            if all(self.card[row][col] == 'X' for row in range(self.rows)):
                self.bingo_finish = True
                return True

        if all(self.card[i][i] == 'X' for i in range(min(self.rows, self.cols))):  #Überprüfung Diagtonal von links oben nach rechts unten nach Bingo
            self.bingo_finish = True
            return True

        if all(self.card[i][self.cols - i - 1] == 'X' for i in range(min(self.rows, self.cols))):        #Überprüfung Diagtonal von rechts oben nach links unten nach Bingo
            self.bingo_finish = True
            return True

        return False

    def mark(self, row, col):      #Methode zum Markieren der Felder
        self.card[row][col] = 'X'
        log_event(self.log_filename, f"Marked {self.original_card[row][col]} ({row}/{col})")

    def unmark(self, row, col):   #Methode um Markierungen rückgängig zu machen
        if self.card[row][col] == 'X':
            self.card[row][col] = self.original_card[row][col]
            log_event(self.log_filename, f"Unmarked {self.card[row][col]} ({row}/{col})")

    def __str__(self):             # Methode zur Erstellung einer gut formatierten Zeichenkette um die Bingokarte besser darzustellen
        card_str = ""
        for row in self.card:
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        return card_str


def get_default_words():        #eine Liste mit default Words die zur Option steht wenn keine korrekte Wordfile eingegeben wird
    default_words = [
        "Synergie", "Rating", "Wertschöpfend", "Benefits", "Ergebnisorientiert", "Nachhaltig",
        "Hut aufhaben", "Visionen", "Zielführend", "Global Player", "Rund sein", "Szenario", "Diversity",
        "Corporate Identitiy", "Fokussieren", "Impact", "Target", "Benchmark", "Herausforderung(en)/Challenges",
        "Gadget", "Value", "Smart", "Web 2.0 oder 3.0", "Qualität", "Big Picture", "Revolution", "Pro-aktiv",
        "Game-changing", "Blog", "Community", "Social Media", "SOA", "Skalierbar", "Return on Invest (ROI)",
        "Wissenstransfer", "Best Practice", "Positionierung/Positionieren", "Committen", "Geforwarded",
        "Transparent", "Open Innovation", "Out-of-the-box", "Dissemination", "Blockchain", "Skills", "Gap",
        "Follower", "Win-Win", "Kernkomp"
    ]
    return random.sample(default_words, len(default_words))


def load_words(file_path, roundfile, xaxis, yaxis):       #Einlesen der Wordfile und Fehlerbehandlung bei falscher Wordfile
    def read_words_from_file(path):
        try:
            with open(path, 'r', encoding='utf-8') as file:
                return [line.strip() for line in file]
        except FileNotFoundError:
            return None

    while True:
        words = read_words_from_file(file_path)
        if words is not None and len(words) > int(xaxis) * int(yaxis):
            print("Länge:")
            print(len(words))
            return words

        print(f"Fehler: Datei '{file_path}' nicht gefunden oder zu wenige Wörter vorhanden.")
        user_choice = input(
            "Möchten Sie die Standardwörter verwenden (Option 1) oder einen anderen Dateipfad angeben (Option 2)? ") #Zwei Optionen für diese man sich entscheiden kann,wenn wordfile nicht gefunden

        if user_choice == '1':
            print("Standardwörter werden verwendet.")            # Wenn der User sich für 1 entscheidet werden Standardwörter benutzt
            set_wordfile_to_zero(roundfile)
            return get_default_words()
        elif user_choice == '2':
            file_path = input("Bitte geben Sie den Dateipfad zur Wortdatei ein: ")      #Wenn man sich für 2 entscheidet, kann der User einen neuen Pfad zur Wordfile eingeben
        else:                                         #
            print("Ungültige Eingabe. Bitte wählen Sie entweder Option 1 oder Option 2.")     #Wenn es eine falsche Eingabe gab kann er es erneut eingeben


# JAMIE END


# MARVIN
# Hauptfensterobjekt stdscr von curses als Übergabeparameter
def get_screen_content(stdscr):
    max_y, max_x = stdscr.getmaxyx()  # Fenstergröße der Shell ermitteln
    content = []  # leere liste content wird initialisiert
    for y in range(max_y):  # Schleife, die durch jede zeile iteriert, y ist zeilenindex
        line = []  # leere liste der zeile
        for x in range(max_x):  # x ist Spaltenindex, liest den Zeileninhalt und speichert ihn in line
            try:
                char = stdscr.inch(y, x)
                line.append(char)
            except curses.error:
                line.append(None)
        content.append(
            line)  # content ist liste mit allen zeilen, die jeweils wiederum eine liste der information der jeweiligen Zeile ist
    return content


# folgende Methode zeichnet die Bingo-Karte und den Gewinnbutton in die Shell
# Übergabeparameter: stdscr: Hauptfensterobjekt von der Curses Bibliothek -> für Text und Grafiken im Terminal
# card ist eine zweidimensionale liste, jedes Element ist ein Wort oder MArkierung der Bingo-Karte
# marked enthält markierten Felder der Bingokarte, ist ein set von tupeln
# field_width, field_height: Größe des Feldes in Zeichen (int)
# green_black, red_white, blue_yellow Farbpaare
# Offset als Platzhalter für die draw_players_info
# roundfile für Spielerinformationen
# boolean, ob button selected ist (initial auf false)
def draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow, offset_y, roundfile,
              button_selected=False):
    max_y, max_x = stdscr.getmaxyx()  # Höhe und Breite der geöffneten Shell
    card_height = len(card) * (
                field_height + 1)  # aus der höhe für ein Bingofeld wird die Höhe der karte ermittelt, 1 Zeichen Abstand
    card_width = len(card[0]) * (field_width + 1)  # das gleiche für die Breite
    button_height = 2  # Höhe des Buttons auf 2

    if max_y < card_height + button_height + getmaxplayer(
            roundfile) + 8:  # Check, ob die Shell zu klein vertikal ist, getmaxplayer steht für den Platz der players_info; außerdem +8 für Platz der Gewinnnachricht
        stdscr.clear()
        stdscr.addstr(0, 2, "Fenster ist zu klein, bitte vertikal vergrößern.", curses.A_BOLD | curses.color_pair(2))
        stdscr.refresh()
        return None, None, None, None
    elif max_x < card_width + 5:  # das gleiche Prinzip für die Breite, hier ist nur die Breite der BingoKarte relevant
        stdscr.clear()
        stdscr.addstr(0, 2, "Fenster ist zu klein, bitte horizontal vergrößern.", curses.A_BOLD | curses.color_pair(2))
        stdscr.refresh()
        return None, None, None, None

    for i, row in enumerate(card):  # Iteration durch jede row(zeile) der Karte
        for j, word in enumerate(row):  # Iteration durch jedes Element der Zeile
            x1, y1 = 2 + j * (field_width + 1), offset_y + 2 + i * (
                        field_height + 1)  # Koordinatenberechnung der linken oberen Ecke, x ist horizontal, y ist vertikal
            x2, y2 = x1 + field_width, y1 + field_height  # Koordinatenberechnung der rechten unteren Ecke, x ist horizontal, y ist vertikal
            if y2 >= max_y or x2 >= max_x:  # Überprüfen ob Feld innerhalb der Fenstergrenzen liegt
                continue
            try:  # Abfangen einer Exception: Beispielsweise wenn Werte in marked nicht richtig sind
                textpad.rectangle(stdscr, y1, x1, y2, x2)  # Rechteck um jedes Feld anhand ermittelten Koordinaten
                if (i, j) in marked:  # Befüllt Feld mit X mittig, falls markiertes Feld
                    stdscr.addstr(y1 + (field_height // 2), x1 + 1, "X".center(field_width - 1),
                                  curses.A_REVERSE | green_black)
                else:  # ansonsten wird das Feld mit dem Wort befüllt
                    stdscr.addstr(y1 + (field_height // 2), x1 + 1, word.center(field_width - 1), green_black)
            except curses.error:
                pass

    stdscr.addstr(0, 2, "Drücke 'X' zum Beenden",
                  curses.A_BOLD | red_white)  # Schrift ganz oben als Hinweis zum beenden

    button_text = "Klicke hier um Gewinn zu bestätigen"  # Buttontext wird initialisiert
    button_width = len(button_text) + 6  # Buttonbreite ist Text + Puffer

    button_y = offset_y + card_height + 2  # Berechnet Position des Buttons unter der Karte
    button_x = 2  # Button 2 Zeichen entfernt vom Rand
    # buttonhöhe wurde am Anfang der Methode auf 2 initialisiert

    try:
        textpad.rectangle(stdscr, button_y, button_x, button_y + button_height,
                          button_x + button_width)  # Umranden des Buttons nach ermittelten Koordinaten
    except curses.error:
        pass

    if button_selected:  # falls true, dann ändert sich Text auf "Gewinn bestätigt"
        button_text = "Gewinn bestätigt"
        stdscr.attron(red_white | curses.A_REVERSE)
    else:
        stdscr.attron(red_white)

    try:  # fügt den Text in den Button ein und stellt sicher, dass Textattribute nach dem Schreiben des Textes zurückgesetzt werden.
        stdscr.addstr(button_y + 1, button_x + 2, f" {button_text} ".center(button_width - 4))
        stdscr.attroff(red_white | curses.A_REVERSE)
    except curses.error:
        pass

    stdscr.refresh()
    return button_x, button_y, button_width, button_height  # Button wird für die Gewinnbestätigung verwendet, Programm muss wissen, wo sich dieser befindet


# Übergabeparameter: stdscr als haupt-curses-Fenster
# xaxis und yaxis sind Anzahl der Bingo-Zeilen und Spalten
# list words sind die für die Bingokarte relevanten Wörter
# mg beschreibt relevante messagequere
# maxplayer sind maximale Spieleranzahl, playernumber ist nummer des aktuellen spielers
# roundfile für Daten zum Spiel, log_filename um in das log zu schreiben
def main_game(stdscr, xaxis, yaxis, words, mq, maxplayer, playernumber, roundfile, log_filename):
    # Bestimmen von color-paaren für die visualisierung
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)
    blue_yellow = curses.color_pair(3)

    # Start und Größe des Feldes werden geloggt
    log_event(log_filename, "Start des Spiels")
    log_event(log_filename, f"Größe des Spielfelds: {xaxis}/{yaxis}")

    bingo_card = BingoCard(xaxis, yaxis, words, log_filename)  # Instanzierung des Objekts BingoKarte
    card = bingo_card.card  # Speichern der Karte in der Variable card
    marked = set()  # initialiseren eines sets für markierte Felder

    if xaxis == yaxis and xaxis % 2 == 1:  # Markieren des mittleren Feldes, wenn Karte ungerade Anzahl an Zeilen und Spalten hat
        middle = xaxis // 2
        marked.add((middle, middle))

    longest_word_length = max(
        len(word) for word in words)  # Feldbreite soll auf der Breite des längsten Wortes basieren
    field_width = longest_word_length + 2
    field_height = 4

    curses.mousemask(
        curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)  # Aktivieren: Erfassung der Mausereignisse und Mausposition

    players_data = read_roundfile(roundfile)  # Spielerinformationen aus Rundendatei einlesen
    offset_y = getmaxplayer(roundfile) + 1  # Platz für players_info anhand der maximalen Spieleranzahl

    stdscr.timeout(100)  # Timeout Eingabeabfrage auf 100ms

    # Initialisierung von Variablen zur Überwachung des Fensters, Fenstergröße, status und Anzahl der Spieler
    last_screen = get_screen_content(stdscr)
    prev_max_y, prev_max_x = stdscr.getmaxyx()
    nichtverloren = True
    gewonnen_nachricht = None
    last_player_count = len(players_data)

    # Initiale Zeichnung der Karte+Spielerinfo
    stdscr.clear()
    draw_players_info(stdscr, players_data, green_black)
    button_selected = False
    button_x, button_y, button_width, button_height = draw_card(
        stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow, offset_y, roundfile,
        button_selected
    )
    prev_max_y, prev_max_x = stdscr.getmaxyx()  # aktuelle Größe des Fensters wird gespeichert
    stdscr.refresh()  # Initiale Aktualisierung des Bildschirms

    # Initialisieren der Button-Dimensionen bei Fehlern
    if button_x is None or button_y is None or button_width is None or button_height is None:
        button_x, button_y, button_width, button_height = 2, 2, 20, 2  # default Werte

    while True:
        max_y, max_x = stdscr.getmaxyx()  # Fenstergrößé
        if max_y != prev_max_y or max_x != prev_max_x:  # Wenn Fenstergröße geändert wird Shell neu gezeichnet -> Bug Behebung
            stdscr.clear()
            draw_players_info(stdscr, players_data, green_black)
            button_x, button_y, button_width, button_height = draw_card(
                stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow, offset_y,
                roundfile, button_selected
            )
            prev_max_y, prev_max_x = max_y, max_x

            if button_x is None or button_y is None or button_width is None or button_height is None:
                button_x, button_y, button_width, button_height = 2, 2, 20, 2  # default values

            stdscr.refresh()  # Bildschirm aktualisieren bei Größenänderung

        # Wenn ein Spieler gewinnt, wird dessen name als mq gesendet
        message = check_for_message(mq)  # Überprüfen von Nachrichten in der message queue
        if message:  # wenn inhalt der message darauf hindeutet, dass man selbst gewonnen hat, erscheint dies, ansonsten erscheint eine Nachricht, welcher Spieler sonst gewonnen hat
            if message == getplayername(roundfile, playernumber):
                gewonnen_nachricht = "BINGO! Du hast gewonnen! Drücke X zum Beenden."
            else:
                gewonnen_nachricht = f"{message} hat gewonnen! Du hast verloren! Drücke X zum Beenden."
                nichtverloren = False

        key = stdscr.getch()  # Wartet auf Ereignis, außer timeout setzt ein

        if key == ord('x'):  # bei x wird spiel beendet
            break

        if nichtverloren and key == curses.KEY_MOUSE:  # überprüft ob spiel noch läuft und mausereignis aufgetreten ist
            _, mx, my, _, _ = curses.getmouse()  # mauskorrdinaten werden eingelesen und gespeichert
            if button_x is not None and button_y is not None:
                if button_x <= mx <= button_x + button_width and button_y <= my <= button_y + button_height:
                    button_selected = not button_selected  # boolean von Button wird geändert, wenn Mausereignis im Button ist
                    bingo_card.button_selected = button_selected
                    draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow,
                              offset_y, roundfile,
                              button_selected)  # Karte wird neu gezeichnet um geänderten Zustand des Buttons darzustellen
                    if button_selected and bingo_card.bingo_finish:  # Doppelte Gewinnüberprüfung: Button und Bingo muss erfüllt sein
                        gewinner = getplayername(roundfile, playernumber)
                        set_gameover(roundfile)
                        for i in range(int(maxplayer)):
                            mq.send(
                                gewinner.encode())  # Schreibe den Namen des Gewinners für anzahl an maxplayers in message queue

                        nichtverloren = False
                    continue

            # Verarbeitung von Klicks auf der Karte
            col = (mx - 2) // (field_width + 1)  # Berechnet Spalt des angeklickten Feldes
            row = (my - offset_y - 2) // (field_height + 1)  # Berechnet Zeile des angeklickten Feldes
            if 0 <= row < xaxis and 0 <= col < yaxis:  # WEnn Werte innerhalb Grenzen der KArte liegen
                if (row, col) in marked:  # wenn markiert
                    marked.remove((row, col))  # dann nicht mehr markieren
                    bingo_card.unmark(row, col)
                else:  # ansonten markieren
                    marked.add((row, col))
                    bingo_card.mark(row, col)
                draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow,
                          offset_y, roundfile, button_selected)  # Karte in jedem Fall neu zeichnen
                if bingo_card.check_bingo():  # Checken auf Bingo
                    if button_selected:  # wenn dann noch Button selected ist, wird nach dem Prinzip wie oben gewinnnachricht gesendet
                        gewinner = getplayername(roundfile, playernumber)
                        set_gameover(roundfile)
                        for i in range(int(maxplayer)):
                            mq.send(gewinner.encode())

                        nichtverloren = False

        new_players_data = read_roundfile(roundfile)  # aktuelle Spielerinformationen aus rundendatei
        if len(new_players_data) != last_player_count:  # WEnn Anzahl der Spieler geändert hat:
            players_data = new_players_data  # players_data wird geupdated und die ganze KArte + players_info neu gezeichnet
            stdscr.clear()
            draw_players_info(stdscr, players_data, green_black)
            button_x, button_y, button_width, button_height = draw_card(
                stdscr, card, marked, field_width, field_height, green_black, red_white, blue_yellow, offset_y,
                roundfile, button_selected
            )
            last_player_count = len(players_data)  # updaten anzahl der Spieler

        if gewonnen_nachricht:  # Wenn gewinnachticht vorhanden, wird diese unterhalb des Buttons angezeigt
            try:
                button_y_bottom = button_y + button_height + 2
                stdscr.addstr(button_y_bottom, 2, gewonnen_nachricht.center((field_width + 1) * yaxis), blue_yellow)
            except curses.error:
                stdscr.addstr(0, 2, gewonnen_nachricht, blue_yellow)
            stdscr.refresh()

        current_screen = get_screen_content(stdscr)  # Aktuellen Bildschirminhalt erfassen
        if current_screen != last_screen:  # Bildschirm nur aktualisieren, wenn sich der Inhalt geändert hat
            stdscr.refresh()
            last_screen = current_screen


# MARVIN END

# ROBIN
def get_words(file_path):  # Attribut wird übernommen
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Öffung und Decodierung des Dateiinhalts
            return [line.strip() for line in file]  # Zeilen werden durchgegangen und getrennt
    except FileNotFoundError:  # Ausnahmebehandlung
        print(f"Die Datei unter dem Pfad {file_path} wurde nicht gefunden.")  # Fehlermeldung
        return []  # leere Liste wird zurückgegeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Ein Fehler ist aufgetreten: {e}")  # Fehlermeldung
        return []  # leere Liste wird zurückgegeben


def set_wordfile_to_zero(filename):  # Attribut wird übernommen
    lines = []  # erstellen einer leeren Liste
    with open(filename, 'r') as file:  # Datei wird gelesen
        lines = file.readlines()  # Datei wird in "Lines" gespeichert

    with open(filename, 'w') as file:  # Datei wird im schreibmodus geöffnet
        for line in lines:  # jede Zeile der Datei wird durchgegangen
            if line.startswith('wordfile:'):  # wenn eine Zeile mit "wordfile": beginnt
                file.write('wordfile: 0\n')  # wird die "wordfile" auf 0 gesetzt
            else:
                file.write(line)  # andernfalls wird die ursprüngliche Zeile in die Datei geschrieben


def check_wordfile_not_zero(filename):  # Attribut wird übernommen
    with open(filename, 'r') as file:  # Datei wird gelesen
        for line in file:  # jede Zeile der Datei wird durchgegangen
            if line.startswith('wordfile:'):  # wenn eine Zeile mit "wordfile": beginnt
                value = line.split(':')[1].strip()  # Zeile wird aufgeteilt, leerzeichen entfernt
                if value == '0':  # wenn der Wert nach "wordfile" = 0
                    return False  # wird false zurückgegeben
                else:
                    return True  # ansonsten True
    return False  # wenn keine Zeile mit wordfile: gefunden wurde, gibt die Funktion False zurück


def change_wordfile(filename, new_value):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('wordfile:'):
                line = f'wordfile: {new_value}\n'
            lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(lines)


def getmaxplayer(rundendatei):  # Attribute werden übernommen
    try:
        with open(rundendatei, 'r') as f:  # rundendatei wird im Lesemodus geöffnet
            for line in f:  # rundendatei wird durchlaufen
                if line.startswith("maxplayer:"):  # wenn ein zeile mit "maxplayer" beginnt
                    return int(line.split(":")[1].strip())  # wird der Wert danach extrahiert und zurückgegeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Error reading max players from {rundendatei}: {e}")  # Fehlermeldung
        return None


def getwordfile(rundendatei):  # Attribute werden übernommen
    try:
        with open(rundendatei, 'r') as f:  # rundendatei wird im Lesemodus geöffnet
            for line in f:  # rundendatei wird durchlaufen
                if line.startswith("wordfile:"):  # wenn ein zeile mit "wordfile" beginnt
                    return line.split(":")[1].strip()  # wird der Wert danach extrahiert und zurückgegeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Error reading max players from {rundendatei}: {e}")  # Fehlermeldung
        return None


def getplayername(rundendatei, player_count):  # Attribute werden übernommen
    try:
        with open(rundendatei, 'r') as f:  # rundendatei wird im Lesemodus geöffnet
            playerstring = "playername" + str(player_count)  # suchbegriff "(playerstring)" wird erstellt
            for line in f:  # rundendatei wird durchlaufen
                if line.startswith(playerstring):  # wenn ein zeile mit "(playerstring)" beginnt
                    return str(line.split(":")[1].strip())  # wird der Wert danach extrahiert und zurückgegeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Error reading playername from {rundendatei}: {e}")  # Fehlermeldung
        return None


def getplayer(rundendatei):  # Attribute werden übernommen
    try:
        with open(rundendatei, 'r') as f:  # rundendatei wird im Lesemodus geöffnet
            for line in f:  # rundendatei wird durchlaufen
                if line.startswith("players:"):  # wenn ein zeile mit "player" beginnt
                    return int(line.split(":")[1].strip())  # wird der Wert danach extrahiert und zurückgegeben
    except Exception as e:  # Ausnahmebehandlung
        print(f"Error reading players from {rundendatei}: {e}")  # Fehlermeldung
        return None

# BENEDIKT

def clear_and_close_message_queue(mq_name):
    try:

        # Öffne die Message-Queue
        mq = posix_ipc.MessageQueue(mq_name)

        # Leere die Message-Queue
        while True:
            try:
                mq.receive(timeout=1)  # timeout in seconds
            except posix_ipc.BusyError:
                # Keine weiteren Nachrichten vorhanden
                break

        # Schließe die Message-Queue
        mq.close()

        # Lösche die Message-Queue
        posix_ipc.unlink_message_queue(mq_name)

        print(f"Message-Queue {mq_name} wurde erfolgreich geleert und gelöscht.")

    except posix_ipc.Error as e:
        print(f"Fehler beim Umgang mit der Message-Queue: {e}")
        sys.exit(1)


def end_round(roundfile, mq_name):
    if decrease_players(roundfile):
        print(mq_name)
        clear_and_close_message_queue(mq_name)


def handle_sigint(roundfile, mq_name, sig, frame):
    end_round(roundfile, mq_name)
    print("\nSIGINT empfangen. Das Programm wird beendet...")

    exit(0)  # Beende das Programm


def host_start(maxplayer, roundfile, xaxis, yaxis, wordfile, hostname):
    # Erzeuge den Namen der Message-Queue
    mq_name = f"/{hostname}_{maxplayer}_{os.getpid()}"

    # Erstellt MessageQueue falls nicht bereits vorhanden
    mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)
    # behandelt Spielabbruch durch STRG+C
    signal.signal(signal.SIGINT, partial(handle_sigint, roundfile, mq_name))

    # Prüfen ob ein  Wordfile Pfad existiert
    # Wenn ja, lade load_words (Überprüft auch auf Gültigkeit!)
    if wordfile != 0:
        words = load_words(wordfile, roundfile, xaxis, yaxis)
    # Wenn nicht, lade Standardwörter
    else:
        words = get_default_words()

    # Starte blockierendes Ereignis mq.receive und warte auf Spieler 2
    print("\nBingo wird gestartet. Warte auf mind. einen Mitspieler...")

    message, _ = mq.receive()
    print(f": {message.decode()}")

    # Wenn eine Nachricht vorhanden
    if message:

        try:
            # Initialisiere Log für Host
            log_filename = create_log_file(hostname)
            # Starte die Curses Umgebung (startet das gesamte Bingospiel für den Host)
            curses.wrapper(main_game, int(xaxis), int(yaxis), words, mq, maxplayer, 1, roundfile, log_filename)

            end_round(roundfile, mq_name)
            print("Host beendet")
        # Behandle FileNotFound Error
        except FileNotFoundError as e:
            print(e)
            exit(1)
        # Behandle Value Error
        except ValueError as e:
            print(e)
            exit(1)


def player_start(second, playernumber, roundfile, maxplayer, xaxis, yaxis, wordfile):
    mq_name = f"/{getplayername(roundfile, 1)}_{maxplayer}_{get_pid_host(roundfile)}"
    mq = posix_ipc.MessageQueue(mq_name)
    signal.signal(signal.SIGINT, partial(handle_sigint, roundfile, mq_name))

    if second:
        playername = getplayername(roundfile, playernumber)
        message = "Spieler 2 ist beigetreten: " + playername
        mq.send(message.encode())
        try:
            if check_wordfile_not_zero(roundfile):
                words = get_words(wordfile)
            else:
                words = get_default_words()

            log_filename = create_log_file(playername)
            log_event(log_filename, "Spieler 2 beigetreten")
            curses.wrapper(main_game, int(xaxis), int(yaxis), words, mq, maxplayer, playernumber, roundfile, log_filename)

            print("Spieler 2 beendet")
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except ValueError as e:
            print(e)
            exit(1)
    else:
        try:
            if check_wordfile_not_zero(roundfile):
                words = get_words(wordfile)
            else:
                words = get_default_words()

            playername = getplayername(roundfile, playernumber)
            log_filename = create_log_file(playername)
            log_event(log_filename, f"Spieler {playernumber} beigetreten")
            curses.wrapper(game, int(xaxis), int(yaxis), words, mq, maxplayer, playernumber, roundfile, log_filename)

            print(f"Spieler{playernumber} beendet")
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except ValueError as e:
            print(e)
            exit(1)
    end_round(roundfile, mq_name)


def check_for_message(mq):
    try:
        message, _ = mq.receive(timeout=0)
        return message.decode()
    except posix_ipc.BusyError:
        return None


def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False


def parse_args_host(args):
    config = {
        "xaxis": 5, "yaxis": 5, "roundfile": "rundendatei.txt",
        "maxplayers": 5, "wordfile": 0, "playername": None
    }

    i = 2
    while i < len(args):
        # Verarbeite das Argument "-roundfile"
        if args[i] == "-roundfile":
            # Überprüfen ob ein Argument danach folgt und ob dieses nicht mit - beginnt
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                config["roundfile"] = args[i + 1]
                i += 2
            else:
                print("Fehlendes Argument für -roundfile.")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-xaxis"
        elif args[i] == "-xaxis":
            # Überprüfen ob ein Argument danach ein Integer ist und ob dieses kleiner als 8 und größer als 2 ist
            if i + 1 < len(args) and is_integer(args[i + 1]) and 2 < int(args[i + 1]) < 8:
                config["xaxis"] = int(args[i + 1])
                i += 2
            else:
                print("Falsches Argument für -xaxis. Min: 3 / Max: 7")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-yaxis"
        elif args[i] == "-yaxis":
            # Überprüfen ob ein Argument danach ein Integer ist und ob dieses kleiner als 8 und größer als 2 ist
            if i + 1 < len(args) and is_integer(args[i + 1]) and 2 < int(args[i + 1]) < 8:
                config["yaxis"] = int(args[i + 1])
                i += 2
            else:
                print("Falsches Argument für -yaxis. Min: 3 / Max: 7")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-wordfile"
        elif args[i] == "-wordfile":
            # Überprüfen ob ein Argument danach folgt und ob dieses nicht mit - beginnt
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                config["wordfile"] = args[i + 1]
                i += 2
            else:
                print("Fehlendes Argument für -wordfile.")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-maxplayers"
        elif args[i] == "-maxplayers":
            # Überprüfen ob ein Argument folgt welches ein Integer ist
            if i + 1 < len(args) and is_integer(args[i + 1]):
                config["maxplayers"] = int(args[i + 1])
                i += 2
            else:
                print("Fehlendes Argument für -maxplayers.")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-playername"
        elif args[i] == "-playername":
            # Überprüfen ob ein Argument danach folgt und ob dieses nicht mit - beginnt
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                config["playername"] = args[i + 1]
                i += 2
            else:
                print("Fehlendes oder ungültiges Argument für -playername.")
                print_usage()
                sys.exit(1)
        else:
            print(f"Unbekanntes Argument {args[i]}")
            print_usage()
            sys.exit(1)

    return config


def parse_args_player(args):
    # Initialisiere Konfiguration für den Beitritt
    config = {
        "roundfile": "rundendatei.txt",
        "playername": None,
    }

    i = 2
    while i < len(args):
        # Verarbeite das Argument "-roundfile"
        if args[i] == "-roundfile":
            # Überprüfe, ob ein Argument danach folgt und ob dieses nicht mit - beginnt
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                config["roundfile"] = args[i + 1]
                i += 2
            else:
                print("Fehlendes Argument für -roundfile.")
                print_usage()
                sys.exit(1)
        # Verarbeite das Argument "-playername"
        elif args[i] == "-playername":
            # Überprüfe, ob ein Argument danach folgt und ob dieses nicht mit - beginnt
            if i + 1 < len(args) and not args[i + 1].startswith('-'):
                config["playername"] = args[i + 1]
                i += 2
            else:
                print("Fehlendes Argument für -playername oder ungültiges Format.")
                print_usage()
                sys.exit(1)
        else:
            print(f"Unbekanntes Argument {args[i]}")
            print_usage()
            sys.exit(1)

    return config


# Funktion zur Ausgabe der Nutzungshinweise
def print_usage():
    print(
        "Spiel erstellen: meinskript.py -newround [-roundfile rundendatei.txt -xaxis INT -yaxis INT -maxplayers INT] -wordfile wordfile.txt -playername NAME")
    print("Spiel beitreten: meinskript.py -joinround [-roundfile rundendatei.txt] -playername NAME")
    print("Hinweis: Die Argumente in Klammern sind optional und müssen nicht angegeben werden!")


if __name__ == "__main__":
    # Prüfe, ob die Anzahl der Argumente in einem sinnvollen Bereich liegt
    if len(sys.argv) < 4 or len(sys.argv) > 14:
        print_usage()
        sys.exit(1)

    # Verarbeite den Befehl "-newround"
    if sys.argv[1] == "-newround":
        config = parse_args_host(sys.argv)
        # Überprüfe ob der Spielername fehlt
        if config["playername"] is None:
            print("Fehlendes Argument für -playername.")
            print_usage()
            sys.exit(1)
        # Wenn Spielername korrekt angegeben erstelle Roundfile und starte host_start()
        else:
            create_roundfile(config["roundfile"], config["xaxis"], config["yaxis"], config["maxplayers"],
                             config["playername"], config["wordfile"])
            host_start(config["maxplayers"], config["roundfile"], config["xaxis"], config["yaxis"], config["wordfile"],
                       config["playername"])

    # Verarbeite den Befehl "-joinround"
    elif sys.argv[1] == "-joinround":
        config = parse_args_player(sys.argv)

        # Prüfe, ob die Rundendatei existiert
        if os.path.exists(config["roundfile"]):
            # Prüfe, ob das Spiel bereits vorbei ist
            if check_gameover(config["roundfile"]):
                print("Beitritt abgebrochen! Das Spiel ist bereits vorbei.")
                exit(1)

            # Prüfe, ob die maximale Spieleranzahl erreicht ist
            mplayer = getmaxplayer(config["roundfile"])
            if getplayer(config["roundfile"]) < mplayer:
                playernumber = incplayer(config["roundfile"], config["playername"])
                print("Ich bin Spieler Nummer: " + str(playernumber))
                if playernumber != 2:
                    player_start(False, playernumber, config["roundfile"], mplayer, getyachse(config["roundfile"]),
                                 getxachse(config["roundfile"]), getwordfile(config["roundfile"]))
                else:
                    player_start(True, playernumber, config["roundfile"], mplayer, getxachse(config["roundfile"]),
                                 getyachse(config["roundfile"]), getwordfile(config["roundfile"]))
            else:
                print("Maximale Spieleranzahl erreicht. Beitritt abgebrochen")
        else:
            print("Beitritt nicht möglich! Die angegebene Rundendatei existiert nicht")
    else:
        print("Unbekannter Befehl")
        print_usage()
        sys.exit(1)
