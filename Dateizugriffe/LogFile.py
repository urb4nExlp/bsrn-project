def createlogfile(spielername):
    """ Erstellt eine neue Logdatei für den angegebenen Spieler."""
    logfile_name = f"{spielername}_log.txt"
    with open(logfile_name, 'w') as logfile:
        logfile.write(f"Logdatei für Spieler: {spielername}\n")
        logfile.write(f"{'-' * 30}\n")
    print(f"Die Logdatei '{logfile_name}' wurde erfolgreich erstellt.")

def addtolog(spielername, eintrag):
