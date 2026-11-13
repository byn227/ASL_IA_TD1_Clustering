# TD Clustering - Data Mining (INSA Centre Val de Loire)

NGUYEN Dinh Huy, NGUYEN Vinh Tri

Le compte rendu est dans `rapport/rapport.pdf`.

## Installation

Les bibliotheques sont installees dans un environnement virtuel :

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Execution

Depuis la racine du projet :

| Commande | Contenu |
|---|---|
| `.venv/bin/python section1_kmeans.py` | Section 1, Exercices 1 a 3 (figures `figures/ex3_*.png`) |
| `.venv/bin/python section1_sklearn.py` | Section 1, Exercice 4 (comparaison avec SciKit-Learn) |
| `.venv/bin/python section1_verifications.py` | Verifications citees dans le compte rendu (Section 1) |
| `.venv/bin/python section2_hierarchique.py` | Section 2 (figures `figures/s2_*.png`) |
| `.venv/bin/python section3_etude_de_cas.py` | Section 3 (figures `figures/s3_*.png`) |

## Fichiers

- `data/Country-data.csv` : jeu de donnees de l'etude de cas
- `figures/` : figures generees par les scripts
- `rapport/` : source LaTeX et PDF du compte rendu
  (compilation : `cd rapport && latexmk -pdf rapport.tex`)
