#!/usr/bin/env python3
"""TD Clustering - Section 1 : clustering k-means.

Implementation de k-means sans bibliotheque externe, pour des points de
dimension quelconque. Un point est represente par une liste de nombres,
par exemple [1] en 1D ou [-2, 3] en 2D.

Usage :
    .venv/bin/python section1_kmeans.py
Affiche les resultats des Exercices 1 a 3 et sauvegarde les figures de
l'Exercice 3 dans figures/ex3_init_M1_M2_iter<i>.png et
figures/ex3_init_M4_M6_iter<i>.png.
"""

import math
import os
import random

import matplotlib.pyplot as plt

FIG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "figures")

# Couleur du cluster j (cluster 0 en rouge, cluster 1 en bleu, comme l'enonce)
COULEURS = ["red", "blue", "orange", "green", "purple", "brown", "pink", "gray"]


def distance_carree(p, q):
    """Carre de la distance euclidienne : somme_i (p_i - q_i)^2."""
    if len(p) != len(q):
        raise ValueError("Les deux points doivent avoir la meme dimension")
    return sum((a - b) ** 2 for a, b in zip(p, q))


def distance_euclidienne(p, q):
    """Distance euclidienne entre deux points p et q de meme dimension :
    d(p, q) = racine( somme_i (p_i - q_i)^2 )."""
    return math.sqrt(distance_carree(p, q))


def centroide_le_plus_proche(point, centroides):
    """Indice du centroide le plus proche de point.
    En cas d'egalite, on garde le premier (indice le plus petit)."""
    distances = [distance_euclidienne(point, c) for c in centroides]
    return distances.index(min(distances))


def affecter_points(data, centroides):
    """Affecte chaque point au centroide le plus proche.
    Retourne une liste de k clusters : clusters[j] contient les points
    affectes au centroide j, dans l'ordre du jeu de donnees."""
    clusters = [[] for _ in centroides]
    for point in data:
        clusters[centroide_le_plus_proche(point, centroides)].append(point)
    return clusters


def calculer_centroides(clusters, anciens_centroides):
    """Nouveau centroide de chaque cluster = moyenne de ses points,
    coordonnee par coordonnee.
    Si un cluster est vide, on garde son ancien centroide."""
    nouveaux = []
    for cluster, ancien in zip(clusters, anciens_centroides):
        if len(cluster) == 0:
            nouveaux.append(ancien)
        else:
            nouveaux.append([sum(coord) / len(cluster) for coord in zip(*cluster)])
    return nouveaux


def calculer_sse(clusters, centroides):
    """Erreur SSE = somme, sur tous les clusters, des carres des distances
    entre chaque point et le centroide de son cluster."""
    sse = 0
    for cluster, c in zip(clusters, centroides):
        for x in cluster:
            sse += distance_carree(x, c)
    return sse


def dessiner_iteration(data, noms, centroides, titre, fichier):
    """Figure 2D d'une iteration de k-means, sauvegardee dans fichier.
    Les points sont des 'o' annotes avec leur nom, les centroides des 'x' ;
    un cluster et son centroide ont la meme couleur."""
    fig, ax = plt.subplots(figsize=(5, 5))
    for i, point in enumerate(data):
        # meme regle que affecter_points : le point prend la couleur
        # du centroide le plus proche
        j = centroide_le_plus_proche(point, centroides)
        ax.plot(point[0], point[1], "o", color=COULEURS[j % len(COULEURS)])
        if noms is not None:
            ax.annotate(noms[i], (point[0], point[1]),
                        xytext=(3, 3), textcoords="offset points")
    for j, c in enumerate(centroides):
        ax.plot(c[0], c[1], "x", color=COULEURS[j % len(COULEURS)],
                markersize=12, markeredgewidth=2)
    # axes x = 0 et y = 0, et cadre symetrique autour de l'origine
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)
    limite = max(abs(v) for point in data for v in point) + 1
    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(titre)
    fig.savefig(fichier, dpi=100)
    plt.close(fig)


