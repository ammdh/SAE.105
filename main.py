from flask import Flask, render_template, request, send_file
import numpy as np
import os
from collections import Counter

app = Flask(__name__)

def process_file(file_content):
    ress = file_content.split('\n')
    tab_dest = np.array([])
    ssh_attempts = 0
    icmp_count = 0

    with open("test.csv", "w") as fic:
        evenement = "DATE;SOURCE;PORT;DESTINATION;FLAG;SEQ"
        fic.write(evenement + "\n")

        for event in ress:
            if event.startswith('11:42'):
                seq, heure1, nomip, port, flag = "", "", "", "", ""

                texte = event.split(" ")
                heure1 = texte[0]

                nomip1 = texte[2].split(".")
                nomip = ".".join(nomip1[:3])

                if nomip not in tab_dest:
                    tab_dest = np.append(tab_dest, nomip)

                port = texte[2].split(".")[-1]

                nomip2 = texte[4]

                texte_flag = event.split("[")
                if len(texte_flag) > 1:
                    flag = texte_flag[1].split("]")[0]

                    if port == "ssh" and flag == "S":
                        ssh_attempts += 1

                texte_seq = event.split(",")
                if len(texte_seq) > 1 and texte_seq[1].startswith(" seq"):
                    seq = texte_seq[1].split(" ")[2]

                evenement = f"{heure1};{nomip};{port};{nomip2};{flag};{seq}"
                fic.write(evenement + "\n")

                if "ICMP echo request" in event:
                    icmp_count += 1

    data = np.genfromtxt("test.csv", delimiter=';', skip_header=1, dtype=str)

    types_attaques = Counter(data[:, 4])
    nb_flags = Counter(data[:, 4])['S']
    taille_paquet = os.path.getsize("test.csv")
    adresses_ip_frequentes = Counter(data[:, 3]).most_common(10)

    with open("bilan.md", "w") as bilan_file:
        bilan_file.write(f"Type de flags:\n{types_attaques}\n\n")
        bilan_file.write(f"Nombre de flags de connexion [S]: {nb_flags}\n\n")
        bilan_file.write(f"Nombre de tentatives SSH de connexion: {ssh_attempts}\n")
        bilan_file.write(f"Nombre de pings ICMP: {icmp_count}\n")
        bilan_file.write(f"Taille du paquet (en octets): {taille_paquet}\n\n")
        bilan_file.write("Top 10 adresses IP les plus fréquentes:\n")
        for adresse, count in adresses_ip_frequentes:
            bilan_file.write(f"{adresse}: {count}\n")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "Aucun fichier n'a été téléchargé."

    file = request.files['file']
    if file.filename == '':
        return "Aucun fichier sélectionné."

    try:
        file_content = file.read().decode('utf-8')
        process_file(file_content)

        return send_file("bilan.md", as_attachment=True, download_name="bilan.md")

    except Exception as e:
        return f"Une erreur s'est produite: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
