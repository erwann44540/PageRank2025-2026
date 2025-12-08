import argparse
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

import subprocess

from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession

from rdd import run_pageRank_rdd
from dataframe import run_pageRank_dataframe


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--input",
        required=True,
        help="Chemin du fichier TTL sur GCS (ex: gs://page-rank-ce/data/wikilinks_lang=en.ttl.bz2)",
    )
    parser.add_argument(
        "--output",
        required=False,
        help="Préfixe de sortie GCS pour le graphe (ex: gs://page-rank-ce/outputs/diagramme-3nodes-XXXX)",
    )
    args = parser.parse_args()

    input_path = args.input
    output_prefix = args.output

    print("Fichier TTL utilisé :", input_path)

    appName = "MyApp"

    conf = SparkConf().setAppName(appName)
    sc = SparkContext.getOrCreate(conf=conf)
    spark = SparkSession(sc)

    duration_rdd = run_pageRank_rdd(conf, sc, input_path)
    duration_df = run_pageRank_dataframe(conf, sc, spark, input_path)

    print("Durations RDD:", duration_rdd)
    print("Durations DataFrame:", duration_df)

    n_iter = min(len(duration_rdd), len(duration_df))
    if n_iter > 0:
        iterations = list(range(1, n_iter + 1))
        x = np.arange(n_iter)
        width = 0.35

        plt.figure(figsize=(8, 6))

        plt.bar(x - width / 2, duration_rdd[:n_iter], width, label="PageRank avec RDD")
        plt.bar(x + width / 2, duration_df[:n_iter], width, label="PageRank avec DataFrame")

        plt.xlabel("Itérations")
        plt.ylabel("Temps d'exécution (s)")
        plt.title("Temps d'exécution PageRank (RDD vs DataFrame)")
        plt.xticks(x, iterations)
        plt.legend()
        plt.tight_layout()

        png_name = "pagerank_graph.png"
        plt.savefig(png_name)
        print(f"Graphe sauvegardé localement dans le driver sous le nom : {png_name}")

        if output_prefix:
            output_prefix = output_prefix.rstrip("/")
            gcs_path = f"{output_prefix}/pagerank_graph.png"

            try:
                subprocess.run(["gsutil", "cp", png_name, gcs_path], check=True)
                print(f"Diagramme envoyé sur GCS : {gcs_path}")
            except Exception as e:
                print(f"Échec de l'envoi du diagramme sur GCS ({gcs_path}) : {e}")
    else:
        print("Aucune durée récupérée, graphe non généré.")

    spark.stop()
    sc.stop()
