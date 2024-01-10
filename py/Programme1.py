import icalendar
from datetime import datetime

def ics_event_to_csv(event):
    # Récupérer les informations pertinentes de l'événement
    summary = event.get('summary')
    start_time = event.get('dtstart').dt
    end_time = event.get('dtend').dt

    # Convertir les dates au format ISO 8601
    start_time_iso = start_time.isoformat()
    end_time_iso = end_time.isoformat()

    # Créer une ligne CSV
    csv_line = f"{start_time_iso},{end_time_iso},{summary}"

    return csv_line

def ics_to_csv(file_path):
    # Ouvrir le fichier .ics
    with open(file_path, 'rb') as file:
        # Charger le contenu du fichier .ics
        cal_data = file.read()

        # Analyser le fichier .ics
        cal = icalendar.Calendar.from_ical(cal_data)

        # Récupérer les événements
        events = cal.walk('vevent')

        # Créer une liste pour stocker les lignes CSV
        csv_data = []

        # Parcourir chaque événement et convertir en CSV
        for event in events:
            csv_line = ics_event_to_csv(event)
            csv_data.append(csv_line)

        return csv_data

def main():
    # Chemin vers le fichier .ics
    ics_file_path = 'chemin/vers/votre/fichier.ics'

    # Appeler la fonction pour convertir le fichier .ics en CSV
    csv_data = ics_to_csv(ics_file_path)

    # Afficher le résultat
    for line in csv_data:
        print(line)

if __name__ == "__main__":
    main()
