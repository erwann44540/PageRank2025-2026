from pyspark import SparkContext, SparkConf

appName = "MyApp"
master = "local[*]"

conf = SparkConf().setAppName(appName).setMaster(master)
sc = SparkContext(conf=conf)

distFile = sc.textFile("20000_first_lines.ttl")

#print(distFile.collect())
dico = {}

def f(a):
    key2 = a.split(" ")[0]
    value2 = a.split(" ")[2]
    if key in dico:
        dico[key].append(value)
        return a.split(" ")[0], a.split(" ")[2]
    else:
        dico[key] = [value]
        return a.split(" ")[0], a.split(" ")[2]

def fqdklsmjf(x, y):
    list = []
    if x[0] == y[0] :
        list = [x[1],y[1]]
        return (x[0], list)
    else :
        return (x[0], x[1])

test2 = distFile.map(lambda t : (t.split(" ")[0], [t.split(" ")[2]])).reduceByKey(lambda x,y : x+y)
test4 = distFile.map(f)
test3 = distFile.map(lambda t : (t.split(" ")[0])).distinct()

#print(test2.collect())

for i in test2.collect():
    key = i[0]
    value = i[1]
    if key in dico:
        dico[key].append(value)
    else:
        dico[key] = [value]

#test4 = test2.join(test3)
def afficher_dico(dico):
    cpt=1
    for key, values in dico.items():
        print(f"Clé {cpt} {key} :")
        for value in values:
            print(f"  - {value}")
        cpt += 1

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

def ecrire_map(liste, filename):
    cpt=1
    with open(filename, 'w', -1, "utf-8") as f:
        for tpl1, liste_values in liste:
            f.write(f"Tuple {cpt} - {tpl1} :\n")
            for value in liste_values:
                f.write(f"  - {value}\n")
            cpt += 1
        f.write(f"Nombre total de clés : {len(liste)}")

#ecrire_map(test2.collect(), 'map_output.txt')
#print(test4.collect())
test = distFile.flatMap(lambda t : (t.split(" ")[0], t.split(" ")[1], t.split(" ")[2])).distinct()

#print(test.collect())

ranks = test.map(lambda node: (node, 1.0))

#print (ranks.collect())
def fusion(liste, nbr):
    ret = []
    for i in liste:
        ret.append((i,nbr))
    return ret
#ranks.saveAsTextFile('rank')
def func (tuples) :
    urls = tuples[0]
    rank = tuples[1]
    lenurl = len(urls)
    dividedRank = rank/lenurl
    return fusion(urls,dividedRank)

biboup = test2.join(ranks).values().flatMap(func)
#biboup = test2.join(ranks).values().flatMap(lambda urls,rank : (urls.map(lambda dest : (dest, rank/len(urls)))))

biboup.saveAsTextFile('biboup3')
kqldfjhsdfg = biboup.reduceByKey(lambda x,y : x+y).mapValues(lambda z : 0.15 + 0.85 * z)
print(kqldfjhsdfg.collect())
kqldfjhsdfg.saveAsTextFile('winoupawin')
iter = 5

#contribs = test2.join(ranks).values().flatMap(lambda case : case.map(lambda dest : (dest, case[1]/case[0].size())))

#print (contribs.collect())
