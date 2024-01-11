import csv

def get_ics_info(filename):
  """Récupère les informations d'un fichier ics.

  Args:
    filename: Le chemin du fichier ics.

  Returns:
    Une liste de listes, où chaque sous-liste contient les informations d'un événement.
  """

  with open(filename, "r") as f:
    lines = f.readlines()

  # Initialise la liste des informations.
  infos = []

  # Parcours le fichier ligne par ligne.
  for line in lines:
    # Ignore les lignes vides.
    if not line.strip():
      continue

    # Détermine le type d'information.
    if line.startswith("BEGIN"):
      info_type = line.split(":")[1]
    elif line.startswith("END"):
      info_type = line.split(":")[1]
    else:
      info_type = None

    # Ajoute l'information à la liste.
    if info_type is not None:
      infos.append([info_type] + line.split(";"))

  return infos


def main():
  """Programme principal."""

  # Le chemin du fichier ics.
  filename = "/Users/arsen/OneDrive/Bureau/evenementSAE_15.ics"

  # Récupère les informations du fichier.
  infos = get_ics_info(filename)

  # Affiche les informations.
  for info in infos:
    print(info)


if __name__ == "__main__":
  main()
