import sys
import posix_ipc
import time
import os
import random
import curses
from curses import textpad
import argparse
import datetime

def create_log_file(player_name):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    filename = f"{timestamp}-bingo-{player_name}.txt"
    return filename

def log_event(filename, event):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    with open(filename, 'a') as file:
        file.write(f"{timestamp} {event}\n")

def host_start(maxplayer, roundfile, xaxis, yaxis, wordfile, hostname, words):
    # HOST Methode, erstellt erstmalig die MQ und wartet auf Spieler 2

    # Erstellen der Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)

    #Aufrufen der load_words Methode (enthält Exception und Option Standardwörter zu verwenden
    #words = load_words(wordfile, roundfile)
    #if len(words) < int(xaxis) * int(yaxis):
    #    raise ValueError("Nicht genügend Wörter in der Datei, um die Bingo-Karte zu füllen.")

    print("\nBingo wird gestartet. Warte auf mind. einen Mitspieler...")

    # Warten auf Nachricht vom Client
    message, _ = mq.receive()
    print(f": {message.decode()}")

    # Sobald Spieler 2 beigetreten ist startet das Spiel
    if message:
        try:
            # wörter aus angegebener Datei werden geladen

            # Log-Datei erstellen mit dem Spielernamen
            log_filename = create_log_file(hostname)  # Host ist der Name des ersten Spielers

            # Die Main-Methode wird als Curses Umgebung gestartet
            curses.wrapper(main, int(xaxis), int(yaxis), words, mq, maxplayer, 1, roundfile, log_filename)
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except ValueError as e:
            print(e)
            exit(1)

    # Message Queue schließen
    mq.close()

def player_start(second, playernumber, roundfile, maxplayer, xaxis, yaxis, wordfile):
    # SPIELER Methode, tritt dem Spiel bei

    # Initialisiere den Namen der Message Queue
    mq_name = "/my_message_queue"

    # Öffne die existierende Message Queue
    mq = posix_ipc.MessageQueue(mq_name)

    # Falls es sich um Spieler 2 handelt, wird die Nachricht an den Host gesendet
    if second:
        # Nachricht an Spieler 1 senden
        playername = getplayername(roundfile, playernumber)
        message = "Spieler2 ist beigetreten: " + playername
        mq.send(message.encode())
        try:
            # wörter aus angegebener Datei werden geladen
            #words = load_words(wordfile)

            if check_wordfile_not_zero(roundfile):
                words = get_words(wordfile)
            else:
                words = get_default_words()

            if len(words) < int(xaxis) * int(yaxis):
                raise ValueError("Nicht genügend Wörter in der Datei, um die Bingo-Karte zu füllen.")

            log_filename = create_log_file(playername)
            log_event(log_filename, "Spieler 2 beigetreten")

            # Die Main-Methode wird als Curses Umgebung gestartet
            curses.wrapper(main, int(xaxis), int(yaxis), words, mq, maxplayer, playernumber, roundfile, log_filename)
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except ValueError as e:
            print(e)
            exit(1)

    # Falls es sich um Spieler != 2 handelt wird das Spiel gestartet
    else:
        # Starte Bingo
        try:
            # wörter aus angegebener Datei werden geladen
            if check_wordfile_not_zero(roundfile):
                words = get_words(wordfile)
            else:
                words = get_default_words()

            if len(words) < int(xaxis) * int(yaxis):
                raise ValueError("Nicht genügend Wörter in der Datei, um die Bingo-Karte zu füllen.")

            playername = getplayername(roundfile, playernumber)
            log_filename = create_log_file(playername)
            log_event(log_filename, f"Spieler {playernumber} beigetreten")

            # Die Main-Methode wird als Curses Umgebung gestartet
            curses.wrapper(main, int(xaxis), int(yaxis), words, mq, maxplayer, playernumber, roundfile, log_filename)
        except FileNotFoundError as e:
            print(e)
            exit(1)
        except ValueError as e:
            print(e)
            exit(1)

def check_for_message(mq):
    # Methode die prüft ob eine Nachricht in der MQ vorliegt
    try:
        message, _ = mq.receive(timeout=0)  # Versuche, eine Nachricht zu empfangen
        return message.decode()  # Nachricht vorhanden, gebe sie zurück
    except posix_ipc.BusyError:
        return None  # Keine Nachricht vorhanden

