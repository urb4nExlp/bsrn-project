def createlogfile(Pid):
   # Erstellt eine neue Logdatei für den angegebenen Spieler.
    logfile_name = f"{Pid}_log.txt"
    with open(logfile_name, 'w') as logfile:
        logfile.write(f"Logdatei für Spieler: {Pid}\n")
        logfile.write(f"{'-' * 30}\n")
    print(f"Die Logdatei '{logfile_name}' wurde erfolgreich erstellt.")

def addtolog(Pid, eintrag):
    #Fügt einen neuen Eintrag zur Logdatei des angegebenen Spielers hinzu.
 logfile_name = f"{Pid}_log.txt"
if os.path.exists(logfile_name):
    with open(logfile_name, 'a') as logfile:
        logfile.write(f"{eintrag}\n")
    print(f"Der Eintrag '{eintrag}'  wurde zur Logdatei '{logfile_name}' hinzugefügt.")
else:
    print(f"Die Logdatei '{logfile_name}' existiert nicht. Bitte erst die Logdatei mit createlogfile erstellen.")

    # Ende 