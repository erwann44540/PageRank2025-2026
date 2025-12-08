from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row
from pyspark.sql.functions import lit
import time

def run_pageRank_dataframe(conf, sc, spark, input_path) :
    appName = "MyApp"
    master = "local[*]"

    print("DEBUT DATAFRAME")

    duration = []
    distFile = sc.textFile(input_path).map(lambda r : (Row(r.split(" ")[0]), Row(r.split(" ")[1]), Row(r.split(" ")[2]))).toDF()

    sel = distFile.select("_1","_3")
    sel = sel.withColumnRenamed("_3", "_2")
    distFile.createOrReplaceTempView("tableA")
    select_cmd = spark.sql("SELECT tableA._1 as _1, 1/count(*) as _3 from tableA GROUP BY tableA._1")

    start = time.time()

    select_cmd = select_cmd.join(sel, "_1")
    temp_state = select_cmd
    select_cmd = select_cmd.groupby("_2").sum("_3")
    select_cmd = select_cmd.withColumnRenamed("sum(_3)", "_3")
    select_cmd = select_cmd.withColumn('_3', 0.15+0.85*select_cmd._3)
    select_cmd = select_cmd.withColumnRenamed("_2", "_1")

    temp_state = temp_state.withColumnRenamed("_3", "_4")
    duration.append(time.time() - start)
    for i in range(1,5) :
        start = time.time()
        select_cmd = select_cmd.join(temp_state, "_1")
        select_cmd = select_cmd.withColumn('_3', select_cmd._3*select_cmd._4)
        select_cmd = select_cmd.groupby("_2").sum("_3")
        select_cmd = select_cmd.withColumnRenamed("sum(_3)", "_3")
        select_cmd = select_cmd.withColumn('_3', 0.15+0.85*select_cmd._3)
        select_cmd = select_cmd.withColumnRenamed("_2", "_1")
        duration.append(time.time() - start)
        #sc.cancelAllJobs()

    print("Duration dataframe : ", duration)
    max_row = select_cmd.agg({"_3": "max"}).collect()[0][0]
    print("MAX DATAFRAME :", max_row)

    return duration