def is_integer(value):
    # Methode die prüft ob ein Wert ein Integer ist
    try:
        int(value)
        return True
    except ValueError:
        return False

def getxachse(rundendatei):
    # Methode gibt anhand der roundfile die xachse zurück
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("width:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading x-axis from {rundendatei}: {e}")
        return None

def getyachse(rundendatei):
    # Methode gibt anhand der roundfile die yachse zurück
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("height:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading y-axis from {rundendatei}: {e}")
        return None

def getmaxplayer(rundendatei):
    # Methode gibt den maxplayer Wert aus der roundfile zurück
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("maxplayer:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading max players from {rundendatei}: {e}")
        return None

def getwordfile(rundendatei):
    # Methode gibt den wordfile Wert aus der roundfile zurück
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("wordfile:"):
                    return line.split(":")[1].strip()
    except Exception as e:
        print(f"Error reading max players from {rundendatei}: {e}")
        return None

def getplayername(rundendatei, player_count):
    # Methode gibt den Spielernamen anhand von roundfile, playernumber zurück
    try:
        with open(rundendatei, 'r') as f:
            playerstring = "playername" + str(player_count)
            for line in f:
                if line.startswith(playerstring):
                    return str(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading playername from {rundendatei}: {e}")
        return None

def getplayer(rundendatei):
    # Methode gibt den Wert der bisher beigetretenen Spieler zurück
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("players:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading players from {rundendatei}: {e}")
        return None
#test
def incplayer(rundendatei, spielername):
    # Methode zur Verwaltung der Spieler, Namens / Nummernzuweisung
    try:
        # Lese den aktuellen Spielerzähler
        with open(rundendatei, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("players:"):
                # Extrahiert den int nach playercount anhand vom ":"
                player_count = int(line.split(":")[1].strip())
                # erhöht die Spieleranzahl um 1 (beigetreten)
                player_count += 1
                # Schreibt den neuen Wert zurück
                lines[i] = f"players: {player_count}\n"
                break
        # String Variable die playernumber1/2/3/n einträgt
        playerstring = "playername" + str(player_count)

        # playernumber{n} wird mit dem Namen und der PID gespeichert
        # Trennung erfolgt mit ":" für die .split Methode
        # Wird als Line "drangehängt"
        lines.append(f"{playerstring}: {spielername}: {os.getpid()}\n")

        # Schreibe den neuen Inhalt zurück in die Datei
        with open(rundendatei, 'w') as f:
            f.writelines(lines)
        return player_count
    except Exception as e:
        print(f"Error updating players in {rundendatei}: {e}")

def create_roundfile(rundendatei, xachse, yachse, maxspieler, hostname, wordfile):  # Upload.
    # Methode für die roundfile, integriert direkt die PID des Hosts
    try:
        with open(rundendatei, 'w') as f:
            f.write(f"maxplayer: {maxspieler}\n")
            f.write(f"wordfile: {wordfile}\n")
            f.write(f"height: {yachse}\n")
            f.write(f"width: {xachse}\n")
            f.write(f"players: {1}\n")
            f.write(f"playername1: {hostname}: {os.getpid()}\n")
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

def draw_players_info(stdscr, players_data, color_pair):
    max_y, max_x = stdscr.getmaxyx()
    y_position = 1
    stdscr.addstr(y_position, 2, "TEILNEHMER:", color_pair)  # Hinzufügen der Zeile "TEILNEHMER:"
    y_position += 1
    for player_info in players_data:
        stdscr.addstr(y_position, 2, player_info, color_pair)
        y_position += 1
    stdscr.refresh()

class BingoCard:
    # Konstruktor BingoCard, Originalkarte wird als Kopie gespeichert.
    def __init__(self, rows, cols, words, log_filename):
        self.rows = rows
        self.cols = cols
        self.log_filename = log_filename
        # Attribut Karte wird mit Methode create_card erstellt
        self.card = self.create_card(words)
        self.original_card = [row[:] for row in
                              self.card]  # Kopie der Originalkarte, um später die Klicks auch rückgängig machen zu können
        self.button_selected = False
        self.bingo_finish = False


    # gibt liste mit wörtern aus wordfile wieder
    def create_card(self, words):
        # leere Liste
        card = []
        used_words = set()  # Verwendete Wörter speichern, um Duplikate zu vermeiden, jedes Element im Set kann nur einmal vorkommen

        # Zufällige Wörter in die Karte einfügen
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                # von der Logik durchgehen
                if self.rows % 2 != 0 and self.cols % 2 != 0 and i == self.rows // 2 and j == self.cols // 2:
                    row.append('X')  # Mittleres Feld als Joker, Symbol 'X' verwendet
                else:
                    word = random.choice(words)
                    while word in used_words:
                        word = random.choice(words)
                    row.append(self.split_word(word))
                    used_words.add(word)
            card.append(row)
        return card

    def split_word(self, word):
        # Keine Zeilentrennung, das Wort bleibt in einer Zeile
        return word

    def check_bingo(self):




        # Horizontale Überprüfung
        for row in self.card:
            if all(cell == 'X' for cell in row):
                self.bingo_finish = True
                return True

        # Vertikale Überprüfung
        for col in range(self.cols):
            if all(self.card[row][col] == 'X' for row in range(self.rows)):
                self.bingo_finish = True
                return True

        # Diagonale Überprüfung (von links oben nach rechts unten)
        if all(self.card[i][i] == 'X' for i in range(min(self.rows, self.cols))):
            self.bingo_finish = True
            return True

        # Diagonale Überprüfung (von rechts oben nach links unten)
        if all(self.card[i][self.cols - i - 1] == 'X' for i in range(min(self.rows, self.cols))):
            self.bingo_finish = True
            return True


        return False




    def mark(self, row, col):
        self.card[row][col] = 'X'  # Markieren mit einem Kreuz
        log_event(self.log_filename, f"Marked {self.original_card[row][col]} ({row}/{col})")

    def unmark(self, row, col):
        if self.card[row][col] == 'X':  # Nur wenn es sich nicht um das Jokerfeld handelt
            self.card[row][col] = self.original_card[row][col]  # Rücksetzen auf das Originalwort
            log_event(self.log_filename, f"Unmarked {self.card[row][col]} ({row}/{col})")

    def __str__(self):
        card_str = ""
        for row in self.card:
            # Für jede Zeile in der BingoCard wird eine Zeichenkette erstellt. Zellen der Zeile sind durch "|" getrennt.
            card_str += " | ".join(f"{cell:15}" for cell in row) + "\n"
        # Rückgabe sind alle Wörter als String. Jedes Wort ist eine Zelle, 15 Zeichen breit, und Zellen werden mit "|" getrennt
        return card_str


def draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, offset_y,
              button_selected=False):
    stdscr.clear()
    max_y, max_x = stdscr.getmaxyx()  # Maximale Größe des Fensters
    card_height = len(card) * (field_height + 1)
    card_width = len(card[0]) * (field_width + 1)

    for i, row in enumerate(card):
        for j, word in enumerate(row):
            x1, y1 = 2 + j * (field_width + 1), offset_y + 2 + i * (field_height + 1)  # Offset hinzugefügt
            x2, y2 = x1 + field_width, y1 + field_height
            # Überprüfen, ob die Koordinaten innerhalb der Fenstergrenzen liegen
            if y2 >= max_y or x2 >= max_x:
                continue
            try:
                textpad.rectangle(stdscr, y1, x1, y2, x2)  # Zeichnet eine Umrandung um jedes Feld
                if (i, j) in marked:
                    stdscr.addstr(y1 + (field_height // 2), x1 + 1, "X".center(field_width - 1),
                                  curses.A_REVERSE | green_black)  # Wenn markiert, dann 'X'
                else:
                    stdscr.addstr(y1 + (field_height // 2), x1 + 1, word.center(field_width - 1), green_black)
            except curses.error:
                pass  # Fehler ignorieren, wenn das Fenster zu klein ist

    # **Anweisung zum Beenden ganz oben in der Mitte hinzufügen**
    stdscr.addstr(0, (max_x - len("Drücke 'X' zum Beenden")) // 2, "Drücke 'X' zum Beenden",
                  curses.A_BOLD | green_black)

    # Button mittig unter der Karte hinzufügen
    button_text = "Klicke hier um Gewinn zu bestätigen"
    button_width = len(button_text) + 6  # Platz für Polsterung
    button_height = 3
    card_x_center = (max_x - card_width) // 2
    card_y_bottom = offset_y + card_height + 2
    button_x = card_x_center + (card_width - button_width) // 2
    button_y = card_y_bottom  # Position direkt unter der Karte

    # Zeichne eine Umrandung um den Button
    try:
        textpad.rectangle(stdscr, button_y, button_x, button_y + button_height, button_x + button_width)
    except curses.error:
        pass  # Fehler ignorieren, wenn das Fenster zu klein ist

    if button_selected:
        button_text = "Gewinn bestätigt"
        stdscr.attron(red_white | curses.A_REVERSE)  # Setzt den Farbpaar für den ausgewählten Button (reverse)
    else:
        stdscr.attron(red_white)  # Setzt den Farbpaar für den Button (rot-weiß)

    try:
        stdscr.addstr(button_y + 1, button_x + 2, f" {button_text} ".center(button_width - 4))
        stdscr.attroff(red_white | curses.A_REVERSE)
    except curses.error:
        pass  # Fehler ignorieren, wenn das Fenster zu klein ist

    stdscr.refresh()
    return button_x, button_y, button_width, button_height


def main(stdscr, xaxis, yaxis, words, mq, maxplayer, playernumber, roundfile, log_filename):
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_RED)
    curses.init_pair(3, curses.COLOR_BLUE, curses.COLOR_YELLOW) # Blau-gelbe Farbpaare für den Button
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)
    blue_yellow = curses.color_pair(3)

    log_event(log_filename, "Start des Spiels")
    log_event(log_filename, f"Größe des Spielfelds: {xaxis}/{yaxis}")

    bingo_card = BingoCard(xaxis, yaxis, words, log_filename)
    card = bingo_card.card
    marked = set()

    if xaxis == yaxis and xaxis % 2 == 1:
        middle = xaxis // 2
        marked.add((middle, middle))

    longest_word_length = max(len(word) for word in words)
    field_width = longest_word_length + 2
    field_height = 4

    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)

    players_data = read_roundfile(roundfile)  # Spielerinformationen laden
    offset_y = getmaxplayer(roundfile) + 1  # Verschiebung um maxplayers + 1 Zeilen nach unten
    draw_players_info(stdscr, players_data, green_black)  # Spielerinformationen anzeigen

    button_selected = False
    button_x, button_y, button_width, button_height = draw_card(stdscr, card, marked, field_width, field_height,
                                                                green_black, red_white, offset_y, button_selected)

    nichtverloren = True
    gewonnen_nachricht = None  # Hinzufügen einer Variablen, um die Gewinnnachricht zu speichern

    stdscr.timeout(1000)  # 1000 ms (1 Sekunde) Timeout für nicht blockierende Eingabe

    while True:
        message = check_for_message(mq)
        if message:
            if message == getplayername(roundfile, playernumber):
                gewonnen_nachricht = "BINGO! Du hast gewonnen! Drücke X zum Beenden."
            else:
                gewonnen_nachricht = f"{message} hat gewonnen! Du hast verloren! Drücke X zum Beenden."
            nichtverloren = False

        key = stdscr.getch()

        if key == ord('x'):
            break


        if nichtverloren and key == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            if button_x is not None and button_y is not None:
                if button_x <= mx <= button_x + button_width and button_y <= my <= button_y + button_height:
                    button_selected = not button_selected
                    bingo_card.button_selected = button_selected
                    draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, offset_y, button_selected)
                    if button_selected and bingo_card.bingo_finish:
                        gewinner = getplayername(roundfile, playernumber)
                        for i in range(int(maxplayer)):
                            mq.send(gewinner.encode())
                        gewonnen_nachricht = "BINGO! Du hast gewonnen! Drücke X zum Beenden."
                        nichtverloren = False
                    continue

            col = (mx - 2) // (field_width + 1)
            row = (my - offset_y - 2) // (field_height + 1)  # Offset berücksichtigen
            if 0 <= row < xaxis and 0 <= col < yaxis:
                if (row, col) in marked:
                    marked.remove((row, col))
                    bingo_card.unmark(row, col)
                else:
                    marked.add((row, col))
                    bingo_card.mark(row, col)
                draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, offset_y, button_selected)
                if bingo_card.check_bingo():
                    if button_selected:
                        gewinner = getplayername(roundfile, playernumber)
                        for i in range(int(maxplayer)):
                            mq.send(gewinner.encode())
                        gewonnen_nachricht = "BINGO! Du hast gewonnen! Drücke X zum Beenden."
                        nichtverloren = False

        draw_card(stdscr, card, marked, field_width, field_height, green_black, red_white, offset_y, button_selected)
        players_data = read_roundfile(roundfile)  # Spielerinformationen neu laden
        draw_players_info(stdscr, players_data, green_black)  # Spielerinformationen erneut anzeigen

        # Kontinuierliche Anzeige der Gewinnnachricht
        if gewonnen_nachricht:
            button_y_bottom = button_y + button_height + 2  # Position unter dem Button
            stdscr.addstr(button_y_bottom, 2,
                          gewonnen_nachricht.center((field_width + 1) * yaxis), blue_yellow)
            stdscr.refresh()

