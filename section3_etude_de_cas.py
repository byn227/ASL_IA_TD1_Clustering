#!/usr/bin/env python3
"""TD Clustering - Section 3 : etude de cas sur Country-data.csv.

Workflow : lecture du CSV -> ACP sur donnees centrees reduites -> k-means
(k = 2, 3) et clustering hierarchique (single / complete link) -> figures.

Usage :
    python3 section3_etude_de_cas.py                  # figures dans figures/
    python3 section3_etude_de_cas.py --show           # les affiche aussi
    python3 section3_etude_de_cas.py --csv chemin.csv # autre emplacement du CSV
"""

import argparse
import csv
import os
import random
from collections import Counter

import matplotlib
from numpy import argsort, array, identity, matmul, mean, std, transpose
from numpy.linalg import eig

HERE = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = os.path.join(HERE, "figures")
DEFAULT_CSV = os.path.join(HERE, "data", "Country-data.csv")
COLORS = ["red", "blue", "orange", "green", "purple", "brown"]


# ---------------------------------------------------------------------------
# 1. Preparation des donnees
# ---------------------------------------------------------------------------
def read_country_data(path):
    """Retourne (countries, variables, data_country) ou data_country est une
    liste de 167 listes de 9 flottants. Le module csv gere les noms entre
    guillemets contenant une virgule (ex. "Congo, Dem. Rep.")."""
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
        countries, data_country = [], []
        for row in reader:
            if not row:
                continue
            countries.append(row[0])
            data_country.append([float(x) for x in row[1:]])
    return countries, header[1:], data_country


def pca_2d(data_country):
    """ACP sur donnees centrees reduites (squelette du sujet, complete).

    Retourne (data_reduced, eigenvalues tries, eigenvectors tries)."""
    X = array(data_country)
    n = len(data_country)
    p = len(data_country[0])
    # Donnees centrees : somme = 0 sur chaque colonne
    Y = X - matmul(transpose(array([n * [1]])),
                   transpose(array([[mean(variable)] for variable in transpose(X)])))
    # Donnees centrees reduites : ecart type = 1 sur chaque colonne
    Z = matmul(Y, array(list(map(lambda variable: [1. / std(variable)],
                                 transpose(X)))) * identity(p))
    # Matrice de correlation (variance/covariance des donnees centrees reduites)
    R = matmul(matmul(transpose(Z), 1. / n * identity(n)), Z)
    # numpy.linalg.eig ne garantit pas l'ordre des valeurs propres : on trie
    # par valeur propre decroissante pour etre sur de garder les 2 premieres
    # composantes principales (ici l'ordre de eig etait deja le bon).
    eigenvalues, eigenvectors = eig(R)
    order = argsort(eigenvalues)[::-1]
    eigenvalues, eigenvectors = eigenvalues[order], eigenvectors[:, order]
    components = [matmul(Z, eigenvectors[:, 0]), matmul(Z, eigenvectors[:, 1])]
    data_reduced = [[components[0][i], components[1][i]] for i in range(n)]
    return data_reduced, eigenvalues, eigenvectors


# ---------------------------------------------------------------------------
# 2a. k-means
# ---------------------------------------------------------------------------
def dist2(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))


def kmeans(points, k, centroids=None, seed=None, max_iter=300):
    """k-means (distance euclidienne), meme principe que la Section 1 :
    affectation au centroide le plus proche puis recalcul des centroides
    jusqu'a stabilite. Retourne (labels, centroids, sse).

    NB : version compacte sans affichage des iterations (167 points).
    TODO fusion : remplacer par la fonction de la Section 1 si elle expose
    les labels des points."""
    if centroids is None:
        centroids = random.Random(seed).sample(points, k)
    centroids = [list(c) for c in centroids]
    labels = None
    for _ in range(max_iter):
        new_labels = [min(range(k), key=lambda j: dist2(pt, centroids[j]))
                      for pt in points]
        if new_labels == labels:
            break
        labels = new_labels
        for j in range(k):
            members = [pt for pt, l in zip(points, labels) if l == j]
            if members:  # un cluster vide garde son centroide
                centroids[j] = [sum(c) / len(members) for c in zip(*members)]
    sse = sum(dist2(pt, centroids[l]) for pt, l in zip(points, labels))
    return labels, centroids, sse


def canonical(labels):
    """Partition sous forme canonique (independante de la numerotation)."""
    groups = {}
    for i, l in enumerate(labels):
        groups.setdefault(l, []).append(i)
    return frozenset(frozenset(g) for g in groups.values())


def plot_kmeans(points, names, labels, centroids, title, path):
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(16, 14))
    for (x, y), name, l in zip(points, names, labels):
        ax.plot(x, y, ".", color=COLORS[l])
        ax.annotate(name, (x, y), fontsize=7, xytext=(2, 0),
                    textcoords="offset points")
    for j, (cx, cy) in enumerate(centroids):
        ax.plot(cx, cy, "x", color=COLORS[j], markersize=12, mew=2)
    ax.set_xlabel("X (1ere composante principale)")
    ax.set_ylabel("Y (2eme composante principale)")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"  -> {path}")


