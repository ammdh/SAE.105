from flask import Flask, render_template, request, send_file, redirect 
import numpy as np
import os
from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import markdown
import webbrowser

app = Flask(__name__)

app = Flask(__name__, static_url_path='/static', static_folder='static')



def process_file(file_content):
    ress = file_content.split('\n')
    tab_dest = np.array([])
    ssh_attempts = 0
    icmp_count = 0

    with open("test.csv", "w") as fic:
        evenement = "DATE;SOURCE;PORT;DESTINATION;FLAG;SEQ"
        fic.write(evenement + "\n")

        for event in ress:
            if event.startswith('11:4'):
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

    analyze_dumpfile(file_content)

def analyze_dumpfile(file_content):
    file = file_content.split('\n')
    file = [line.rstrip() for line in file]

    tableau_evenement = []

    nb_bp_linux8 = 0
    nb_src_bp_linux8 = 0
    nb_dst_bp_linux8 = 0
    nb_paquet = 0
    nb_solunet = 0
    autre = 0
    nb_src_solunet = 0
    nb_dst_solunet = 0

    for line in file:
        if "IP" in line:
            nb_paquet += 1
            texts = line.split()
            time = texts[0]
            source = texts[2]
            destination = texts[4]
            evenement = {"heure": time, "ip source": source, "ip destinataire": destination}
            tableau_evenement.append(evenement)
            if 'BP-Linux' in source:
                nb_src_bp_linux8 += 1
            if 'BP-Linux' in destination:
                nb_dst_bp_linux8 += 1
            if 'solunet' in source:
                nb_src_solunet += 1
            if 'solunet' in destination:
                nb_dst_solunet += 1
            if 'BP-Linux' in line:
                nb_bp_linux8 += 1
            if 'solunet' in line:
                nb_solunet += 1
            if 'seq' in line:
                texts1 = line.split(',')
                if len(texts1) >= 8:
                    sequence = texts1[1]
                    ack = texts1[2]
                    win = texts1[3]
                    length = texts1[7]
                    evenement = {"heure": time, "ip source": source, "ip destinataire": destination, "sequence": sequence, "acknowledge": ack, "win": win, "taille": length}
                    tableau_evenement.append(evenement)
        elif 'ack' in line:
            texts2 = line.split(',')
            if len(texts2) >= 5:
                ack1 = texts2[1]
                win1 = texts2[2]
                length1 = texts2[6]
                evenement = {"heure": time, "ip source": source, "ip destinataire": destination, "acknowledge": ack1 , "win": win1, "taille": length1}
                tableau_evenement.append(evenement)

    autre1 = nb_paquet - nb_src_bp_linux8 - nb_src_solunet
    autre2 = nb_paquet - nb_dst_bp_linux8 - nb_dst_solunet

    start_size1 = np.array([nb_src_bp_linux8, nb_src_solunet, autre1, nb_paquet])
    start_name1 = np.array(["BP-Linux8", "solunet", "autre", "paquets totals"])
    tableau1 = np.vstack((start_name1, start_size1)).T

    labels1 = "BP-Linux8", "solunet", "autre", "paquets totals"
    size1 = start_size1
    colors1 = ["red", "yellow", "blue", "green"]

    def absolute_value(val):
        a = np.round(val/100.*np.sum(size1), 0)
        return int(a)

    start_size2 = np.array([nb_dst_bp_linux8, nb_dst_solunet, autre2, nb_paquet])
    start_name2 = np.array(["BP-Linux8", "solunet", "autre", "paquets totals"])
    tableau2 = np.vstack((start_name2, start_size2)).T

    labels2 = "BP-Linux8", "solunet", "autre", "paquets totals"
    size2 = start_size2
    colors2 = ["red", "yellow", "blue", "green"]

    def absolute_value(val):
        a = np.round(val/100.*np.sum(size2), 0)
        return int(a)

    df = pd.DataFrame(tableau_evenement)
    df_src = pd.DataFrame(tableau1, columns=["Source", "Nombre"])
    df_dst = pd.DataFrame(tableau2, columns=["Destination", "Nombre"])

    html_src = df_src.to_html(index=False)
    html_dst = df_dst.to_html(index=False)

    plt.figure(figsize=(10, 5))

    plt.figure(figsize=(5, 5))
    plt.bar(labels1, size1, color=colors1)
    plt.xlabel('sources')
    plt.ylabel('Nombre de paquets')
    plt.title('répartition des paquets envoyés')
    plt.savefig("static/images/diagramme_batons1.png")

    plt.figure(figsize=(5, 5))
    plt.bar(labels2, size2, color=colors2)
    plt.xlabel('destinations')
    plt.title('répartition des paquets reçus')
    plt.savefig("static/images/diagramme_batons2.png")

    output = markdown.markdown(f'''
    # Nombre de paquets (total) : {nb_paquet}
    ### Ces données sont issues du fichier DumpFile.txt
                            Sur ce fichier, tous les paquets sont envoyés en l'espace de seulement 1 minute
    **Source des paquets:**
    {html_src} 
    **Destination des paquets:**
    {html_dst}
    # Présentation des mêmes données avec un diagramme à barres, ci-contre

    #### On comprend donc avec ces données que la machine portant le nom de BP-Linux se fait attaquer par une machine de nom Solunet
    #### On suppose donc un DDOS sur la machine BP-Linux8 par la machine Solunet
    ''')

    with open("bilan.md", "w") as bilan_file:
        bilan_file.write(output)

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
        analyze_dumpfile(file_content)

        return redirect('/result')

    except Exception as e:
        return f"Une erreur s'est produite: {str(e)}"
    
@app.route('/download')
def download():
    # Fournir le chemin vers le fichier 'test.csv' pour le téléchargement
    return send_file("test.csv", as_attachment=True, download_name="test.csv")

@app.route('/result')
def result():
    # Read the content of the 'bilan.md' file
    with open("bilan.md", "r") as bilan_file:
        bilan_content = bilan_file.read()

    # Render the 'result.html' template with the content and filenames
    return render_template('results.html', bilan_content=bilan_content)

if __name__ == "__main__":
    app.run(debug=True)
