#!/usr/bin/env python3
"""TD Clustering - Section 2 : clustering hierarchique avec SciPy.

Usage :
    python3 section2_hierarchique.py            # sauvegarde les figures dans figures/
    python3 section2_hierarchique.py --show     # affiche aussi les figures a l'ecran
"""

import os
import sys

import matplotlib

if "--show" not in sys.argv:
    matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")
LABELS = ["p1", "p2", "p3", "p4", "p5"]
METHODS = [("single", "Single link"), ("complete", "Complete link")]


def matrix_to_condensed(matrix):
    """Lit les valeurs au-dessus de la diagonale principale (format compact 1D
    attendu par hierarchy.linkage)."""
    n = len(matrix)
    return [matrix[i][j] for i in range(n) for j in range(i + 1, n)]


def similarity_to_distance(sim):
    """distance(pi, pj) = 1 - similarite(pi, pj)."""
    return [[1 - s for s in row] for row in sim]


def plot_dendrograms(condensed, labels, title, filename):
    """Genere cote a cote les dendrogrammes single link et complete link."""
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, (method, name) in zip(axes, METHODS):
        Z = hierarchy.linkage(condensed, method=method)
        hierarchy.dendrogram(Z, labels=labels, ax=ax)
        ax.set_title(name)
        print(f"  {name} - matrice de linkage (idx1, idx2, distance, taille) :")
        for row in Z:
            print(f"    {int(row[0])} {int(row[1])} {row[2]:.2f} {int(row[3])}")
    fig.suptitle(title)
    fig.tight_layout()
    os.makedirs(FIG_DIR, exist_ok=True)
    path = os.path.join(FIG_DIR, filename)
    fig.savefig(path, dpi=150)
    print(f"  -> {path}")
    return fig


def main():
    # 1) Matrice de distance donnee directement, encodee a la main
    data = [0.1, 0.9, 0.35, 0.8, 0.3, 0.4, 0.5, 0.6, 0.7, 0.2]
    print("Matrice de distance :", data)
    plot_dendrograms(data, LABELS, "Matrice de distance", "s2_distance.png")

    # 2) Matrice de similarite -> distance = 1 - similarite
    similarity = [
        [1.00, 0.10, 0.41, 0.55, 0.35],
        [0.10, 1.00, 0.64, 0.47, 0.98],
        [0.41, 0.64, 1.00, 0.44, 0.85],
        [0.55, 0.47, 0.44, 1.00, 0.76],
        [0.35, 0.98, 0.85, 0.76, 1.00],
    ]
    dist = similarity_to_distance(similarity)
    condensed = matrix_to_condensed(dist)
    # Verification avec la fonction de SciPy (checks=False car 1 - 1.00 peut
    # donner des flottants non exactement nuls / symetriques)
    assert all(abs(a - b) < 1e-12
               for a, b in zip(condensed, squareform(dist, checks=False)))
    print("\nMatrice de similarite convertie :", [round(d, 2) for d in condensed])
    plot_dendrograms(condensed, LABELS, "Matrice de similarite (distance = 1 - sim)",
                     "s2_similarite.png")

    if "--show" in sys.argv:
        plt.show()


if __name__ == "__main__":
    main()
