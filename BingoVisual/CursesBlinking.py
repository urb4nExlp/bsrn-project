import curses
from curses import wrapper
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)

    for i in range(10):
        stdscr.clear()
        color = green_black
        if i % 2 == 0:
            color = red_white | curses.A_REVERSE
        stdscr.addstr(i, 0, str(i), color)
        stdscr.refresh()
        time.sleep(0.5)
    
    stdscr.getch()


# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
