#!/usr/bin/env python3
"""TD Clustering - Section 1 : clustering k-means.

Implementation de k-means sans bibliotheque externe, pour des points de
dimension quelconque. Un point est represente par une liste de nombres,
par exemple [1] en 1D ou [-2, 3] en 2D.
"""

import math
import random


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


def kmeans(data, k, centroides_initiaux=None):
    """Algorithme k-means.

    data               : liste de points (meme dimension pour tous)
    k                  : nombre de clusters
    centroides_initiaux: liste de k points ; si None, on tire au hasard
                         k points distincts du jeu de donnees

    Affiche les resultats intermediaires et retourne l'erreur SSE.
    """
    if centroides_initiaux is None:
        centroides = random.sample(data, k)
    else:
        centroides = centroides_initiaux
    if len(centroides) != k:
        raise ValueError("Il faut exactement k centroides initiaux")

    clusters_precedents = None
    iteration = 1
    while True:
        clusters = affecter_points(data, centroides)
        print("Iteration", iteration)
        for c, cluster in zip(centroides, clusters):
            print("Centroid", c, " Points", cluster)
        # Critere d'arret : l'affectation des points n'a pas change,
        # donc les centroides ne changeraient plus non plus.
        if clusters == clusters_precedents:
            break
        clusters_precedents = clusters
        centroides = calculer_centroides(clusters, centroides)
        iteration += 1

    sse = calculer_sse(clusters, centroides)
    print("Fin clustering, erreur = ", sse)
    return sse


if __name__ == "__main__":
    data1 = [[1], [2], [18], [20], [31]]

    print("=== Exercice 1 : centroides initiaux [[1], [2], [18]] ===")
    kmeans(data1, 3, [[1], [2], [18]])

    print("\n=== Exercice 1 : centroides initiaux [[18], [20], [31]] ===")
    kmeans(data1, 3, [[18], [20], [31]])

    print("\n=== Exercice 1 : centroides initiaux tires au hasard ===")
    kmeans(data1, 3)
