import curses
from curses import wrapper
from curses.textpad import Textbox, rectangle
import time  # Das time-Modul importieren


def main(stdscr):
    # Farbpaare initialisieren
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_YELLOW)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    blue_yellow = curses.color_pair(1)
    red_white = curses.color_pair(2)
    curses.echo()

    stdscr.attron(red_white)
    stdscr.border()
    stdscr.attroff(red_white)

    stdscr.attron(blue_yellow)
    rectangle(stdscr, 1,1, 5, 20)
    stdscr.attroff(blue_yellow)
    stdscr.addstr(5, 30, "press q to finish, alles geschriebene wird aufgeschrieben")

    stdscr.move(10,20)

    stdscr.refresh()

    while True:
        key = stdscr.getkey()
        if key == "q":
            break

# Die main-Funktion innerhalb des curses-Wrapper ausführen
wrapper(main)
