import os
import numpy as np
import math

def loadData():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "真实影片评分数据集", "ml-100k", "u.data")
    # print("Trying to open:", file_path)
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"File does not exist: {file_path}")
    data = []
    with open(file_path, 'r') as f:
        for i in range(100000):
            h = f.readline().strip().split('\t')
            if not h or len(h) < 3:
                break
            h = list(map(int, h))
            data.append(h[0:3])
    return data

def loadMovieName():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, "真实影片评分数据集", "ml-100k", "u.item")
    # print("Trying to open:", file_path)
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"File does not exist: {file_path}")
    name = []
    with open(file_path, encoding='ISO-8859-1') as f:
        for i in range(1682):
            h = f.readline()
            k = ''
            m = 0
            for j in range(len(h)):
                k += h[j]
                if h[j] == '|':
                    m += 1
                if m == 2:
                    break
            name.append(k)
    return name


def manageDate(data):
    outdata = []
    for i in range(943):
        outdata.append([])
        for j in range(1682):
            outdata[i].append(0)
    for h in data:
        outdata[h[0] - 1][h[1] - 1] = h[2]
    return outdata


def calcMean(x, y):
    sum_x = sum(x)
    sum_y = sum(y)
    n = len(x)
    x_mean = float(sum_x + 0.0) / n
    y_mean = float(sum_y + 0.0) / n
    return x_mean, y_mean


def calcPearson(x, y):
    x_mean, y_mean = calcMean(x, y)
    n = len(x)
    sumTop = 0.0
    sumBottom = 0.0
    x_pow = 0.0
    y_pow = 0.0
    for i in range(n):
        sumTop += (x[i] - x_mean) * (y[i] - y_mean)
    for i in range(n):
        x_pow += math.pow(x[i] - x_mean, 2)
    for i in range(n):
        y_pow += math.pow(y[i] - y_mean, 2)
    sumBottom = math.sqrt(x_pow * y_pow)
    p = sumTop / sumBottom
    return p


def calcAttribute(dataSet, num):
    prr = []
    n, m = np.shape(dataSet)
    x = [0] * m 
    y = [0] * m
    y = dataSet[num - 1]
    for j in range(n): 
        x = dataSet[j]
        prr.append(calcPearson(x, y))
    return prr


def choseMovie(outdata, num):
    prr = calcAttribute(outdata, num)
    list=[]
    mid=[]
    out_list=[]
    movie_rank=[]
    for i in range(1682):
        movie_rank.append([i,0])
    k=0
    for i in range(943):
        list.append([i,prr[i]])
    for i in range(943):
        for j in range(942-i):
            if list[j][1]<list[j+1][1]:
                mid=list[j]
                list[j]=list[j+1]
                list[j+1]=mid
    for i in range(1,51):
        for j in range(0,1682):
            movie_rank[j][1]=movie_rank[j][1]+outdata[list[i][0]][j]*list[i][1]/50
    for i in range(1682):
        for j in range(1681-i):
            if movie_rank[j][1]<movie_rank[j+1][1]:
                mid=movie_rank[j]
                movie_rank[j]=movie_rank[j+1]
                movie_rank[j+1]=mid
    for i in range(1,1682):
        if(outdata[num-1][movie_rank[i][0]]==0):
            mark=0
            for d in out_list:
                if d[0]==j:
                        mark=1
                if mark!=1:
                    k+=1
                    out_list.append(movie_rank[i])
            if k==10:
                break
    return movie_rank

def printMovie(out_list,name):
    print("base on the data we think you may like those movies:")
    for i in range(10):
        print(name[out_list[i][0]]," rank score:",out_list[i][1])


i_data = loadData()
name = loadMovieName()
out_data = manageDate(i_data)
a = eval(input("please input the id of user:"))
out_list = choseMovie(out_data, a)
printMovie(out_list,name)
