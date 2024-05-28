import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)

    win = curses.newwin(3, 18, 2, 2)
    box = Textbox(win)
    rectangle(stdscr, 1,1, 5, 20)

    stdscr.refresh()

    box.edit()
    text = box.gather().strip().replace('\n', ' ')

    stdscr.addstr(10,40, text)

    stdscr.getch()


# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
