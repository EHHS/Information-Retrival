from flask import Flask, redirect, url_for, request, render_template
import numpy as np
import math
from random import randint

resultDic = {}


def randomchar():
    s = randint(10, 20)
    str = ""
    for i in range(0, s):
        str += chr(randint(65, 69)) + " "
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
    result = ''.join(i for i in x if not i.isdigit())
    for i in range(0, len(result)):
        char = result[i]
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


def main1(query):
    dm = []
    for i in range(1, 6):
        dm.append(readfromfile("d" + str(i) + ".txt"))

    for i in range(0, len(dm)):
        dm[i] = termfrequency(dm[i])

    query = termfrequency(query)

    idfd = idf(dm[0], dm[1], dm[2], dm[3], dm[4], query)

    for i in range(0, len(dm)):
        dm[i] = idftf(dm[i], idfd)

    query = idftf(query, idfd)
    file = {}
    for i in range(0, len(dm)):
        file.update(
            {("D" + str(i + 1)): round(cossim(innerproduct(dm[i], query), sigmamul(dm[i]), sigmamul(query)), 2)})
    sorted_score = sorted(file.items(), key=lambda kv: kv[1], reverse=True)

    return sorted_score


def main(query):
    file2 = ["cossim =" + str(main1(query)), str(authority())]
    return file2


def create_matrix_with_val():
    matrix = []
    x = 1
    for i in range(0, 5):
        matrix.append([])
        f = readfromfile("d" + str(x) + ".txt")
        x += 1
        for j in range(1, 6):
            if (i + 1) == j:
                matrix[i].append(0)
            else:
                if str(j) in f:
                    matrix[i].append(1)
                else:
                    matrix[i].append(0)

    return matrix


def authority():
    original = create_matrix_with_val()

    hub_vector = np.array([1, 1, 1, 1, 1])

    mx = np.array(original)
    adjacenttranspose = np.array(mx).T
    A = np.dot(adjacenttranspose, hub_vector)
    hub2 = np.dot(mx, A)

    i = 0

    while i < 20000:
        titration = A
        titrationhub = hub2
        A_normalized = np.divide(A, math.sqrt(np.sum(np.square(A))))
        hub_normalized = np.divide(hub2, math.sqrt(np.sum(np.square(hub2))))
        A = np.dot(adjacenttranspose, hub_normalized)
        hub2 = np.dot(mx, A_normalized)
        print(np.max(np.subtract(titration, A)))
        if np.max(abs(np.subtract(titration, A))) < 0.0001:
            print(i)
            break
        i += 1

    file = {}
    for i in range(0, 5):
        file.update({("D" + str(i + 1)): round(A_normalized[i], 2)})
    sorted_score = sorted(file.items(), key=lambda kv: kv[1], reverse=True)
    file2 = {}
    for i in range(0, 5):
        file.update({("D" + str(i + 1)): round(hub_normalized[i], 2)})
    sorted_score2 = sorted(file.items(), key=lambda kv: kv[1], reverse=True)
    file3 = ["Authority = " + str(sorted_score), "Hub = " + str(sorted_score2)]

    return file3


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/', methods=['POST', 'GET'])
def start():
    if request.method == 'POST':
        query = request.form['query']
        return render_template("result.html", list=main(query))


app.run(debug=True)
