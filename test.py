import os
import subprocess

def host_process(pipe):
    print("Host-Prozess gestartet.")
    message = "Hallo, dies ist eine Nachricht vom Host-Prozess."
    pipe.stdin.write(message.encode())  # Nachricht an den Benutzerprozess senden
    pipe.stdin.close()  # Eingabe der Pipe schließen
    print("Nachricht an Benutzer gesendet.")
    pipe.wait()  # Warten, bis der Benutzerprozess beendet ist

def user_process():
    print("Benutzer-Prozess gestartet.")
    message = input("Warte auf Nachricht vom Host-Prozess: ")
    print("Nachricht vom Host erhalten:", message)

def main():
    parent_pipe, child_pipe = os.pipe()  # Anonyme Pipe erstellen

    pid = os.fork()  # Neuen Prozess erstellen

    if pid == 0:  # Kindprozess
        os.close(parent_pipe)  # Kindprozess schließt die nicht verwendete Endung der Pipe
        subprocess.Popen(['python', __file__, '--user'], stdin=child_pipe)  # Benutzerprozess starten
    else:  # Elternprozess
        os.close(child_pipe)  # Elternprozess schließt die nicht verwendete Endung der Pipe
        host_process(subprocess.Popen(['python', __file__, '--host'], stdin=parent_pipe))  # Hostprozess starten

if __name__ == "__main__":
    import sys
    if '--host' in sys.argv:
        host_process(sys.stdin)
    elif '--user' in sys.argv:
        user_process()
    else:
        main()