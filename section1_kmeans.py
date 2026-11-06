#!/usr/bin/env python3
"""TD Clustering - Section 1 : clustering k-means.

Implementation de k-means sans bibliotheque externe, pour des points de
dimension quelconque. Un point est represente par une liste de nombres,
par exemple [1] en 1D ou [-2, 3] en 2D.
"""

import math


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
