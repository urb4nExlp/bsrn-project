import sys
import posix_ipc

def host_start():
    # Erstellen der Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name, posix_ipc.O_CREAT)

    print("Host gestartet. Warte auf Client...")

    # Warten auf Nachricht vom Client
    message, _ = mq.receive()
    print(f"Nachricht vom Client erhalten: {message.decode()}")

    # Nachricht "Hallo Welt" ausgeben
    print("Hallo Welt")

    # Message Queue schließen
    mq.close()
    posix_ipc.unlink_shared_memory(mq_name)

def client_start():
    # Öffnen der existierenden Message Queue
    mq_name = "/my_message_queue"
    mq = posix_ipc.MessageQueue(mq_name)

    # Nachricht an den Host senden
    message = "Client gestartet"
    mq.send(message.encode())

    # Message Queue schließen
    mq.close()

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
