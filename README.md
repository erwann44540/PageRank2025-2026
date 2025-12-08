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

_NOTE :_

- _Les graphiques ont été réalisés avec 1% du dataframe originel, ce qui fait que les graphiques ont des valeurs plutôt faibles_
- _Toutes les exécutions ont été effectué avec 5 itérations._

### Diagramme pour 3 noeuds

![Diagramme pour 3 noeuds](/diagrams/pagerank_graph_3nodes.png "Diagramme pour 3 noeuds")

Max : <http://dbpedia.org/resource/FIFA> (RDD : 166.1415274865461 / DF : 166.14152748654607)

### Diagramme pour 4 noeuds 

![Diagramme pour 4 noeuds](/diagrams/pagerank_graph_4nodes.png "Diagramme pour 4 noeuds")

Max : <http://dbpedia.org/resource/FIFA> (RDD : 166.1415274865461 / DF : 166.14152748654604)

### Diagramme pour 6 noeuds 

![Diagramme pour 6 noeuds](/diagrams/pagerank_graph_6nodes.png "Diagramme pour 6 noeuds")

Max : <http://dbpedia.org/resource/FIFA> (RDD : 166.1415274865461 / DF : 166.14152748654604)

### Observations

Ici, nous pouvons voir que pour un diagramme avec 4 noeuds celui-ci est plus rapide pour le RDD que celui avec le 3 et 6 noeuds qui correspond que pour les datas sélectionnés, lorsque nous avons trop de noeuds, le temps réaugmente. 

Pour le dataframe, le 6 noeud est plus adapté d'après les graphiques. 

Dans tout les cas, le RDD est plus rapide (en moyenne) que le dataframe et tout les deux donnent des page ranks max proche. 

## Page Rank 

Nous pouvons observer que le page rank pour les deux cas explosent lorsque les données augmentent. Ce résultat est suite à notre choix de prendre en compte la formule du cours et de l'appliquer. En théorique dans un Page Rank, le max est proche de 1 car les variables fixes issues du cours sont automatiquement modifier selon l'évolution des itérations. 


