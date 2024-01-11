def lire_fichier_ics(chemin_fichier):
    with open(chemin_fichier, 'r', encoding='utf-8') as fichier:
        lignes = fichier.readlines()
    return lignes

def extraire_informations(lignes):
    informations = []
    evenement_en_cours = {}

    for ligne in lignes:
        if ligne.startswith('BEGIN:VEVENT'):
            evenement_en_cours = {}
        elif ligne.startswith('END:VEVENT'):
            informations.append(evenement_en_cours)
        else:
            champs = ligne.strip().split(':')
            if len(champs) == 2:
                cle, valeur = champs
                evenement_en_cours[cle] = valeur

    return informations

def afficher_informations(informations):
    for evenement in informations:
        ligne_formattee = ";".join([f"{cle}:{valeur}" for cle, valeur in evenement.items()])
        print(ligne_formattee)
        print("-" * 30)

if __name__ == "__main__":
    chemin_dossier = r"C:\Users\arsen\OneDrive\Bureau"
    fichier_ics = "evenementSAE_15.ics"
    chemin_complet = f"{chemin_dossier}\\{fichier_ics}"

    lignes_fichier = lire_fichier_ics(chemin_complet)
    evenements = extraire_informations(lignes_fichier)
    afficher_informations(evenements)
