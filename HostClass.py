def create_bingo_game():
    print("Wilkommen beim Buzzword-Bingo-Spiel ")

# Call up the function

create_bingo_game()


# Enter the lap details: such as name of the lap, width and height of the map

round_name = input("Bitte geben Sie den Namen der Runde ein: ")
width = int(input("Bitte geben Sie die Breite der Bingo-Karte ein: "))
height = int(input("Bitte geben Sie die Höhe der Bingo-Karte ein: "))

#--------------------------------------------------------------------------------------------

# Enter the player name

player_name =  input("Bitte geben Sie Ihren Namen ein: ")

# Enter the World/Text File (Bingowords / File )

text_file_name = input("Bitte geben Sie den Pfad/Name der Text/Word Datei/File: ")

#--------------------------------------------------------------------------------------------

# Confirm the entries and create the game environment

print(f"\nSpielrunde '{round_name}' wird erstellt ...")
print(f"Erstelle eine {width}x{height} Bingo-Karte für Spieler {player_name} mit der Wortliste aus '{text_file_name}'.")

#Continue code .....

