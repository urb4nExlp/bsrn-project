import random

class BingoCard:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.card = self.create_card()

    def create_card(self):
        card = []
        for _ in range(self.rows):
            column = random.sample(range(1, self.cols + 1), self.cols)
            card.append(column)
        return card

    def __str__(self):
        card_str = ""
        for row in self.card:
            card_str += " ".join(f"{cell:2}" for cell in row) + "\n"
        return card_str

def main():
    try:
        rows = int(input("Geben Sie die Anzahl der Zeilen der Bingo-Karte ein: "))
        cols = int(input("Geben Sie die Anzahl der Spalten der Bingo-Karte ein: "))
        if rows <= 0 or cols <= 0:
            raise ValueError("Die Anzahl der Zeilen und Spalten muss größer als Null sein.")

        bingo_card = BingoCard(rows, cols)
        print("Hier ist Ihre Bingo-Karte:")
        print(bingo_card)

    except ValueError as e:
        print("Fehler:", e)

if __name__ == "__main__":
    main()

