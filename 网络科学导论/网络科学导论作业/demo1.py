#!-*- coding:utf-8 -*-
# __author__ : Sora
# ___time___ : 2019/06/23/16:34


import networkx as nx
import matplotlib.pyplot as plt

G = nx.DiGraph()
G.add_node(1)
G.add_node(2)                  # 加点
G.add_nodes_from([3, 4, 5, 6])    # 加点集合
G.add_cycle([1, 2, 3, 4])         # 加环
G.add_edge(1, 3)
G.add_edges_from([(3, 5), (3, 6), (6, 7)])  # 加边集合
for node in G.nodes():
    print(G.out_degree(node))
print("nodes:", G.nodes())      # 输出全部的节点： [1, 2, 3]
print("edges:", G.edges())    # 输出全部的边：[(2, 3)]
print("number of edges:", G.number_of_edges())   # 输出边的数量：1
nx.draw(G)
plt.savefig("youxiangtu.png", bbox_inches="tight")
plt.show()
