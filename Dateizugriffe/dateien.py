def create_roundfile(rundendatei, xachse, yachse, maxspieler): #Upload.
    """Erstellt eine Datei mit Rundendetails."""
    try:
        with open(rundendatei, 'w') as f:
            f.write(f"MaxPlayer: {maxspieler}\n")
            f.write(f"Height: {yachse}\n")
            f.write(f"Width: {xachse}\n")
            f.write(f"Players: {1}\n")
        print("Round file created successfully.")
    except Exception as e:
        print("Error creating round file:", e)


def getrundendatei():
    """Return STRING der rundendatei"""
    try:
        # Beispiel-Implementierung, um die Rundendatei zurückzugeben
        # Passen Sie dies entsprechend an, wie Sie die Rundendatei speichern/verwenden
        return "roundfile.txt"
    except Exception as e:
        print("Error getting round file:", e)
        return None


def getxachse(rundendatei):
    """Return INT der X Achse"""
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("Width:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading x-axis from {rundendatei}: {e}")
        return None


def getyachse(rundendatei):
    """Return INT der Y Achse"""
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("Height:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading y-axis from {rundendatei}: {e}")
        return None


def getspielerzahl(rundendatei):
    """Return INT Maxplayer"""
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("Max:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading max players from {rundendatei}: {e}")
        return None

create_roundfile("testdatei.txt", 5 , 5, 3)