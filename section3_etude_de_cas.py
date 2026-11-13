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

VARIABLES = ["child_mort", "exports", "health", "imports", "income", "inflation", "life_expec", "total_fer", "gdpp"]
VARIABLES_RESUME = ["child_mort", "exports", "income", "life_expec", "total_fer", "gdpp"]

REFERENCE_ENONCE = [2.91, -0.1]  # debut de data_reduced dans l'enonce
GRAINES = {2: 0, 3: 13}          # graines qui redonnent les Figures 1 et 2 de l'enonce


def lire_donnees(chemin=FICHIER_CSV):
    with open(chemin, newline="") as f:
        en_tete, *lignes = list(csv.reader(f))
    if en_tete != ["country"] + VARIABLES:
        raise ValueError("Colonnes inattendues dans le fichier CSV : %s" % en_tete)
    countries = [ligne[0] for ligne in lignes]
    data_country = [[float(v) for v in ligne[1:]] for ligne in lignes]
    return countries, data_country


def preparer_donnees(countries, data_country):
    X = array(data_country)
    n = len(countries)
    p = len(data_country[0])

    # La matrice des donnees centrees, c'est-a-dire la somme = 0 sur chaque colonne
    Y = X - matmul(transpose(array([n * [1]])), transpose(array([[mean(variable)] for variable in transpose(X)])))

    # La matrice des donnees centrees et reduites, qui en plus a l'ecart type constant = 1 sur chaque colonne
    Z = matmul(Y, array(list(map(lambda variable: [1. / std(variable)], transpose(X)))) * identity(p))

    # La matrice (symetrique) de variance/covariance des donnees centrees reduites
    R = matmul(matmul(transpose(Z), 1. / n * identity(n)), Z)

    valeurs_propres, eigenvectors = eig(R)

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


def kmeans_muet(data, k, graine):
    """Sans l'affichage detaille. Retourne (SSE, clusters, nombre d'iterations)."""
    random.seed(graine)
    with contextlib.redirect_stdout(io.StringIO()) as sortie:
        sse, clusters = kmeans(data, k, retourner_clusters=True)
    return sse, clusters, sortie.getvalue().count("Iteration")


def figure_kmeans(data, noms, clusters, titre, fichier):
    fig, ax = plt.subplots(figsize=(14, 14))
    for j, cluster in enumerate(clusters):
        couleur = COULEURS[j % len(COULEURS)]
        ax.plot([p[0] for p in cluster], [p[1] for p in cluster], ".", color=couleur)
        centroide = calculer_centroides([cluster], [None])[0]
        ax.plot(centroide[0], centroide[1], "x", color=couleur, markersize=12, markeredgewidth=2)
    for nom, (x, y) in zip(noms, data):
        ax.annotate(nom, (x, y), fontsize=8)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_title(titre)
    fig.savefig(fichier)
    plt.close(fig)


