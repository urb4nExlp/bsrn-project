import time
import sys

def loading_animation(duration):
    # Zeichen für die Animation
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    bar_length = 30  # Länge des Ladebalkens

    # ASCII-Farbcodes
    colors = [
        "\033[91m",  # Rot
        "\033[92m",  # Grün
        "\033[93m",  # Gelb
        "\033[94m",  # Blau
        "\033[95m",  # Magenta
        "\033[96m",  # Cyan
        "\033[97m",  # Weiß
    ]
    reset_color = "\033[0m"

    # Endzeit berechnen
    end_time = time.time() + duration
    start_time = time.time()
    idx = 0

    while time.time() < end_time:
        # Berechne den Fortschritt
        elapsed_time = time.time() - start_time
        progress = elapsed_time / duration
        filled_length = int(bar_length * progress)

        # Ladebalken und Animation
        bar = '#' * filled_length + '-' * (bar_length - filled_length)
        char = animation[idx % len(animation)]

        # Wähle eine Farbe basierend auf dem Fortschritt
        color = colors[idx % len(colors)]

        # Fortschrittsanzeige in die Konsole schreiben
        sys.stdout.write(f"\r{color}Lädt... [{bar}] {char}{reset_color}")
        sys.stdout.flush()

        # Warte ein wenig
        time.sleep(0.1)
        idx += 1

    # Animation beenden
    sys.stdout.write(f"\r{colors[-1]}Lädt... [##################################] Fertig!{reset_color}\n")

# Ladeanimation für 5 Sekunden anzeigen
loading_animation(5)
