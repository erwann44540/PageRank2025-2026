import matplotlib.pyplot as plt
from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
import numpy as np
from rdd import run_pageRank_rdd
from dataframe import run_pageRank_dataframe

appName = "MyApp"
master = "local[*]"

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

duration_rdd = run_pageRank_rdd(conf, sc)
duration_df = run_pageRank_dataframe(conf, sc, spark)

n_iter = min(len(duration_rdd), len(duration_df))
iterations = list(range(1, n_iter + 1))

x = np.arange(n_iter)
width = 0.35

plt.figure(figsize=(8, 6))

plt.bar(x - width / 2, duration_rdd[:n_iter], width, label="PageRank avec RDD")
plt.bar(x + width / 2, duration_df[:n_iter], width, label="PageRank avec DataFrame")

plt.xlabel("Itérations")
plt.ylabel("Temps d'exécution (s)")
plt.title("Temps d'exécution PageRank")
plt.xticks(x, iterations)
plt.legend()

plt.tight_layout()
plt.savefig("pagerank_graph.png")
plt.show()