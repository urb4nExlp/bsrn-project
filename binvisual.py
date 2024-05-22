import random
import curses
from curses import textpad

def load_words(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file]
    return words

def create_bingo_card(words, xaxis, yaxis):
    random.shuffle(words)
    return [words[i*yaxis:(i+1)*yaxis] for i in range(xaxis)]

def draw_card(stdscr, card, marked, xaxis, yaxis):
    stdscr.clear()
    for i, row in enumerate(card):
        for j, word in enumerate(row):
            x, y = 2 + j * 12, 2 + i * 2
            if (i, j) in marked:
                stdscr.addstr(y, x, "X".center(12), curses.A_REVERSE)
            else:
                stdscr.addstr(y, x, word.center(12))
    stdscr.refresh()

def check_bingo(marked, xaxis, yaxis):
    # Check rows
    for i in range(xaxis):
        if all((i, j) in marked for j in range(yaxis)):
            return True
    # Check columns
    for j in range(yaxis):
        if all((i, j) in marked for i in range(xaxis)):
            return True
    # Check diagonals
    if all((i, i) in marked for i in range(xaxis)):
        return True
    if all((i, yaxis - 1 - i) in marked for i in range(xaxis)):
        return True
    return False

def main(stdscr, xaxis, yaxis, words):
    card = create_bingo_card(words, xaxis, yaxis)
    marked = set()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)

    draw_card(stdscr, card, marked, xaxis, yaxis)

    while True:
        key = stdscr.getch()
        if key == ord('x'):
            break
        if key == curses.KEY_MOUSE:
            _, mx, my, _, _ = curses.getmouse()
            col = (mx - 2) // 12
            row = (my - 2) // 2
            if 0 <= row < xaxis and 0 <= col < yaxis:
                if (row, col) in marked:
                    marked.remove((row, col))
                else:
                    marked.add((row, col))
                draw_card(stdscr, card, marked, xaxis, yaxis)
                if check_bingo(marked, xaxis, yaxis):
                    stdscr.addstr(2 + xaxis * 2, 2, "BINGO! Du hast gewonnen!".center(12 * yaxis))
                    stdscr.refresh()
                    stdscr.getch()
                    break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Bingo-Spiel")
    parser.add_argument('-xaxis', type=int, default=5, help='Anzahl der Felder in der Breite')
    parser.add_argument('-yaxis', type=int, default=5, help='Anzahl der Felder in der Höhe')
    parser.add_argument('-wordfile', type=str, default='wordfile.txt', help='Pfad zur Datei mit den Wörtern')
    args = parser.parse_args()

    words = load_words(args.wordfile)
    if len(words) < args.xaxis * args.yaxis:
        raise ValueError("Nicht genügend Wörter in der Datei, um die Bingo-Karte zu füllen.")

    curses.wrapper(main, args.xaxis, args.yaxis, words)