def get_words(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file]
    except FileNotFoundError:
        print(f"Die Datei unter dem Pfad {file_path} wurde nicht gefunden.")
        return []
    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
        return []

def set_wordfile_to_zero(filename):
    lines = []
    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            if line.startswith('wordfile:'):
                file.write('wordfile: 0\n')
            else:
                file.write(line)

def check_wordfile_not_zero(filename):
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('wordfile:'):
                # Extrahiere den Wert hinter 'wordfile:'
                value = line.split(':')[1].strip()
                if value == '0':
                    return False
                else:
                    return True
    return False  # Falls keine 'wordfile:' Zeile gefunden wurde


def change_wordfile(filename, new_value):
    lines = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('wordfile:'):
                line = f'wordfile: {new_value}\n'
            lines.append(line)

    with open(filename, 'w') as file:
        file.writelines(lines)
def get_default_words():
    default_words = [
        "Synergie", "Rating", "Wertschöpfend", "Benefits", "Ergebnisorientiert", "Nachhaltig",
        "Hut aufhaben",
        "Visionen", "Zielführend", "Global Player", "Rund sein", "Szenario", "Diversity",
        "Corporate Identitiy",
        "Fokussieren", "Impact", "Target", "Benchmark", "Herausforderung(en)/Challenges", "Gadget", "Value",
        "Smart",
        "Web 2.0 oder 3.0", "Qualität", "Big Picture", "Revolution", "Pro-aktiv", "Game-changing", "Blog",
        "Community",
        "Social Media", "SOA", "Skalierbar", "Return on Invest (ROI)", "Wissenstransfer", "Best Practice",
        "Positionierung/Positionieren", "Committen", "Geforwarded", "Transparent", "Open Innovation",
        "Out-of-the-box",
        "Dissemination", "Blockchain", "Skills", "Gap", "Follower", "Win-Win", "Kernkomp"
    ]
    return random.sample(default_words, len(default_words))

