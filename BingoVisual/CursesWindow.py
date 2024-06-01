import curses
from curses import wrapper
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)

    #Ein neues Fenster erstellen
    win1 = curses.newwin(1, 20, 10, 10)
    # Text außerhalb des Fensters hinzufügen
    stdscr.addstr("nicht im Fenster")
    stdscr.refresh()

    # Schleife, um den Inhalt des Fensters zu aktualisieren
    for i in range(10):
         win1.clear()
         color = green_black
         if i % 2 == 0:
             color = red_white | curses.A_REVERSE
         win1.addstr(0, 0, f"{i+1}. Output", color)
         win1.refresh()
         time.sleep(0.5)

    # Warten auf eine Taste, bevor das Programm endet
    stdscr.getch()


# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
