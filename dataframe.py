from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row
from pyspark.sql.functions import lit
import time

def run_pageRank_dataframe(conf, sc, spark) :
    appName = "MyApp"
    master = "local[*]"

    def plus_mean(pandas_df):
        return pandas_df.assign(_1=pandas_df._1 - pandas_df._1.mean())

    duration = []

    distFile = sc.textFile("20000_first_lines.ttl").map(lambda r : (Row(r.split(" ")[0]), Row(r.split(" ")[1]), Row(r.split(" ")[2]))).toDF()

    sel = distFile.select("_1","_3")
    sel = sel.withColumnRenamed("_3", "_2")
    distFile.createOrReplaceTempView("tableA")
    mewtwo = spark.sql("SELECT tableA._1 as _1, 1/count(*) as _3 from tableA GROUP BY tableA._1")
    tests = spark.sql("SELECT tableA._1 as _1, 1/count(*) as _3 from tableA GROUP BY tableA._1")

    start = time.time()

    tests = tests.join(sel, "_1")
    mew = tests
    tests = tests.groupby("_2").sum("_3")
    tests = tests.withColumnRenamed("sum(_3)", "_3")
    tests = tests.withColumn('_3', 0.15+0.85*tests._3)
    tests = tests.withColumnRenamed("_2", "_1")

    mew = mew.withColumnRenamed("_3", "_4")
    duration.append(time.time() - start)
    spark.interruptAll()
    for i in range(1,5) :
        start = time.time()
        tests = tests.join(mew, "_1")
        print(tests.show())
        tests = tests.withColumn('_3', tests._3*tests._4)
        tests = tests.groupby("_2").sum("_3")
        tests = tests.withColumnRenamed("sum(_3)", "_3")
        tests = tests.withColumn('_3', 0.15+0.85*tests._3)
        tests = tests.withColumnRenamed("_2", "_1")
        duration.append(time.time() - start)
        spark.interruptAll()
        sc.cancelAllJobs()

    print(duration)
    return duration
    #suite = tests.join ("")
    """print(sel.show())
    rank = sel.select("_1")
    rank = rank.withColumn('_3', lit(1))
    rank = rank.groupBy("_1").avg()
    rank = rank.withColumnRenamed("avg(_3)", "_3")
    print(rank.show())
    print(rank._3)
    rank = rank.join(sel,"_1")
    print(rank.show())"""