#!/usr/bin/env python3
"""TD Clustering - Section 1, Exercice 4 : comparaison avec SciKit-Learn.

Usage :
    .venv/bin/python section1_sklearn.py
"""

import contextlib
import io
import math

from numpy import array
from sklearn.cluster import KMeans

from section1_kmeans import kmeans


def kmeans_sklearn(data, k, centroides_initiaux):
    """k-means de SciKit-Learn a partir des centroides initiaux donnes.
    n_init=1 : une seule execution, a partir de ces centroides."""
    return KMeans(n_clusters=k, n_init=1, init=array(centroides_initiaux)).fit(data)


def labels_vers_clusters(data, labels, k):
    """Regroupe les points selon leur label : clusters[j] contient les points
    de label j, dans l'ordre du jeu de donnees (meme format que notre code)."""
    clusters = [[] for _ in range(k)]
    for point, label in zip(data, labels):
        clusters[label].append(point)
    return clusters


def memes_clusters(clusters_a, clusters_b):
    """Vrai si les deux clusterings regroupent les memes points, quel que soit
    le numero des clusters (on compare les partitions, pas les labels)."""
    def forme_canonique(clusters):
        return sorted(tuple(tuple(point) for point in cluster) for cluster in clusters)
    return forme_canonique(clusters_a) == forme_canonique(clusters_b)


if __name__ == "__main__":
    data1 = [[1], [2], [18], [20], [31]]
    data2 = [[2], [4], [6], [12], [24], [30]]
    M = [[-2, 3], [-2, 1], [-2, -1], [2, -1], [2, 1], [1, 0]]

    # Code de l'enonce (Exercice 1)
    print("=== Code de l'enonce ===")
    print(KMeans(n_clusters=3, n_init=1, init=array([[1], [2], [18]])).fit(data1).labels_)
    print(KMeans(n_clusters=3, n_init=1, init=array([[18], [20], [31]])).fit(data1).labels_)

    # Comparaison automatique notre code / SciKit-Learn
    tests = [
        ("Ex1, init [1],[2],[18]", data1, 3, [[1], [2], [18]]),
        ("Ex1, init [18],[20],[31]", data1, 3, [[18], [20], [31]]),
        ("Ex2 (a), init [2],[6]", data2, 2, [[2], [6]]),
        ("Ex2 (b), init [12],[24]", data2, 2, [[12], [24]]),
        ("Ex3, init M1,M2", M, 2, [M[0], M[1]]),
        ("Ex3, init M4,M6", M, 2, [M[3], M[5]]),
    ]
    print("\n=== Comparaison notre k-means / SciKit-Learn ===")
    for nom, data, k, init in tests:
        # on masque l'affichage detaille de notre fonction (deja vu en Ex1-3)
        with contextlib.redirect_stdout(io.StringIO()):
            notre_sse, nos_clusters = kmeans(data, k, init, retourner_clusters=True)
        modele = kmeans_sklearn(data, k, init)
        clusters_sk = labels_vers_clusters(data, modele.labels_, k)
        print(f"\n{nom}")
        print("  labels_ SciKit-Learn :", modele.labels_)
        print("  clusters notre code  :", nos_clusters)
        print("  clusters SciKit-Learn:", clusters_sk)
        print(f"  SSE notre code = {notre_sse:.4f}   inertia_ SciKit-Learn = {modele.inertia_:.4f}")
        print("  -> memes clusters :", "OUI" if memes_clusters(nos_clusters, clusters_sk) else "NON",
              "| meme SSE :", "OUI" if math.isclose(notre_sse, modele.inertia_) else "NON")
