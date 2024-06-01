def createlogfile(spielername):
   # Erstellt eine neue Logdatei für den angegebenen Spieler.
    logfile_name = f"{spielername}_log.txt"
    with open(logfile_name, 'w') as logfile:
        logfile.write(f"Logdatei für Spieler: {spielername}\n")
        logfile.write(f"{'-' * 30}\n")
    print(f"Die Logdatei '{logfile_name}' wurde erfolgreich erstellt.")

def addtolog(spielername, eintrag):
    #Fügt einen neuen Eintrag zur Logdatei des angegebenen Spielers hinzu.
 logfile_name = f"{spielername}_log.txt"
if os.path.exists(logfile_name):
    with open(logfile_name, 'a') as logfile:
        logfile.write(f"{eintrag}\n")
    print(f"Der Eintrag '{eintrag}'  wurde zur Logdatei '{logfile_name}' hinzugefügt.")
else:
    print(f"Die Logdatei '{logfile_name}' existiert nicht. Bitte erst die Logdatei mit createlogfile erstellen.")

    #.