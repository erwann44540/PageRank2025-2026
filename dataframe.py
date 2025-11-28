from pyspark import SparkContext, SparkConf
from pyspark.sql import SparkSession
from datetime import datetime, date
import pandas as pd
from pyspark.sql import Row
from pyspark.sql.functions import lit

appName = "MyApp"
master = "local[*]"

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)
spark = SparkSession(sc)

def plus_mean(pandas_df):
    return pandas_df.assign(_1=pandas_df._1 - pandas_df._1.mean())

distFile = sc.textFile("20000_first_lines.ttl").map(lambda r : (Row(r.split(" ")[0]), Row(r.split(" ")[1]), Row(r.split(" ")[2]))).toDF()

sel = distFile.select("_1","_2")
sel.createOrReplaceTempView("tableA")
tests = spark.sql("SELECT count(*) as _3 from tableA GROUP BY tableA._1")
print(sel.show())
rank = sel.select("_1")
rank = rank.withColumn('_2', lit(1))
print(rank.show())
print(tests.show())
print(tests._3)
print(rank._2)
rank = rank.withColumn('_2', rank._2+tests._3)
#print(rank.show())