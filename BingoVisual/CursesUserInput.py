import curses
from curses import wrapper
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)
    stdscr.nodelay(True)

    x, y = 0, 0
    while True:
        try:
            key = stdscr.getkey()
        except:
            key = None
        if key == "KEY_LEFT":
            x -= 1
        elif key == "KEY_RIGHT":
            x += 1
        elif key == "KEY-UP":
            y -= 1
        elif key == "KEY-DOWN":
            y += 1

        stdscr.clear()
        stdscr.addstr(y, x, "0")
        stdscr.refresh()


# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
