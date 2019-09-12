#!-*- coding:utf-8 -*-
# __author__ : Sora
# ___time___ : 2019/06/24/15:05

import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt
import warnings
import formula

init_nodes = int(input("Please type in the initial number of nodes (m_0): "))
final_nodes = int(input("\nPlease type in the final number of nodes: "))
m_parameter = int(input("\nPlease type in the value of m parameter (m<=m_0): "))


print("\n")
print("Creating initial graph...")

G = nx.complete_graph(init_nodes)
for i in range(init_nodes):
    fitness = 0
    while fitness == 0:
        fitness = rd.random()
        G.node[i]['f'] = fitness
        print("node:",i)
        print("fitness:{}",format(fitness))
nx.draw(G, node_size=30)
plt.show()

print("Graph created. Number of nodes: {}".format(len(G.nodes())))
print("Adding nodes...")

def rand_prob_node():
    nodes_probs = []
    all_fitness = 0
    for node in G.nodes():
        all_fitness += G.node[node]['f'] *G.degree(node)
    for node in G.nodes():
        node_degr = G.degree(node)
        node_proba = G.node[node]['f'] * node_degr / all_fitness
        nodes_probs.append(node_proba)
    random_proba_node = np.random.choice(G.nodes(),p=nodes_probs)
    return random_proba_node

def add_edge():
        if len(G.edges()) == 0:
            random_proba_node = 0
        else:
            random_proba_node = rand_prob_node()
        new_edge = (random_proba_node, new_node)
        print("Edge: {} {}".format(new_node + 1, random_proba_node + 1))
        if new_edge in G.edges():
            print("edge is exist！")
            add_edge()
        else:
            print("add edge sucess!")
            G.add_edge(new_node, random_proba_node)
            # nx.draw(G, node_size=30)
            # plt.show()
            print("Edge added: {} {}".format(new_node + 1, random_proba_node + 1))

count = 0
new_node = init_nodes

for f in range(final_nodes - init_nodes):
    print("----------> Step {} <----------".format(count))
    fitness = 0
    while fitness == 0:
        fitness = rd.random()
        G.add_node(init_nodes + count, f=fitness)
    print("Node added: {}".format(init_nodes + count + 1))
    count += 1
    for e in range(0, m_parameter):
        add_edge()
    new_node += 1


print("\nFinal number of nodes ({}) reached".format(len(G.nodes())))
nx.draw(G, pos=nx.random_layout(G), node_size=3, width=0.05)
print("density:", formula.density(G))
print("clustering coefficient:", formula.clustering_coefficient(G))
a = formula.average_path_length(G)
print('nx.shortest_path_length(G):', a)
plt.savefig("fitness.png", dpi=1000)
plt.show()


f = open('fitness_degree.txt', 'w+')
for node in G.nodes():
    node_degr = G.degree(node)
    f.write("node {} degree is {}".format(node + 1, node_degr))
    f.write('\n')
f.close()