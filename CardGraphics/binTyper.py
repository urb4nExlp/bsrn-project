import typer
import random

app = typer.Typer()

def generate_bingo_card(xaxis: int, yaxis: int) -> str:
    bingo_card = []
    step = 75 // xaxis
    ranges = [(i * step + 1, (i + 1) * step) for i in range(xaxis)]

    for start, end in ranges:
        bingo_card.append(random.sample(range(start, end + 1), yaxis))

    # Format the card as a string
    card_str = "+" + "+".join(["----"] * xaxis) + "+\n"
    for i in range(yaxis):
        row = "|"
        for j in range(xaxis):
            cell = bingo_card[j][i]
            if isinstance(cell, int):
                cell = f"{cell:2}"
            row += f" {cell} |"
        card_str += row + "\n"
        card_str += "+" + "+".join(["----"] * xaxis) + "+\n"

    return card_str

@app.command()
def show_bingo_card(xaxis: int = 5, yaxis: int = 5):
    """
    Show a bingo card with the given number of rows (yaxis) and columns (xaxis).
    """
    card = generate_bingo_card(xaxis, yaxis)
    typer.echo(card)

if __name__ == "__main__":
    app()
