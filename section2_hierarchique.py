#!/usr/bin/env python3
import os

import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")


def dendrogramme(donnees, labels, methode, ax, orientation="top"):
    """donnees : distances au format compact 1D ou liste de points (linkage accepte les deux)."""
    Z = hierarchy.linkage(donnees, method=methode)
    hierarchy.dendrogram(Z, labels=labels, orientation=orientation, ax=ax)
    return Z


def similarite_vers_distance(sim):
    return 1 - np.array(sim)


def figure_single_complete(donnees, labels, titre, fichier):
    """Single link et complete link cote a cote ; affiche les fusions."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, methode in zip(axes, ["single", "complete"]):
        Z = dendrogramme(donnees, labels, methode, ax)
        ax.set_title(f"{methode.capitalize()} link")
        print(f"  {methode.capitalize()} link - fusions (cluster 1, cluster 2, distance, taille) :")
        for ligne in Z:
            print(f"    {int(ligne[0])} {int(ligne[1])} {ligne[2]:.2f} {int(ligne[3])}")
    fig.suptitle(titre)
    fig.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    fig.savefig(os.path.join(FIG_DIR, fichier))
    plt.close(fig)


if __name__ == "__main__":
    plt.switch_backend("Agg")  # ici les figures sont seulement sauvegardees
    labels = ["p1", "p2", "p3", "p4", "p5"]

    # 1) Matrice de distance, au format compact (valeurs au-dessus de la diagonale)
    data = [0.1, 0.9, 0.35, 0.8, 0.3, 0.4, 0.5, 0.6, 0.7, 0.2]
    print("Matrice de distance :", data)
    figure_single_complete(data, labels, "Matrice de distance", "s2_distance.png")

    # 2) Matrice de similarite -> distance = 1 - similarite
    sim = [
        [1.00, 0.10, 0.41, 0.55, 0.35],
        [0.10, 1.00, 0.64, 0.47, 0.98],
        [0.41, 0.64, 1.00, 0.44, 0.85],
        [0.55, 0.47, 0.44, 1.00, 0.76],
        [0.35, 0.98, 0.85, 0.76, 1.00],
    ]
    data_sim = squareform(similarite_vers_distance(sim))
    print("\nMatrice de similarite convertie en distances :", [round(float(d), 2) for d in data_sim])
    figure_single_complete(data_sim, labels, "Matrice de similarite (distance = 1 - similarite)",
                           "s2_similarite.png")
