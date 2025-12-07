from pyspark import SparkContext, SparkConf
import time

def run_pageRank_rdd(conf, sc) :
    appName = "MyApp"
    master = "local[*]"

    distFile = sc.textFile("20000_first_lines.ttl")
    dico = {}
    map1 = distFile.map(lambda t : (t.split(" ")[0], [t.split(" ")[2]])).reduceByKey(lambda x,y : x+y)

    for i in map1.collect():
        key = i[0]
        value = i[1]
        if key in dico:
            dico[key].append(value)
        else:
            dico[key] = [value]

    def ecrire_dico(dico, filename):
        cpt=1
        with open(filename, 'w', -1, "utf-8") as f:
            for key, values in dico.items():
                f.write(f"Clé {cpt} - {key} :\n")
                for value in values:
                    f.write(f"  - {value}\n")
                cpt += 1
            f.write(f"Nombre total de clés : {len(dico)}")

    ecrire_dico(dico, "avecdistinct")

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
        sc.cancelAllJobs()

    print(duration)
    return duration
