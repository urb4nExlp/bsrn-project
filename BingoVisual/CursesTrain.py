import curses
from curses import wrapper

def main(stdscr):
    stdscr.clear()
    stdscr.addstr(3, 1, "Welcome to BingoVisual", curses.A_BOLD)
    stdscr.addstr(3, 30, "press x to finish")
    stdscr.refresh()
    while True:
        key = stdscr.getch()
        if key == ord('x'):
            break

wrapper(main)