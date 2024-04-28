#kleiner Bingo Code zum Herumspielen
import random

class Bingo:
    def __init__(self, players):
        self.players = players
        self.cards = {player: self.generate_card() for player in players}
        self.called_numbers = set()

    def generate_card(self):
        card = []
        for _ in range(5):
            row = random.sample(range(1, 11), 5)
            card.append(row)
        return card

    def display_card(self, player):
        print(f"\nBingo card for Player {player}:")
        card = self.cards[player]
        for row in card:
            print(row)

    def call_number(self):
        number = random.randint(1, 10)
        self.called_numbers.add(number)
        print(f"\nCalled number: {number}")

    def check_card(self, player):
        card = self.cards[player]
        for row in card:
            if all(num in self.called_numbers for num in row):
                return True
        return False

    def play(self):
        while True:
            self.call_number()
            for player in self.players:
                self.display_card(player)
                if self.check_card(player):
                    print(f"\nPlayer {player} wins!")
                    return

# Beispiel: Spiel mit zwei Spielern
players = ["Robal", "Bemie"]
bingo_game = Bingo(players)
bingo_game.play()
