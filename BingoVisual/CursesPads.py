import curses
from curses import wrapper
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)

    # Ein neues Pad erstellen
    pad = curses.newpad(100, 100)
    stdscr.refresh()
    # Das Pad mit grünem Hintergrund füllen
    for i in range(100):
        for j in range(26):
            pad.addstr(str(j), green_black)
    # Das Pad auf den Bildschirm zeichnen
    pad.refresh(0, 0, 5, 5, 20, 25)

    # Warten auf eine Taste, bevor das Programm endet
    stdscr.getch()


# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
