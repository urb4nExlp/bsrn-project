import curses
from curses import wrapper

def main(stdscr):
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_WHITE)
    green_black = curses.color_pair(1)
    red_white = curses.color_pair(2)

    stdscr.clear()
    stdscr.addstr(3, 1, "Welcome to BingoVisual", curses.A_REVERSE)
    stdscr.addstr(3, 30, "press x to finish", red_white)
    stdscr.addstr(12, 30, "press x to finish", green_black)
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('x'):
            break

wrapper(main)