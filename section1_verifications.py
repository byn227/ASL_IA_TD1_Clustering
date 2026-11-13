#!/usr/bin/env python3
"""TD Clustering - Section 1 : verification de l'affichage de l'Exercice 1.

Compare l'affichage de notre fonction kmeans avec celui donne dans l'enonce,
pour les deux configurations de centroides initiaux de l'Exercice 1.

Usage :
    .venv/bin/python section1_verifications.py
"""

import contextlib
import io

from section1_kmeans import kmeans

# Affichages attendus, recopies de l'enonce
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


if __name__ == "__main__":
    data1 = [[1], [2], [18], [20], [31]]
    for init, attendu in [([[1], [2], [18]], ATTENDU_INIT_1_2_18),
                          ([[18], [20], [31]], ATTENDU_INIT_18_20_31)]:
        sortie = io.StringIO()
        with contextlib.redirect_stdout(sortie):
            kmeans(data1, 3, init)
        print(f"init {init} : affichage identique a l'enonce : {sortie.getvalue() == attendu}")
