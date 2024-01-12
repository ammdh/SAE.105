import re

def lire_fichier_ics(chemin_fichier, nom_fichier):
    chemin_complet = fr"{chemin_fichier}\{nom_fichier}"
    with open(chemin_complet, 'r', encoding='utf-8') as fichier:
        contenu = fichier.read()
    return contenu

def extraire_info_activite(contenu_ics):
    debut_evenement = re.search(r'BEGIN:VEVENT', contenu_ics)
    fin_evenement = re.search(r'END:VEVENT', contenu_ics)
    
    if debut_evenement and fin_evenement:
        activite = contenu_ics[debut_evenement.end():fin_evenement.start()]
        return activite
    else:
        return None

def afficher_info_ligne_par_ligne(activite_ics):
    champs = ['BEGIN', 'DTSTAMP', 'DTSTART', 'DTEND', 'SUMMARY', 'LOCATION', 'DESCRIPTION', 'UID', 'CREATED', 'LAST-MODIFIED', 'SEQUENCE', 'END']
    
    for champ in champs:
        match = re.search(fr'{champ}:(.*?)(?=\n[A-Z]+:|$)', activite_ics)
        if match:
            print(f"{champ} : {match.group(1).strip()}")
        else:
            print(f"{champ} : Non trouvé")

if __name__ == "__main__":
    chemin_fichier = r'C:\Users\arsen\OneDrive\Bureau'
    nom_fichier_ics = 'evenementSAE_15.ics'
    
    contenu_ics = lire_fichier_ics(chemin_fichier, nom_fichier_ics)

    activite_ics = extraire_info_activite(contenu_ics)

    if activite_ics:
        afficher_info_ligne_par_ligne(activite_ics)
    else:
        print("Aucune activité trouvée dans le fichier ICS.")