if __name__ == "__main__":
    plt.switch_backend("Agg")  # ici les figures sont seulement sauvegardees
    os.makedirs(FIG_DIR, exist_ok=True)

    # ---------- Exercice 1 : preparation des donnees ----------
    countries, data_country = lire_donnees()
    print(len(data_country), "pays,", len(data_country[0]), "variables")
    print("data_country commence par", data_country[:2])

    data_reduced, part_variance = preparer_donnees(countries, data_country)
    print("data_reduced commence par", [[round(v, 2) for v in point] for point in data_reduced[:2]])
    print("Part de la variance expliquee : composante 1 = %.1f %%, composante 2 = %.1f %%, total = %.1f %%"
          % (100 * part_variance[0], 100 * part_variance[1], 100 * sum(part_variance)))

    print("Correlation de chaque variable avec les axes X et Y :")
    X, C = array(data_country), array(data_reduced)
    for v, nom in enumerate(VARIABLES):
        cx = np.corrcoef(X[:, v], C[:, 0])[0, 1]
        cy = np.corrcoef(X[:, v], C[:, 1])[0, 1]
        print(f"  {nom:<11s} X : {cx:+.2f}   Y : {cy:+.2f}")

    nom_du_point = {tuple(p): nom for p, nom in zip(data_reduced, countries)}
    variables_du_pays = dict(zip(countries, data_country))

    def en_noms(clusters):
        return [[nom_du_point[tuple(p)] for p in c] for c in clusters]

    def cle(clusters):
        """Identique pour deux clusterings egaux, quel que soit l'ordre des clusters."""
        return tuple(sorted(tuple(sorted(c)) for c in en_noms(clusters)))

    # ---------- Exercice 2 : k-means, k = 2 et k = 3 (Figures 1 et 2) ----------
    for k in [2, 3]:
        sse, clusters, nb_iter = kmeans_muet(data_reduced, k, GRAINES[k])
        print(f"k-means k = {k} (graine {GRAINES[k]}) : {nb_iter} iterations,"
              f" SSE = {sse:.2f}, tailles des clusters = {[len(c) for c in clusters]}")

        for j, pays in enumerate(en_noms(clusters)):
            moyennes = mean([variables_du_pays[nom] for nom in pays], axis=0)
            print(f"  cluster {COULEURS[j]:<6s} :", ", ".join(
                f"{nom} = {moyennes[VARIABLES.index(nom)]:.1f}" for nom in VARIABLES_RESUME))

        figure_kmeans(data_reduced, countries, clusters,
                      f"Jeu de donnees Country : k-means avec k = {k}",
                      os.path.join(FIG_DIR, f"s3_kmeans_k{k}.png"))
        if k == 3:
            kmeans3 = [set(pays) for pays in en_noms(clusters)]  # pour comparer au complete link

        # Avec d'autres centroides initiaux, aurait-on des clusterings tres differents ?
        tirages = {}  # clustering -> [nombre de fois, SSE]
        for graine in range(200):
            sse_g, clusters_g, _ = kmeans_muet(data_reduced, k, graine)
            tirages.setdefault(cle(clusters_g), [0, sse_g])[0] += 1
        sses = [s for _, s in tirages.values()]
        print(f"  200 tirages aleatoires : {len(tirages)} clusterings differents,"
              f" SSE entre {min(sses):.2f} et {max(sses):.2f}")
        for c, (nb, sse_c) in sorted(tirages.items(), key=lambda t: -t[1][0])[:6]:
            petits = [list(g) for g in c if len(g) <= 5]
            marque = "  <- clustering de la figure" if c == cle(clusters) else ""
            print(f"    {nb:3d} fois : SSE = {sse_c:.2f}, tailles = {sorted(len(g) for g in c)},"
                  f" petits clusters = {petits}{marque}")

    # ---------- Exercice 2 : single link et complete link (Figures 3 et 4) ----------
    for methode in ["single", "complete"]:
        fig, ax = plt.subplots(figsize=(10, 22))
        Z = dendrogramme(data_reduced, countries, methode, ax, orientation="right")
        ax.set_title(f"Jeu de donnees Country : clustering hierarchique avec {methode.capitalize()} link")
        fig.savefig(os.path.join(FIG_DIR, f"s3_{methode}.png"))
        plt.close(fig)

        # on coupe l'arbre en 2 puis 3 clusters
        for nb in [2, 3]:
            labels = hierarchy.fcluster(Z, nb, criterion="maxclust")
            groupes = [[pays for pays, l in zip(countries, labels) if l == c] for c in sorted(set(labels))]
            petits = [g for g in groupes if len(g) <= 5]
            print(f"{methode.capitalize()} link coupe en {nb} clusters : tailles = {[len(g) for g in groupes]},"
                  f" petits clusters = {petits}")

        # comparaison de la coupe en 3 clusters du complete link avec k-means (k = 3)
        if methode == "complete":
            for g in map(set, groupes):
                communs = [len(g & c) for c in kmeans3]
                print(f"  cluster de {len(g)} pays, pays en commun avec chaque cluster k-means (k = 3) :",
                      ", ".join(f"{COULEURS[j]} {n}" for j, n in enumerate(communs)))
                j = communs.index(max(communs))
                en_plus, en_moins = sorted(g - kmeans3[j]), sorted(kmeans3[j] - g)
                if len(en_plus) + len(en_moins) <= 5:
                    print(f"    differences avec le cluster {COULEURS[j]} : en plus {en_plus}, en moins {en_moins}")