# Datei wird im Lesemodus geöffnet und jede Zeile ist ein Index im Array
def load_words(file_path, roundfile, xaxis, yaxis):
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
            "Möchten Sie die Standardwörter verwenden (Option 1) oder einen anderen Dateipfad angeben (Option 2)? ")

        if user_choice == '1':
            print("Standardwörter werden verwendet.")
            set_wordfile_to_zero(roundfile)
            return get_default_words()
        elif user_choice == '2':
            file_path = input("Bitte geben Sie den Dateipfad zur Wortdatei ein: ")
        else:
            print("Ungültige Eingabe. Bitte wählen Sie entweder Option 1 oder Option 2.")

def parse_args(args):
    #Methode zur Festlegung von Standardwerten
    config = {
        "xaxis": 5,
        "yaxis": 5,
        "roundfile": "rundendatei.txt",
        "maxplayers": 10,
        #Werte dürfen nicht null sein:
        "wordfile": None,
        "playername": None,
    }

    #durchlaufen aller Argumente (Shell)
    #Falls Argument vorhanden, wird der -Wert- (i+1) überschrieben
    i = 2
    while i < len(args):
        if args[i] == "-roundfile":
            config["roundfile"] = args[i + 1]
            i += 2
        elif args[i] == "-xaxis":
            if is_integer(args[i + 1]):
                config["xaxis"] = int(args[i + 1])
            i += 2
        elif args[i] == "-yaxis":
            #Werte werden nur überschrieben wenn Datentyp zulässig
            if is_integer(args[i + 1]):
                config["yaxis"] = int(args[i + 1])
            i += 2
        elif args[i] == "-wordfile":
            config["wordfile"] = args[i + 1]
            i += 2
        elif args[i] == "-maxplayers":
            # Werte werden nur überschrieben wenn Datentyp zulässig
            if is_integer(args[i + 1]):
                config["maxplayers"] = int(args[i + 1])
            i += 2
        elif args[i] == "-playername":
            config["playername"] = args[i + 1]
            i += 2
        else:
            i += 1
    #Gibt die aktualisierte Config zurück
    return config

