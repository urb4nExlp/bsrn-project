import random

class BingoCard:
    def __init__(self):
        self.card = self.generate_card()
        self.marked_numbers = set()

    def generate_card(self):
        card = []
        for _ in range(5):
            column = random.sample(range(1, 16), 5)
            card.append(column)
        card[2][2] = "X"  # Free space
        return card

    def mark_number(self, number):
        for i in range(5):
            for j in range(5):
                if self.card[i][j] == number:
                    self.marked_numbers.add((i, j))
                    return True
        return False

    def check_win(self):
        # Check rows, columns, and diagonals for a win
        for i in range(5):
            if all((i, j) in self.marked_numbers for j in range(5)):
                return True
        for j in range(5):
            if all((i, j) in self.marked_numbers for i in range(5)):
                return True
        if all((i, i) in self.marked_numbers for i in range(5)) or \
           all((i, 4 - i) in self.marked_numbers for i in range(5)):
            return True
        return False

    def print_card(self):
        for row in self.card:
            print(" | ".join(str(num).rjust(2) for num in row))
            print("-" * 25)

# Beispielverwendung
bingo = BingoCard()
bingo.print_card()

while True:
    number = int(input("Bitte geben Sie eine Zahl ein (1-25), oder 0 zum Beenden: "))
    if number == 0:
        break
    if bingo.mark_number(number):
        print("Nummer markiert!")
        bingo.print_card()
        if bingo.check_win():
            print("Bingo! Sie haben gewonnen!")
            break
    else:
        print("Diese Zahl ist nicht auf Ihrer Karte.")