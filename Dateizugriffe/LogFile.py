def createlogfile(spielername):
    """ Erstellt eine neue Logdatei für den angegebenen Spieler."""
    logfile_name = f"{spielername}_log.txt"
    with open(logfile_name, 'w') as logfile:
        