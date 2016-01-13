import csv
from csv_operations import *
from natalia_query_gen import *
#from simple_entropy_fast import *
from linear_greedy import *
from generate_machines import *
from clustering import *
#from gcpa import *
from gcpa_fast import *
from baseline import *
from gcpa_better import *

import numpy as np
import random
import matplotlib.pyplot as plt

iterations = 1000
nmachines = 50
ndata = 100000
nqueries = 50000
min_q_len = 6
max_q_len = 15
NoNodes = ndata


np_vals = []
cluster_lens = []

for iteration in xrange(iterations): 
    print 'Iteration:', iteration
    np = 1.0*random.randint(4000, 16000)/10000

    np_vals.append(np)
    p = np/NoNodes

    g=Graph.Erdos_Renyi(n=NoNodes, p=p)
    print 'Graph generated'

#taking random node from the graph
    node=random.randint(0,NoNodes-1)

#the DFS function, as arguments we have name of the graph, first node
    output = []

#the loop on the number of queries
#    for q in range(N):
    while len(output) < nqueries: 
        node=random.randint(0, NoNodes-1)
        line = iterative_dfs(g, node, path=[])
        if len(line) >= min_q_len:
            output.append(line)

    graphfile = 'n' + str(len(output)/1000) + 'np' + str(np) + '_' + str(iteration)
#    with open(graphfile + '.csv','wb') as f:
#        w = csv.writer(f)
#        for line in output:
#            w.writerow(line)

    print 'Queries generated', len(output)

#    infile = graphfile

    test_queries = output

    max_len = min(50000, len(test_queries))
    test_queries = test_queries[:max_len]

    #    clusters, disjoint, cluster_tracker, data_added_count, data_in_nclusters = simple_entropy(test_queries)
    #    clusters, cl_entropies = simple_entropy(test_queries)
    clustering = Clustering(test_queries, notif='silent')
    clusters = clustering.clusters
    cluster_lens.append(len(clusters))

    with open('cluster_lens_wide_file.csv', 'a') as f: 
        w = csv.writer(f)
        w.writerow([np_vals[-1], cluster_lens[-1]])

#print np_vals

# with open('cluster_lens_file.csv', 'wb') as f: 
#     w = csv.writer(f)
#     for idx, np in enumerate(np_vals): 
#         cluster_len = cluster_lens[idx]
#         w.writerow([np, cluster_len])