if __name__ == "__main__":
    #Fehlerhafte Argumenteingaben behandeln:
    if len(sys.argv) < 3 or len(sys.argv) > 14:
        print("Spiel erstellen: meinskript.py -newround [-roundfile rundendatei.txt -xaxis INT -yaxis INT -maxplayers INT] -wordfile wordfile.txt -playername NAME")
        print("Spiel beitreten: meinskript.py -joinround [-roundfile rundendatei.txt] -spielername NAME")
        print("Hinweis: Die Argumente in Klammern sind optional und müssen nicht angegeben werden!")
        sys.exit(1)
    #Spiel erstellen
    if sys.argv[1] == "-newround":
        #Alle Argumente durchgehen und die Standardwerte austauschen
        config = parse_args(sys.argv)
        #Wenn die Pflichtangaben vorhanden sind erstelle roundfile und initialisiere Start
        if config["wordfile"] and config["playername"]:
            #config lädt die Werte der config (Pflichtangaben + optional überschriebene Standardwerte)
            words = load_words(config["wordfile"], config["roundfile"], config["xaxis"], config["yaxis"])


            create_roundfile(config["roundfile"], config["xaxis"], config["yaxis"], config["maxplayers"], config["playername"], config["wordfile"])
            host_start(config["maxplayers"], config["roundfile"], config["xaxis"], config["yaxis"], config["wordfile"],config["playername"], words)
        else:
            #Falls wordfile und playername (Pflichtfelder) ausgelassen wurden:
            print("Fehlende Argumente für -newround -wordfile und -playername sind erforderlich.")
    #Spiel beitreten
    elif sys.argv[1] == "-joinround":
        #Standardwert für roundfile, playername Pflichtangabe
        config = {
            "roundfile": "rundendatei.txt",
            "playername": None,
        }
        #Wenn vorhanden: extrahiere den roundfile Pfad
        if len(sys.argv) >= 4 and sys.argv[2] == "-roundfile":
            #Standardwert überschreiben
            config["roundfile"] = sys.argv[3]
            #Falls roundfile mit angegeben, extrahiere playername String
            if len(sys.argv) == 6 and sys.argv[4] == "-playername":
                config["playername"] = sys.argv[5]
        #Falls roundfile Standardwert extrahiere playername String
        elif len(sys.argv) == 4 and sys.argv[2] == "-playername":
            config["playername"] = sys.argv[3]
        #Falls playername not null
        if config["playername"]:
            #überprüfe ob roundfile existiert
            if os.path.exists(config["roundfile"]):
                #extrahiere den vom Host gesetzten Wert für maxplayer
                mplayer = getmaxplayer(config["roundfile"])
                #Überprüfung ob das Spiel voll ist
                if getplayer(config["roundfile"]) < mplayer:
                    #Aktuelle Spielerzahl um 1 erhöhen sowie spielername + PID + spielernummer eintragen
                    playernumber = incplayer(config["roundfile"], config["playername"])
                    print("Ich bin Spieler Nummer: " + str(playernumber))
                    #Beitritt für Spieler 3+
                    if playernumber != 2:
                        player_start(False, playernumber, config["roundfile"], mplayer, getyachse(config["roundfile"]), getxachse(config["roundfile"]), getwordfile(config["roundfile"]))
                    #Beitritt für Spieler 2
                    else:
                        player_start(True, playernumber, config["roundfile"], mplayer, getxachse(config["roundfile"]), getyachse(config["roundfile"]), getwordfile(config["roundfile"]))
                #Meldung wenn Spiel voll:
                else:
                    print("Maximale Spieleranzahl erreicht. Beitritt abgebrochen")
            #Meldung wenn roundfile nicht existent
            else:
                print("Beitritt nicht möglich! Die angegebene Rundendatei existiert nicht")
        #Meldung wenn Argumente fehlen
        else:
            print("Fehlende Argumente für -joinround -playername NAME ist erforderlich.")
    else:
        print("Unbekannter Befehl")
        sys.exit(1)