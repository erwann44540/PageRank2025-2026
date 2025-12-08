# PageRank2025-2026

Projet du module de Gestion des données distribuées à large échelle

## Groupe

- Martin HECKEL
- Erwann CUSSAGUET
- Quentin TEGNY

## Structure du projet

### Python

Plusieurs fichiers Python :
- `rdd.py` : exécute le pagerank sur le RDD
- `dataframe.py` : exécute le pagerank sur le dataframe
- `diagramme.py` : génère les graphes avec matplotlib

### Scripts Bash

Plusieurs scripts bash :
- `creater_cluster.sh` : crée un cluster
- `delete_cluster.sh` : supprime un cluster
- `run.sh` : fait tourner toutes les expérimentations
- `submit_job.sh` : run sur GCloud

## Graphiques

_NOTE : Les graphiques ont été réalisés avec 1% du dataframe originel, ce qui fait que les graphiques ont des valeurs plutôt faibles_

![Diagramme pour 3 noeuds](/diagrams/pagerank_graph_3nodes.png "Diagramme pour 3 noeuds")

![Diagramme pour 4 noeuds](/diagrams/pagerank_graph_4nodes.png "Diagramme pour 4 noeuds")

![Diagramme pour 6 noeuds](/diagrams/pagerank_graph_6nodes.png "Diagramme pour 6 noeuds")

