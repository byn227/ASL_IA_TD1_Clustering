#!/usr/bin/env python3
"""TD Clustering - Section 3 : etude de cas sur le jeu de donnees Country.

Usage :
    .venv/bin/python section3_etude_de_cas.py
"""

import contextlib
import csv
import io
import os
import random

import numpy as np
import matplotlib.pyplot as plt
from numpy import array, identity, transpose, matmul, std, mean, argsort
from numpy.linalg import eig
from scipy.cluster import hierarchy

from section1_kmeans import kmeans, calculer_centroides, COULEURS
from section2_hierarchique import dendrogramme

DOSSIER = os.path.dirname(os.path.abspath(__file__))
FICHIER_CSV = os.path.join(DOSSIER, "data", "Country-data.csv")
FIG_DIR = os.path.join(DOSSIER, "figures")

# Les 9 variables du fichier CSV, dans l'ordre des colonnes
VARIABLES = ["child_mort", "exports", "health", "imports", "income",
             "inflation", "life_expec", "total_fer", "gdpp"]

# Variables affichees pour decrire chaque cluster
VARIABLES_RESUME = ["child_mort", "exports", "income", "life_expec", "total_fer", "gdpp"]

# Debut de data_reduced donne dans l'enonce (sert a fixer le signe des axes)
REFERENCE_ENONCE = [2.91, -0.1]

# Graines du tirage aleatoire des centroides initiaux, choisies pour retrouver
# les Figures 1 et 2 de l'enonce (memes clusters et memes couleurs)
GRAINES = {2: 0, 3: 13}


def lire_donnees(chemin=FICHIER_CSV):
    """Lit le fichier CSV. Retourne (countries, data_country) :
    countries    : liste des 167 noms de pays
    data_country : liste de 167 listes de 9 variables (float)"""
    with open(chemin, newline="") as f:
        en_tete, *lignes = list(csv.reader(f))  # on met de cote la ligne d'en-tete
    if en_tete != ["country"] + VARIABLES:
        raise ValueError("Colonnes inattendues dans le fichier CSV : %s" % en_tete)
    countries = [ligne[0] for ligne in lignes]
    data_country = [[float(v) for v in ligne[1:]] for ligne in lignes]
    return countries, data_country


def preparer_donnees(countries, data_country):
    """ACP sur les donnees centrees reduites (squelette de l'enonce).
    Retourne (data_reduced, part_variance) :
    data_reduced  : les 167 pays projetes sur les 2 composantes principales
    part_variance : part de la variance expliquee par chacune des 2 composantes"""
    # Les memes donnees de la matrice data_country, dans le format "array"
    X = array(data_country)

    # Le nombre de points
    n = len(countries)

    # Le nombre de variables
    p = len(data_country[0])

    # La matrice des donnees centrees, c'est-a-dire la somme = 0 sur chaque colonne
    Y = X - matmul(transpose(array([n * [1]])), transpose(array([[mean(variable)] for variable in transpose(X)])))

    # La matrice des donnees centrees et reduites, qui en plus a l'ecart type constant = 1 sur chaque colonne
    Z = matmul(Y, array(list(map(lambda variable: [1. / std(variable)], transpose(X)))) * identity(p))

    # La matrice (symetrique) de variance/covariance des donnees centrees reduites
    R = matmul(matmul(transpose(Z), 1. / n * identity(n)), Z)

    # Les vecteurs propres de R
    valeurs_propres, eigenvectors = eig(R)

    # R est symetrique reelle, donc ses valeurs propres sont reelles, mais eig
    # peut les renvoyer en nombres complexes (partie imaginaire nulle)
    assert np.allclose(valeurs_propres.imag, 0) and np.allclose(eigenvectors.imag, 0)
    valeurs_propres, eigenvectors = valeurs_propres.real, eigenvectors.real

    # eig ne trie pas les valeurs propres : on les range par ordre decroissant
    ordre = argsort(valeurs_propres)[::-1]
    valeurs_propres, eigenvectors = valeurs_propres[ordre], eigenvectors[:, ordre]

    # Le signe d'un vecteur propre est arbitraire (v et -v conviennent) : on le
    # choisit pour retrouver les memes axes que l'enonce (symetrie miroir, les
    # distances entre pays ne changent pas)
    for c in range(2):
        if matmul(Z[0], eigenvectors[:, c]) * REFERENCE_ENONCE[c] < 0:
            eigenvectors[:, c] = -eigenvectors[:, c]

    # Part de la variance expliquee : valeur propre / p (la trace de R vaut p)
    part_variance = [float(valeurs_propres[0] / p), float(valeurs_propres[1] / p)]

    # Les 2 composantes principals = 2 nouvelles variables contenant le plus d'information possible des 9 variables initiales
    components = [matmul(Z, eigenvectors[:, 0]), matmul(Z, eigenvectors[:, 1])]

    # La matrice initiale, projetee sur 2 nouvelles colonnes qui representent les 2 composantes principales
    data_reduced = [[float(components[0][i]), float(components[1][i])] for i in range(n)]
    return data_reduced, part_variance


