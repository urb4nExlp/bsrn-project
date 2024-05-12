import sys
import posix_ipc
import random
import threading
import time


class BingoGame:
    def __init__(self):
        pass

    def start_host(self):
        # Erstellen der Message Queue
        mq_name = "/my_message_queue"
        mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)

        print("Host gestartet. Warte auf Client...")

        # Thread starten, um auf Nachrichten zu warten
        threading.Thread(target=self.wait_for_message, args=(mq,)).start()

    def wait_for_message(self, mq):
        # Warten auf Nachricht vom Client (nicht-blockierend)
        while True:
            try:
                message, _ = mq.receive(block=False)
                print(f"Nachricht vom Client erhalten: {message.decode()}")
                break
            except posix_ipc.BusyError:
                time.sleep(1)  # Kurze Pause, um CPU-Last zu reduzieren

        # Nachricht "Hallo Welt" ausgeben
        print("Hallo Welt")

        # Message Queue schließen
        mq.close()


    def win_client(self):
        # Öffnen der existierenden Message Queue
        mq_name = "/my_message_queue"
        mq = posix_ipc.MessageQueue(mq_name)

        # Nachricht an den Host senden
        message = "Client gestartet"
        mq.send(message.encode())

        # Message Queue schließen
        mq.close()


def ratespiel():
    zahl = 5
    print("Versuche Zahl 1-10 zu erraten:")

    while True:
        eingabe = input("Tipp:")
        zahl2 = int(eingabe)
        if zahl == zahl2:
            print("Erraten!")
            bingogame.win_client()
            break
        else:
            print("Versuche es nochmal!")


def create_round_file(filename):
    # open öffnet die Datei im 'w' Schreibmodus, ist keine Datei vorhanden wird sie erstellt
    with open(filename, 'w') as file:
        pass


bingogame = BingoGame()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: meinskript.py -newround | -joinround | -roundfile rundendatei.txt")
        sys.exit(1)

    if sys.argv[1] == "-newround":
        bingogame.start_host()
    elif sys.argv[1] == "-joinround":
        ratespiel()
    elif sys.argv[1] == "-roundfile":
        if len(sys.argv) != 3:
            print("Usage: meinskript.py -roundfile rundendatei.txt")
            sys.exit(1)
        create_round_file(sys.argv[2])
        print("Rundendatei wurde erfolgreich erstellt:", sys.argv[2])
    else:
        print("Unbekannter Befehl")
        sys.exit(1)
