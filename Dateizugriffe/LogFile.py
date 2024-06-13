import os
from datetime import datetime

def erstelle_logdatei(spieler_nummer):
    # Erstellt eine neue Logdatei für den angegebenen Spieler im erforderlichen Format
    jetzt = datetime.now()
    logdatei_name = jetzt.strftime("%Y-%m-%d-%H-%M-%S") + f"-bingo-{spieler_nummer}.txt"
    with open(logdatei_name, 'w') as logdatei:
        logdatei.write(f"Logdatei für Spieler: {spieler_nummer}\n")
        logdatei.write(f"{'-' * 30}\n")
    print(f"Die Logdatei '{logdatei_name}' wurde erfolgreich erstellt.")
    return logdatei_name

def hinzufuegen_zur_log(logdatei_name, eintrag):
    # Fügt einen neuen Eintrag zur angegebenen Logdatei hinzu
    if os.path.exists(logdatei_name):
        with open(logdatei_name, 'a') as logdatei:
            logdatei.write(f"{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')} {eintrag}\n")
        print(f"Der Eintrag '{eintrag}' wurde zur Logdatei '{logdatei_name}' hinzugefügt.")
    else:
        print(f"Die Logdatei '{logdatei_name}' existiert nicht. Bitte erst die Logdatei mit erstelle_logdatei erstellen.")
