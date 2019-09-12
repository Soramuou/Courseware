#!-*- coding:utf-8 -*-
# __author__ : Sora
# ___time___ : 2019/06/24/22:36

import networkx as nx

def density(G):
    nodes = len(G.nodes())
    edges = len(G.edges())
    density = 2 * edges/(nodes * (nodes-1))
    return density

def average_path_length(G):
    return nx.average_shortest_path_length(G)

def clustering_coefficient(G):
    return nx.average_clustering(G)

