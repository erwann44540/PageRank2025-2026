from pyspark import SparkContext, SparkConf
import time

def run_pageRank_rdd(conf, sc, input_path) :
    appName = "MyApp"
    master = "local[*]"

    print("DEBUT RDD")

    distFile = sc.textFile(input_path)
    dico = {}
    map1 = distFile.map(lambda t : (t.split(" ")[0], [t.split(" ")[2]])).reduceByKey(lambda x,y : x+y)
    triplets = distFile.flatMap(lambda t : (t.split(" ")[0], t.split(" ")[1], t.split(" ")[2])).distinct()
    ranks = triplets.map(lambda node: (node, 1.0))

    
    def fusion(liste, nbr):
        ret = []
        for i in liste:
            ret.append((i,nbr))
        return ret

    def func(tuples) :
        urls = tuples[0]
        rank = tuples[1]
        lenurl = len(urls)
        dividedRank = rank/lenurl
        return fusion(urls,dividedRank)

    duration = []
    for i in range(1,6):
        start = time.time()
        flat_map = map1.join(ranks).values().flatMap(func)
        ranks = flat_map.reduceByKey(lambda x,y : x+y).mapValues(lambda z : 0.15 + 0.85 * z)
        duration.append(time.time() - start)
        #sc.cancelAllJobs()

    print("Duration rdd :", duration)

    max = ranks.max(key=lambda t : t[1])

    print("MAX RDD: ", max)
    return duration
