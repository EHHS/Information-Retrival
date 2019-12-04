import math
from random import randint

resultDic = {}


def randomchar():
    s = randint(10, 20)
    str = ""
    for i in range(0, s):
        str += chr(randint(65, 69))
    return str


def inputstringinfile(filename, x):
    f = open(filename, "w")
    f.write(x)
    f.close()


def readfromfile(filename):
    f = open(filename).read()
    return f


def termfrequency(x):
    d = {}
    for i in range(0, len(x)):
        char = x[i]
        if char in d:
            d[char] += 1
        else:
            d[char] = 1
    del d[" "]
    max = 0
    for i in d:
        if d[i] > max:
            max = d[i]
    for i in d:
        d[i] = d[i] / max
    return d


def idf(a={}, b={}, c={}, e={}, f={}, g={}):
    characters = {"A": 0, "B": 0, "C": 0, "D": 0, "E": 0, "F": 0, "G": 0, "H": 0, "I": 0, "J": 0, "K": 0, "L": 0,
                  "M": 0, "N": 0, "O": 0, "P": 0, "Q": 0, "R": 0, "S": 0, "T": 0,
                  "U": 0, "V": 0, "W": 0, "X": 0, "Y": 0, "Z": 0}
    for i in characters:
        count = 0
        if i in a:
            count += 1
        if i in b:
            count += 1
        if i in c:
            count += 1
        if i in e:
            count += 1
        if i in f:
            count += 1
        if i in g:
            count += 1
        if count == 0:
            characters[i] = 0
        else:
            characters[i] = math.log((6 / count), 2)
    return characters


def idftf(tf={}, idf={}):
    for i in tf:
        if i in idf:
            tf[i] = tf[i] * idf[i]
    return tf


def innerproduct(tf1={}, tf2={}):
    d = 0
    for i in tf1:
        if i in tf2:
            d += tf1[i] * tf2[i]
    return d


def sigmamul(tf1={}):
    d = 0
    for i in tf1:
        d += math.pow(tf1[i], 2)
    return d


def cossim(innerproduct1, multi1, multi2):
    d = (innerproduct1 / (math.sqrt(multi1 * multi2)))
    return d


def main(query):
    d1 = readfromfile("d1.txt")
    d2 = readfromfile("d2.txt")
    d3 = readfromfile("d3.txt")
    d4 = readfromfile("d4.txt")
    d5 = readfromfile("d5.txt")

    d1 = termfrequency(d1)
    d2 = termfrequency(d2)
    d3 = termfrequency(d3)
    d4 = termfrequency(d4)
    d5 = termfrequency(d5)

    query = termfrequency(query)

    idfd = idf(d1, d2, d3, d4, d5, query)

    d1 = idftf(d1, idfd)
    d2 = idftf(d2, idfd)
    d3 = idftf(d3, idfd)
    d4 = idftf(d4, idfd)
    d5 = idftf(d5, idfd)
    query = idftf(query, idfd)
    file1 = {"D1": cossim(innerproduct(d1, query), sigmamul(d1), sigmamul(query)),
             "D2": cossim(innerproduct(d2, query), sigmamul(d2), sigmamul(query)),
             "D3": cossim(innerproduct(d3, query), sigmamul(d3), sigmamul(query)),
             "D4": cossim(innerproduct(d4, query), sigmamul(d4), sigmamul(query)),
             "D5": cossim(innerproduct(d5, query), sigmamul(d5), sigmamul(query))}
    sorted_score = sorted(file1.items(), key=lambda kv: kv[1], reverse=True)
    return sorted_score