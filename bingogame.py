import sys
import posix_ipc
import time
import os



def host_start():
    # Erstellen der Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)

    print("\nHost gestartet. Warte auf Client...")

    # Warten auf Nachricht vom Client
    message, _ = mq.receive()
    print(f"Nachricht vom Client erhalten: {message.decode()}")

    # Nachricht "Hallo Welt" ausgeben


    # Überprüfen, ob eine Nachricht vom anderen Spieler empfangen wurde
    #if message:
        # Starte das Rätselspiel, nachdem eine Nachricht empfangen wurde
        #ratespiel(True, mq)

    # Message Queue schließen
    mq.close()



def player_start(second, playernumber, roundfile):
    # Öffnen der existierenden Message Queue
    if second:
        mq_name = "/my_message_queue"
        mq = posix_ipc.MessageQueue(mq_name)
        # Nachricht an den Host senden
        playername = getplayername(roundfile, playernumber)
        message = "Spieler2 ist beigetreten: " + playername
        mq.send(message.encode())
        mq.close()

        

def client_start2():
    # Öffnen der existierenden Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name)

    # Nachricht an den Host senden
    message = "Client gestartet"
    mq.send(message.encode())

    # Starte das Rätselspiel
    #ratespiel(False, mq)

    # Message Queue schließen
    mq.close()

def check_for_message(mq):
    try:
        message, _ = mq.receive(timeout=0)  # Versuche, eine Nachricht zu empfangen
        return message.decode()  # Nachricht vorhanden, gebe sie zurück
    except posix_ipc.BusyError:
        return None  # Keine Nachricht vorhanden

def ratespiel(is_host, mq):
    zahl = 5
    print("Versuche Zahl 1-10 zu erraten:")

    while True:
        message = check_for_message(mq)

        if message:
            print(message + " hat gewonnen, Spiel ist vorbei!")
            break
        else:
            eingabe = input("Tipp:")


            message2 = check_for_message(mq)

            if message2:
                print(message2 + " hat gewonnen, Spiel ist vorbei!")
                break
            else:
                try:
                    zahl2 = int(eingabe)
                    if zahl == zahl2:
                        print("Erraten!")
                        if is_host:
                             mq.send("Hostgewonnen".encode())
                             break
                        else:
                            mq.send("Clientgewonnen".encode())
                            break
                except ValueError:
                    print("Eingabe fehlerhaft, versuche es erneut!")

def is_integer(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

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

def getmaxplayer(rundendatei):
    """Return INT Maxplayer"""
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("maxplayer:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading max players from {rundendatei}: {e}")
        return None

def getplayername(rundendatei, player_count):
    """Return STRING player"""
    try:
        with open(rundendatei, 'r') as f:
            playerstring = "playername" + str(player_count)
            for line in f:
                if line.startswith(playerstring):
                    return str(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading  playername from {rundendatei}: {e}")
        return None
def getplayer(rundendatei):
    """Return INT player"""
    try:
        with open(rundendatei, 'r') as f:
            for line in f:
                if line.startswith("players:"):
                    return int(line.split(":")[1].strip())
    except Exception as e:
        print(f"Error reading  players from {rundendatei}: {e}")
        return None


def incplayer(rundendatei, spielername):
    """Increment the player count in the given file and append player's name."""
    try:
        # Lese den aktuellen Spielerzähler
        with open(rundendatei, 'r') as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            if line.startswith("players:"):
                player_count = int(line.split(":")[1].strip())
                player_count += 1
                lines[i] = f"players: {player_count}\n"
                break
        playerstring = "playername" + str(player_count)

        # Füge den Spielername und den Spielername + Spielerzahl hinzu
        lines.append(f"{playerstring}: {spielername}\n")

        # Schreibe den neuen Inhalt zurück in die Datei
        with open(rundendatei, 'w') as f:
            f.writelines(lines)
        return player_count
    except Exception as e:
        print(f"Error updating players in {rundendatei}: {e}")
def create_roundfile(rundendatei, xachse, yachse, maxspieler, hostname): #Upload.
    """Erstellt eine Datei mit Rundendetails."""
    try:
        with open(rundendatei, 'w') as f:
            f.write(f"maxplayer: {maxspieler}\n")
            f.write(f"height: {yachse}\n")
            f.write(f"width: {xachse}\n")
            f.write(f"players: {1}\n")
            f.write(f"playername1: {hostname}\n")
        print("Roundfile created, initializing game start...")
        ################ Animation #################
        print("loading")
        animation = ["[#"        "]10%", "[##"       "]20%", "[###"      "]30%", "[####"     "]40%", "[#####"    "]50%",
                     "[######"    "]60%", "[#######"  "]70%", "[########"  "]80%", "[#########" "]90%",
                     "[##########]100%"]
        for i in range(len(animation)):
            time.sleep(0.6)
            sys.stdout.write("\r" + animation[i % len(animation)])
        ################ Animation #################
    except Exception as e:
        print("Error creating round file:", e)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: meinskript.py -newround | -joinround")
        sys.exit(1)

    if sys.argv[1] == "-newround":
        if len(sys.argv) != 14:
            print("Falsche Eingabe für die Argumente von -newround")
            print("Nutzung: -newround -roundfile rundenDATEI.txt -xaxis INT -yaxis INT -wordfile wortDATEI.txt -maxplayers INT -playername NAME")
            sys.exit(1)

        if (sys.argv[2] == "-roundfile" and
                sys.argv[4] == "-xaxis" and
                sys.argv[6] == "-yaxis" and
                sys.argv[8] == "-wordfile" and
                sys.argv[10] == "-maxplayers" and
                sys.argv[12] == "-playername" and
                is_integer(sys.argv[5]) and
                is_integer(sys.argv[7]) and
                is_integer(sys.argv[11])):

            create_roundfile(sys.argv[3], sys.argv[5], sys.argv[7], sys.argv[11], sys.argv[13])
            host_start()
        else:
            print("Falsche Argumente für -newround!")

    elif sys.argv[1] == "-joinround":
        if len(sys.argv) != 6:
            print("Falsche Eingabe für die Argumente von -joinround")
            print("Nutzung: -joinround -roundfile DATA.txt -playername NAME")
            sys.exit(1)


        if (os.path.exists(sys.argv[3])):
            if (getplayer(sys.argv[3]) < getmaxplayer(sys.argv[3])):
                playernumber = incplayer(sys.argv[3], sys.argv[5])
                print("Ich bin Spieler Nummer: " + str(playernumber))
                if playernumber != 2:
                    player_start(False,playernumber, sys.argv[3])
                else:
                    player_start(True, playernumber, sys.argv[3])
            else:
                print("Maximale Spieleranzahl erreicht. Beitritt abgebrochen")
        else:
            print("Beitritt nicht möglich! Die angegebene Rundendatei existiert nicht")

    else:
        print("Unbekannter Befehl")
        sys.exit(1)




