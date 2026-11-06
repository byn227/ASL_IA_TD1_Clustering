import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from section1_kmeans import kmeans

# Lecture des donnees
rows = list(csv.reader(open("data/Country-data.csv")))[1:]
countries = [r[0] for r in rows]
X = np.array([[float(v) for v in r[1:]] for r in rows])

# PCA
Z = (X - X.mean(axis=0)) / X.std(axis=0)
R = Z.T @ Z / len(X)
eigenvectors = np.linalg.eig(R)[1]
data_reduced = (Z @ eigenvectors[:, :2]).tolist()

# k-means
for k in [2, 3]:
    sse, clusters = kmeans(data_reduced, k, retourner_clusters=True)
    plt.figure(figsize=(14, 14))
    for cl in clusters:
        plt.plot([p[0] for p in cl], [p[1] for p in cl], ".")
    for name, (x, y) in zip(countries, data_reduced):
        plt.annotate(name, (x, y), fontsize=8)
    plt.title(f"k-means k = {k}")
    plt.savefig(f"figures/s3_kmeans_k{k}.png")

# Clustering hierarchique
for method in ["single", "complete"]:
    plt.figure(figsize=(10, 22))
    hierarchy.dendrogram(hierarchy.linkage(data_reduced, method=method),
                         labels=countries, orientation="right")
    plt.title(f"{method} link")
    plt.savefig(f"figures/s3_{method}.png")
