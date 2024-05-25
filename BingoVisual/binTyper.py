import typer
import random
import os

app = typer.Typer()


def load_words(file_path: str) -> list:
    """
    Load words from a given file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found")

    with open(file_path, 'r') as file:
        words = [line.strip() for line in file.readlines()]

    if len(words) < 25:
        raise ValueError("Not enough words in the file to fill the Bingo card")

    return words


def generate_bingo_card(xaxis: int, yaxis: int, words: list) -> str:
    bingo_card = random.sample(words, xaxis * yaxis)

    # Format the card as a string
    card_str = "+" + "+".join(["----"] * xaxis) + "+\n"
    for i in range(yaxis):
        row = "|"
        for j in range(xaxis):
            cell = bingo_card[i * xaxis + j]
            row += f" {cell[:4]:<4} |"  # Adjust cell width to 4 characters for alignment
        card_str += row + "\n"
        card_str += "+" + "+".join(["----"] * xaxis) + "+\n"

    return card_str


@app.command()
def show_bingo_card(xaxis: int = typer.Option(5, "--xaxis", "-x", help="Number of columns"),
                    yaxis: int = typer.Option(5, "--yaxis", "-y", help="Number of rows"),
                    wordfile: str = typer.Option("Wordfile.txt", "--wordfile", "-w", help="Path to the word file")):
    """
    Show a bingo card with the given number of rows (yaxis) and columns (xaxis).
    """
    words = load_words(wordfile)
    card = generate_bingo_card(xaxis, yaxis, words)
    typer.echo(card)


if __name__ == "__main__":
    app()
