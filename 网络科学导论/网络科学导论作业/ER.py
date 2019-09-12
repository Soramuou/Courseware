#!-*- coding:utf-8 -*-
# __author__ : Sora
# ___time___ : 2019/06/24/9:06

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random
import time
import formula





# 生成ER网络
def generateRandomNetwork():
    count = 0
    probability = 0.0
    for i in range(NETWORK_SIZE):
        for j in range(i + 1, NETWORK_SIZE):
            probability = random.random()
            if probability < PROBABILITY_OF_EAGE:
                count = count + 1
                adjacentMatrix[i][j] = adjacentMatrix[j][i] = 1
    print('您所构造的ER网络边数为：' + str(count))

# 用于绘制ER图
def showGraph():
    G = nx.Graph()
    for i in range(len(adjacentMatrix)):
        G.add_node(i)
        for j in range(len(adjacentMatrix)):
            if adjacentMatrix[i][j] == 1:
                G.add_edge(i, j)
    nx.draw(G,pos=nx.random_layout(G), node_size=3,width=0.05)
    print("density:",formula.density(G))
    print("clustering coefficient:",formula.clustering_coefficient(G))
    a= formula.average_path_length(G)
    print('nx.shortest_path_length(G):',a)
    plt.savefig("ER.png", dpi=300)
    plt.show()



# 将ER网络写入文件中
def writeRandomNetworkToFile():
    ARRS = []
    f = open('randomNetwork01.txt', 'w+')
    for i in range(NETWORK_SIZE):
        t = adjacentMatrix[i]
        ARRS.append(t)
        for j in range(NETWORK_SIZE):
            s = str(t[j])
            f.write(s)
            f.write(' ')
        f.write('\n')
    f.close()


# 计算度分布并将其存入文件中
def calculateDegreeDistribution():
    averageDegree = 0.0
    identify = 0.0
    statistic = np.zeros((NETWORK_SIZE), dtype=float)  # statistic将用于存放度分布的数组，数组下标为度的大小，对应数组内容为该度的概率
    degree = np.zeros((NETWORK_SIZE), dtype=int)  # degree用于存放每个节点的度
    for i in range(NETWORK_SIZE):
        for j in range(NETWORK_SIZE):
            degree[i] = degree[i] + adjacentMatrix[i][j]
    for i in range(NETWORK_SIZE):
        averageDegree += degree[i]
    print('平均度为' + str(averageDegree / NETWORK_SIZE))  # 计算平均度
    for i in range(NETWORK_SIZE):
        statistic[degree[i]] = statistic[degree[i]] + 1
    for i in range(NETWORK_SIZE):
        statistic[i] = statistic[i] / NETWORK_SIZE
        identify = identify + statistic[i]
    identify = int(identify)
    print('如果output为1则该算法正确\toutput=' + str(identify))  # 用于测试算法是否正确



# 主程序开始
print('请输入ER网络的顶点个数：')
NETWORK_SIZE = int(input())
adjacentMatrix = np.zeros((NETWORK_SIZE, NETWORK_SIZE), dtype=int)  # 初始化邻接矩阵


print('请输入连边概率：')
PROBABILITY_OF_EAGE = float(input())
generateRandomNetwork()  # 生成ER随机网络

random.seed(time.time())  # 'random.random()#生成[0,1)之间的随机数

writeRandomNetworkToFile()  # 将随机网络写入randomNetwork01.txt文件中
calculateDegreeDistribution()  # 计算此ER随机网络的度分布并将结果写入文件degreee01.txt文件中

print('您所构造的ER网络如下：')
showGraph()

