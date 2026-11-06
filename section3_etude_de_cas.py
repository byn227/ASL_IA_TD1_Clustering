import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from section1_kmeans import kmeans, COULEURS

# Lecture des donnees
with open("data/Country-data.csv") as f:
    rows = list(csv.reader(f))[1:]
countries = [r[0] for r in rows]
X = np.array([[float(v) for v in r[1:]] for r in rows])

# PCA sur les donnees centrees reduites
Z = (X - X.mean(axis=0)) / X.std(axis=0)
R = Z.T @ Z / len(X)
eigenvectors = np.linalg.eig(R)[1]
data_reduced = (Z @ eigenvectors[:, :2]).tolist()
print("data_reduced commence par", np.round(data_reduced[:2], 2).tolist())

# k-means (Figures 1 et 2)
for k in [2, 3]:
    sse, clusters = kmeans(data_reduced, k, retourner_clusters=True)
    plt.figure(figsize=(14, 14))
    for j, cl in enumerate(clusters):
        couleur = COULEURS[j % len(COULEURS)]
        plt.plot([p[0] for p in cl], [p[1] for p in cl], ".", color=couleur)
        centroide = np.mean(cl, axis=0)
        plt.plot(centroide[0], centroide[1], "x", color=couleur,
                 markersize=12, markeredgewidth=2)
    for name, (x, y) in zip(countries, data_reduced):
        plt.annotate(name, (x, y), fontsize=8)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title(f"Jeu de donnees Country : k-means avec k = {k}")
    plt.savefig(f"figures/s3_kmeans_k{k}.png")

# Clustering hierarchique (Figures 3 et 4)
for method in ["single", "complete"]:
    plt.figure(figsize=(10, 22))
    hierarchy.dendrogram(hierarchy.linkage(data_reduced, method=method),
                         labels=countries, orientation="right")
    plt.title(f"Jeu de donnees Country : clustering hierarchique avec {method.capitalize()} link")
    plt.savefig(f"figures/s3_{method}.png")

plt.show()