def correlations_composantes(data_country, data_reduced):
    """Correlation entre chaque variable initiale et chacune des 2 composantes
    principales. Sert a interpreter les axes X et Y des figures.
    Retourne une liste de 9 couples (correlation avec X, correlation avec Y)."""
    X = array(data_country)
    C = array(data_reduced)
    return [(float(np.corrcoef(X[:, v], C[:, 0])[0, 1]), float(np.corrcoef(X[:, v], C[:, 1])[0, 1]))
            for v in range(X.shape[1])]


def moyennes_clusters(data_reduced, data_country, clusters):
    """Moyenne des variables initiales (non centrees reduites) dans chaque
    cluster, pour decrire les pays qu'il contient."""
    ligne_du_point = {tuple(point): i for i, point in enumerate(data_reduced)}
    return [mean(array([data_country[ligne_du_point[tuple(p)]] for p in cluster]), axis=0)
            for cluster in clusters]


def figure_kmeans(data, noms, clusters, titre, fichier):
    """Figure du clustering final : points colores selon leur cluster et
    annotes avec le nom du pays, centroides representes par des 'x'."""
    fig, ax = plt.subplots(figsize=(14, 14))
    for j, cluster in enumerate(clusters):
        if not cluster:
            continue
        couleur = COULEURS[j % len(COULEURS)]
        ax.plot([p[0] for p in cluster], [p[1] for p in cluster], ".", color=couleur)
        centroide = calculer_centroides([cluster], [None])[0]
        ax.plot(centroide[0], centroide[1], "x", color=couleur,
                markersize=12, markeredgewidth=2)
    for nom, (x, y) in zip(noms, data):
        ax.annotate(nom, (x, y), fontsize=8)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(titre)
    fig.savefig(fichier)
    plt.close(fig)


def comparer_graines(data, noms, k, graines):
    """Lance k-means avec chacune des graines (centroides initiaux tires au
    hasard) et regroupe les clusterings identiques, quels que soient les
    numeros des clusters. Retourne une liste de (nombre de fois, SSE, clusters
    sous forme de noms de pays), du plus frequent au moins frequent."""
    nom_du_point = {tuple(point): nom for point, nom in zip(data, noms)}
    resultats = {}
    for graine in graines:
        random.seed(graine)
        with contextlib.redirect_stdout(io.StringIO()):
            sse, clusters = kmeans(data, k, retourner_clusters=True)
        cle = tuple(sorted(tuple(sorted(nom_du_point[tuple(p)] for p in c)) for c in clusters))
        nb, _ = resultats.get(cle, (0, sse))
        resultats[cle] = (nb + 1, sse)
    return sorted(((nb, sse, cle) for cle, (nb, sse) in resultats.items()), key=lambda r: -r[0])


