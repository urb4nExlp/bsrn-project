import random
import curses
import asyncio
from asyncio import Queue
from textual.app import App, ComposeResult
from textual.widgets import Button
from textual.containers import Grid

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
    for i in range(xaxis):
        if all((i, j) in marked for j in range(yaxis)):
            return True
    for j in range(yaxis):
        if all((i, j) in marked for i in range(xaxis)):
            return True
    if all((i, i) in marked for i in range(xaxis)):
        return True
    if all((i, yaxis - 1 - i) in marked for i in range(xaxis)):
        return True
    return False

async def main_curses(stdscr, xaxis, yaxis, words, queue):
    card = create_bingo_card(words, xaxis, yaxis)
    marked = set()
    curses.mousemask(curses.ALL_MOUSE_EVENTS | curses.REPORT_MOUSE_POSITION)
    curses.curs_set(0)

    draw_card(stdscr, card, marked, xaxis, yaxis)
    await queue.put(marked)

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
                await queue.put(marked)
                if check_bingo(marked, xaxis, yaxis):
                    stdscr.addstr(2 + xaxis * 2, 2, "BINGO! Du hast gewonnen!".center(12 * yaxis))
                    stdscr.refresh()
                    stdscr.getch()
                    break

class BingoCard(Grid):
    def __init__(self, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card = card
        self.marked = set()
        self.generate_grid()

    def generate_grid(self):
        self.columns = len(self.card[0])
        self.rows = len(self.card)
        for row in range(self.rows):
            for col in range(self.columns):
                word = self.card[row][col]
                button = Button(label=word, name=f"{row},{col}")
                self.add(button)

    def update_marked(self, marked):
        self.marked = marked
        for row in range(self.rows):
            for col in range(self.columns):
                button = self.query_one(f"Button[name='{row},{col}']")
                if (row, col) in self.marked:
                    button.label = "X"
                else:
                    button.label = self.card[row][col]

class BingoApp(App):
    def __init__(self, card, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.card = card
        self.bingo_card = None

    def compose(self) -> ComposeResult:
        self.bingo_card = BingoCard(self.card)
        yield self.bingo_card

    async def update_card(self, marked):
        self.bingo_card.update_marked(marked)

async def run_textual(card, queue):
    app = BingoApp(card)
    asyncio.create_task(app.run_async())

    while True:
        marked = await queue.get()
        await app.update_card(marked)

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

    queue = Queue()
    asyncio.run(run_textual(create_bingo_card(words, args.xaxis, args.yaxis), queue))
    curses.wrapper(main_curses, args.xaxis, args.yaxis, words, queue)