def stability_study(points, k, runs=200):
    """Lance k-means `runs` fois avec centroides initiaux aleatoires et compte
    les partitions differentes obtenues."""
    results = Counter()
    sse_of = {}
    for seed in range(runs):
        labels, _, sse = kmeans(points, k, seed=seed)
        part = canonical(labels)
        results[part] += 1
        sse_of[part] = sse
    print(f"  k={k} : {len(results)} partition(s) differente(s) sur {runs} tirages")
    for part, cnt in results.most_common(5):
        sizes = sorted((len(g) for g in part), reverse=True)
        print(f"    {cnt:4d} fois  SSE={sse_of[part]:8.2f}  tailles={sizes}")
    return results, sse_of


# ---------------------------------------------------------------------------
# 2b. Clustering hierarchique
# ---------------------------------------------------------------------------
def plot_dendrogram(points, names, method, title, path, n_clusters=None):
    import matplotlib.pyplot as plt
    from scipy.cluster import hierarchy
    # Ici on donne directement la liste des points (format "observations"),
    # linkage calcule lui-meme les distances euclidiennes.
    Z = hierarchy.linkage(points, method=method)
    fig, ax = plt.subplots(figsize=(14, 22))
    hierarchy.dendrogram(Z, labels=names, orientation="right", ax=ax,
                         leaf_font_size=7)
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    print(f"  -> {path}")
    if n_clusters:
        cut = hierarchy.fcluster(Z, n_clusters, criterion="maxclust")
        sizes = Counter(cut)
        print(f"  Coupe en {n_clusters} clusters :")
        for c, size in sizes.most_common():
            members = [names[i] for i in range(len(names)) if cut[i] == c]
            shown = ", ".join(members[:8]) + (" ..." if size > 8 else "")
            print(f"    taille {size:3d} : {shown}")
    return Z


# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--csv", default=DEFAULT_CSV)
    parser.add_argument("--show", action="store_true")
    parser.add_argument("--seed", type=int, default=0,
                        help="graine pour les centroides initiaux aleatoires")
    args = parser.parse_args()
    if not args.show:
        matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    os.makedirs(FIG_DIR, exist_ok=True)

    # --- Exercice 1 : preparation ---
    countries, variables, data_country = read_country_data(args.csv)
    print(f"{len(countries)} pays, {len(variables)} variables : {variables}")
    print("data_country commence par :", data_country[:2])
    data_reduced, eigval, eigvec = pca_2d(data_country)
    print("data_reduced commence par :",
          [[round(x, 2) for x in pt] for pt in data_reduced[:2]])
    print(f"Variance expliquee par les 2 composantes : "
          f"{eigval[0] / len(variables):.1%} + {eigval[1] / len(variables):.1%}")
    print("Coefficients (vecteurs propres) des 2 composantes :")
    for v, a, b in zip(variables, eigvec[:, 0], eigvec[:, 1]):
        print(f"  {v:11s} {a:+.2f} {b:+.2f}")

    # --- Exercice 2 : k-means ---
    print("\n=== k-means ===")
    for k in (2, 3):
        labels, centroids, sse = kmeans(data_reduced, k, seed=args.seed)
        sizes = Counter(labels)
        print(f"k={k} (seed={args.seed}) SSE={sse:.2f} tailles="
              f"{[sizes[j] for j in range(k)]}")
        for j in range(k):
            members = [countries[i] for i in range(len(countries)) if labels[i] == j]
            print(f"  cluster {j} ({COLORS[j]}) : {', '.join(members[:10])} ...")
        plot_kmeans(data_reduced, countries, labels, centroids,
                    f"Country : k-means avec k = {k} (SSE = {sse:.2f})",
                    os.path.join(FIG_DIR, f"s3_kmeans_k{k}.png"))

    print("\nSensibilite aux centroides initiaux aleatoires :")
    for k in (2, 3):
        stability_study(data_reduced, k)

    # Verification croisee avec scikit-learn (memes centroides initiaux)
    try:
        from sklearn.cluster import KMeans
        for k in (2, 3):
            labels, _, _ = kmeans(data_reduced, k, seed=args.seed)
            init = random.Random(args.seed).sample(data_reduced, k)
            sk = KMeans(n_clusters=k, n_init=1, init=array(init)).fit(array(data_reduced))
            same = canonical(labels) == canonical(list(sk.labels_))
            print(f"  scikit-learn k={k} : meme partition que notre code -> {same}")
    except ImportError:
        print("  (scikit-learn non installe, verification ignoree)")

    # --- Exercice 2 : hierarchique ---
    print("\n=== Clustering hierarchique ===")
    for method, name in [("single", "Single link"), ("complete", "Complete link")]:
        print(name)
        plot_dendrogram(data_reduced, countries, method,
                        f"Country : clustering hierarchique avec {name}",
                        os.path.join(FIG_DIR, f"s3_{method}.png"), n_clusters=3)

    if args.show:
        plt.show()


if __name__ == "__main__":
    main()
