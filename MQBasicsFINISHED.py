import sys
import posix_ipc
import random


def host_start():
    # Erstellen der Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)

    print("Host gestartet. Warte auf Client...")

    # Warten auf Nachricht vom Client
    message, _ = mq.receive()
    print(f"Nachricht vom Client erhalten: {message.decode()}")

    # Nachricht "Hallo Welt" ausgeben


    # Überprüfen, ob eine Nachricht vom anderen Spieler empfangen wurde
    if message:
        # Starte das Rätselspiel, nachdem eine Nachricht empfangen wurde
        ratespiel(True, mq)

    # Message Queue schließen
    mq.close()



def client_start():
    # Öffnen der existierenden Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name)

    # Nachricht an den Host senden
    message = "Client gestartet"
    mq.send(message.encode())

    # Starte das Rätselspiel
    ratespiel(False, mq)

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


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: meinskript.py -hoststart | -clientstart")
        sys.exit(1)

    if sys.argv[1] == "-hoststart":
        host_start()
    elif sys.argv[1] == "-clientstart":
        client_start()
    else:
        print("Unbekannter Befehl")
        sys.exit(1)
