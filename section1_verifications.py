import contextlib
import io
import itertools
import random
from collections import Counter

from section1_kmeans import kmeans, calculer_centroides, calculer_sse

# Affichages attendus, recopies de l'enonce (Exercice 1)
ATTENDU_INIT_1_2_18 = """Iteration 1
Centroid [1]  Points [[1]]
Centroid [2]  Points [[2]]
Centroid [18]  Points [[18], [20], [31]]
Iteration 2
Centroid [1.0]  Points [[1]]
Centroid [2.0]  Points [[2]]
Centroid [23.0]  Points [[18], [20], [31]]
Fin clustering, erreur =  98.0
"""

ATTENDU_INIT_18_20_31 = """Iteration 1
Centroid [18]  Points [[1], [2], [18]]
Centroid [20]  Points [[20]]
Centroid [31]  Points [[31]]
Iteration 2
Centroid [7.0]  Points [[1], [2]]
Centroid [20.0]  Points [[18], [20]]
Centroid [31.0]  Points [[31]]
Iteration 3
Centroid [1.5]  Points [[1], [2]]
Centroid [19.0]  Points [[18], [20]]
Centroid [31.0]  Points [[31]]
Fin clustering, erreur =  2.5
"""


def kmeans_silencieux(data, k, centroides_initiaux=None):
    """Retourne (affichage, SSE, clusters) sans rien afficher."""
    sortie = io.StringIO()
    with contextlib.redirect_stdout(sortie):
        sse, clusters = kmeans(data, k, centroides_initiaux, retourner_clusters=True)
    return sortie.getvalue(), sse, clusters


def sse_partition(clusters):
    """SSE d'une partition, centroides = moyennes des clusters."""
    return calculer_sse(clusters, calculer_centroides(clusters, [None] * len(clusters)))


if __name__ == "__main__":
    data1 = [[1], [2], [18], [20], [31]]
    print("=== Exercice 1 : comparaison avec l'affichage de l'enonce ===")
    for init, attendu in [([[1], [2], [18]], ATTENDU_INIT_1_2_18),
                          ([[18], [20], [31]], ATTENDU_INIT_18_20_31)]:
        affichage, _, _ = kmeans_silencieux(data1, 3, init)
        print(f"  init {init} : affichage identique a l'enonce :", affichage == attendu)

    print("\n=== Exercice 1 : centroides initiaux tires au hasard (graines 0 a 199) ===")
    compte = Counter()
    for graine in range(200):
        random.seed(graine)
        _, sse, _ = kmeans_silencieux(data1, 3)
        compte[sse] += 1
    for sse, nb in sorted(compte.items()):
        print(f"  SSE = {sse} : {nb} fois sur 200 ({100 * nb / 200:.0f} %)")

    print("\n=== Exercice 1 : les C(5,3) = 10 choix possibles de 3 centroides initiaux ===")
    for init in itertools.combinations(data1, 3):
        _, sse, _ = kmeans_silencieux(data1, 3, list(init))
        print(f"  init {list(init)} : SSE = {sse}")

    data2 = [[2], [4], [6], [12], [24], [30]]
    print("\n=== Exercice 2 : les 5 coupures en 2 intervalles (optimum en 1D) ===")
    for i in range(1, len(data2)):
        clusters = [data2[:i], data2[i:]]
        print(f"  {[p[0] for p in clusters[0]]} | {[p[0] for p in clusters[1]]} : SSE = {sse_partition(clusters):.1f}")

    print("\n=== Exercice 2 (a) : egalite du point [4] a l'iteration 1 ===")
    print("  notre regle (premier centroide) : clusters {2, 4} | {6, 12, 24, 30}")
    autre = [[[2]], [[4], [6], [12], [24], [30]]]
    centroides = calculer_centroides(autre, [None, None])
    _, sse, _ = kmeans_silencieux(data2, 2, centroides)
    print(f"  autre choix (second centroide) : clusters {{2}} | {{4, 6, 12, 24, 30}},"
          f" centroides {centroides} -> SSE finale = {sse}")
