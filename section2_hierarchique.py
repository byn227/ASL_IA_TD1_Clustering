import numpy as np
import matplotlib.pyplot as plt
from scipy.cluster import hierarchy
from scipy.spatial.distance import squareform

labels = ["p1", "p2", "p3", "p4", "p5"]

# 1) Matrice de distance
dist1 = [0.1, 0.9, 0.35, 0.8, 0.3, 0.4, 0.5, 0.6, 0.7, 0.2]

# 2) Matrice de similarite -> distance = 1 - similarite
sim = np.array([
    [1.00, 0.10, 0.41, 0.55, 0.35],
    [0.10, 1.00, 0.64, 0.47, 0.98],
    [0.41, 0.64, 1.00, 0.44, 0.85],
    [0.55, 0.47, 0.44, 1.00, 0.76],
    [0.35, 0.98, 0.85, 0.76, 1.00],
])
dist2 = squareform(1 - sim, checks=False)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for i, d in enumerate([dist1, dist2]):
    for j, method in enumerate(["single", "complete"]):
        Z = hierarchy.linkage(d, method=method)
        hierarchy.dendrogram(Z, labels=labels, ax=axes[i, j])
        axes[i, j].set_title(f"Matrice {i + 1} - {method} link")

plt.tight_layout()
plt.show()