if __name__ == "__main__":
    plt.switch_backend("Agg")  # ici les figures sont seulement sauvegardees
    os.makedirs(FIG_DIR, exist_ok=True)

    # Exercice 1 : preparation des donnees
    countries, data_country = lire_donnees()
    print(len(data_country), "pays,", len(data_country[0]), "variables")
    print("data_country commence par", data_country[:2])
    data_reduced, part_variance = preparer_donnees(countries, data_country)
    print("data_reduced commence par", [[round(v, 2) for v in point] for point in data_reduced[:2]])
    print("Part de la variance expliquee : composante 1 = %.1f %%, composante 2 = %.1f %%, total = %.1f %%"
          % (100 * part_variance[0], 100 * part_variance[1], 100 * sum(part_variance)))
    print("Correlation de chaque variable avec les axes X et Y :")
    for nom, (cx, cy) in zip(VARIABLES, correlations_composantes(data_country, data_reduced)):
        print(f"  {nom:<11s} X : {cx:+.2f}   Y : {cy:+.2f}")

    # Exercice 2 : k-means avec k = 2 et k = 3 (Figures 1 et 2)
    noms_kmeans = {}  # clusters des figures, sous forme d'ensembles de noms de pays
    for k in [2, 3]:
        random.seed(GRAINES[k])
        # l'affichage detaille (167 points a chaque iteration) est masque,
        # on n'affiche qu'un resume
        with contextlib.redirect_stdout(io.StringIO()) as detail:
            sse, clusters = kmeans(data_reduced, k, retourner_clusters=True)
        print(f"k-means k = {k} (graine {GRAINES[k]}) : {detail.getvalue().count('Iteration')} iterations,"
              f" SSE = {sse:.2f}, tailles des clusters = {[len(c) for c in clusters]}")
        # moyenne de quelques variables initiales dans chaque cluster
        for j, moyennes in enumerate(moyennes_clusters(data_reduced, data_country, clusters)):
            print(f"  cluster {COULEURS[j]:<6s} :", ", ".join(
                f"{nom} = {moyennes[VARIABLES.index(nom)]:.1f}" for nom in VARIABLES_RESUME))
        figure_kmeans(data_reduced, countries, clusters,
                      f"Jeu de donnees Country : k-means avec k = {k}",
                      os.path.join(FIG_DIR, f"s3_kmeans_k{k}.png"))

        # Avec d'autres centroides initiaux tires au hasard, aurait-on obtenu
        # des clusterings tres differents ? On essaie 200 graines.
        nom_du_point = {tuple(p): nom for p, nom in zip(data_reduced, countries)}
        noms_kmeans[k] = [{nom_du_point[tuple(p)] for p in c} for c in clusters]
        cle_figure = tuple(sorted(tuple(sorted(nom_du_point[tuple(p)] for p in c)) for c in clusters))
        tirages = comparer_graines(data_reduced, countries, k, range(200))
        sses = [sse for _, sse, _ in tirages]
        print(f"  200 tirages aleatoires : {len(tirages)} clusterings differents,"
              f" SSE entre {min(sses):.2f} et {max(sses):.2f}")
        for nb, sse, cle in tirages[:6]:
            petits = [list(c) for c in cle if len(c) <= 5]
            marque = "  <- clustering de la figure" if cle == cle_figure else ""
            print(f"    {nb:3d} fois : SSE = {sse:.2f}, tailles = {sorted(len(c) for c in cle)},"
                  f" petits clusters = {petits}{marque}")

    # Exercice 2 : clustering hierarchique, single link et complete link
    # (Figures 3 et 4), avec la fonction de la Section 2
    for methode in ["single", "complete"]:
        fig, ax = plt.subplots(figsize=(10, 22))
        Z = dendrogramme(data_reduced, countries, methode, ax, orientation="right")
        ax.set_title(f"Jeu de donnees Country : clustering hierarchique avec {methode.capitalize()} link")
        fig.savefig(os.path.join(FIG_DIR, f"s3_{methode}.png"))
        plt.close(fig)
        # tailles des clusters si on coupe l'arbre en 2 ou 3 clusters
        for nb in [2, 3]:
            labels = hierarchy.fcluster(Z, nb, criterion="maxclust")
            groupes = [[countries[i] for i in range(len(countries)) if labels[i] == c]
                       for c in sorted(set(labels))]
            petits = [g for g in groupes if len(g) <= 5]
            print(f"{methode.capitalize()} link coupe en {nb} clusters : tailles = {[len(g) for g in groupes]},"
                  f" petits clusters = {petits}")
            # comparaison de la coupe en 3 clusters du complete link avec k-means (k = 3)
            if methode == "complete" and nb == 3:
                for g in groupes:
                    communs = [len(set(g) & c) for c in noms_kmeans[3]]
                    print(f"  cluster de {len(g)} pays, pays en commun avec chaque cluster k-means (k = 3) :",
                          ", ".join(f"{COULEURS[j]} {n}" for j, n in enumerate(communs)))
                    j = communs.index(max(communs))
                    en_plus, en_moins = sorted(set(g) - noms_kmeans[3][j]), sorted(noms_kmeans[3][j] - set(g))
                    if len(en_plus) + len(en_moins) <= 5:
                        print(f"    differences avec le cluster {COULEURS[j]} : en plus {en_plus}, en moins {en_moins}")