def kmeans(data, k, centroides_initiaux=None, noms=None, prefixe_figures=None,
           retourner_clusters=False):
    """Algorithme k-means.

    data               : liste de points (meme dimension pour tous)
    k                  : nombre de clusters
    centroides_initiaux: liste de k points ; si None, on tire au hasard
                         k points distincts du jeu de donnees
    noms               : (optionnel) noms des points, dans le meme ordre que
                         data, pour etiqueter les points sur les figures
    prefixe_figures    : (optionnel, donnees 2D) si different de None, la
                         figure de l'iteration i est sauvegardee dans
                         <prefixe_figures>_iter<i>.png
    retourner_clusters : (optionnel) si True, retourne (SSE, clusters finaux)
                         au lieu de la SSE seule

    Affiche les resultats intermediaires et retourne l'erreur SSE.
    """
    if centroides_initiaux is None:
        centroides = random.sample(data, k)
    else:
        centroides = centroides_initiaux
    if len(centroides) != k:
        raise ValueError("Il faut exactement k centroides initiaux")
    if prefixe_figures is not None:
        if any(len(point) != 2 for point in data):
            raise ValueError("Les figures ne sont possibles qu'en 2D")
        os.makedirs(os.path.dirname(os.path.abspath(prefixe_figures)), exist_ok=True)

    clusters_precedents = None
    iteration = 1
    while True:
        clusters = affecter_points(data, centroides)
        print("Iteration", iteration)
        for c, cluster in zip(centroides, clusters):
            print("Centroid", c, " Points", cluster)
        if prefixe_figures is not None:
            dessiner_iteration(data, noms, centroides, f"Iteration {iteration}",
                               f"{prefixe_figures}_iter{iteration}.png")
        # Critere d'arret : l'affectation des points n'a pas change,
        # donc les centroides ne changeraient plus non plus.
        if clusters == clusters_precedents:
            break
        clusters_precedents = clusters
        centroides = calculer_centroides(clusters, centroides)
        iteration += 1

    sse = calculer_sse(clusters, centroides)
    print("Fin clustering, erreur = ", sse)
    if retourner_clusters:
        return sse, clusters
    return sse


if __name__ == "__main__":
    plt.switch_backend("Agg")  # ici les figures sont seulement sauvegardees

    data1 = [[1], [2], [18], [20], [31]]

    print("=== Exercice 1 : centroides initiaux [[1], [2], [18]] ===")
    kmeans(data1, 3, [[1], [2], [18]])

    print("\n=== Exercice 1 : centroides initiaux [[18], [20], [31]] ===")
    kmeans(data1, 3, [[18], [20], [31]])

    print("\n=== Exercice 1 : centroides initiaux tires au hasard ===")
    kmeans(data1, 3)

    data2 = [[2], [4], [6], [12], [24], [30]]

    print("\n=== Exercice 2 (a) : centroides initiaux [[2], [6]] ===")
    kmeans(data2, 2, [[2], [6]])

    print("\n=== Exercice 2 (b) : centroides initiaux [[12], [24]] ===")
    kmeans(data2, 2, [[12], [24]])

    M = [[-2, 3], [-2, 1], [-2, -1], [2, -1], [2, 1], [1, 0]]
    noms_M = ["M1", "M2", "M3", "M4", "M5", "M6"]

    print("\n=== Exercice 3 : centroides initiaux M1 et M2 ===")
    kmeans(M, 2, [M[0], M[1]], noms=noms_M,
           prefixe_figures=os.path.join(FIG_DIR, "ex3_init_M1_M2"))

    print("\n=== Exercice 3 : centroides initiaux M4 et M6 ===")
    kmeans(M, 2, [M[3], M[5]], noms=noms_M,
           prefixe_figures=os.path.join(FIG_DIR, "ex3_init_M4_M6"))
