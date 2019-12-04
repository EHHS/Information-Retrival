from flask import Flask
from random import randint




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


def countstring(x):
    return len(x)


def countchar(x):
    d = {}
    for i in range(0, len(x)):
        char = x[i]
        if char in d:
            d[char] += 1
        else:
            d[char] = 1
    return d


def divide(z, x={}):
    for i in x:
        x[i] = round(x[i] / z, 2)
    return x


def innerProduct(x={}, q={}, fileName=''):
    resultDic = {}
    result = 0
    for key in q.keys():
        if key in x.keys():
            result += (float(q[key]) * float(x[key]))

    resultDic[fileName] = result
    return resultDic


dm = []
for i in range(0, 3):
    a = randomchar()
    (inputstringinfile("text" + str(i + 1) + ".txt", a))
    dm.append(a)

l = []
for i in dm:
    y = countchar(i)
    z = countstring(i)
    y=divide(z, y)
    l.append(y)

dic = {}
n = input("enter the query ")
# for x in range(n):
#     key= input("Enter the Key ")
#     dic[key]= input("Enter the Value ")
Local_dic = n.split(";")

for item in Local_dic:
    inner = item.split(":")
    dic[inner[0]] = float(inner[1])
o=0
result=[]
for i in l:
    o+=1
    print(innerProduct(i, dic, "d"+str(o)))
