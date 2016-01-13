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

#number_of_clusterings = 1
#min_q_len = 6
#max_q_len = 15
#NoNodes = 100000
#N = 1000000
#nmachines = 50
#ndata = NoNodes

def full_clustering_procedure(ndata = 100000, N=50000, nmachines = 50, min_q_len = 6, max_q_len = 15, 
                              number_of_clusterings=1, queryfile = None, gcpa_type='better', np=.995): 
    NoNodes = ndata

    for iteration in xrange(number_of_clusterings): 
        print 'ITERATION: ', iteration

        p = np/NoNodes

        output = []
        if queryfile == None: 
    #we genarate random graph on NoNodes vertexes (need to set probability)
            g=Graph.Erdos_Renyi(n=NoNodes, p=p)
            print 'Graph generated'

    #taking random node from the graph
            node=random.randint(0,NoNodes-1)

    #the DFS function, as arguments we have name of the graph, first node
            output = []

    #the loop on the number of queries
    #    for q in range(N):
            while len(output) < N: 
                node=random.randint(0, NoNodes-1)
                line = iterative_dfs(g, node, path=[])
                if len(line) >= min_q_len:
                    output.append(line)

            graphfile = 'n' + str(len(output)/1000) + 'np' + str(np) + '_' + str(iteration)
            with open(graphfile + '.csv','wb') as f:
                w = csv.writer(f)
                for line in output:
                    w.writerow(line)

            print 'Queries generated', len(output)
        else: 
            with open(queryfile + '.csv', 'rb') as f: 
                r = csv.reader(f)
                for row in r:
                    output.append(map(int, row))
            print 'Queries imported'
            graphfile =  queryfile

        infile = graphfile

        test_queries = output

        max_len = min(50000, len(test_queries))
        test_queries = test_queries[:max_len]

    #    clusters, disjoint, cluster_tracker, data_added_count, data_in_nclusters = simple_entropy(test_queries)
    #    clusters, cl_entropies = simple_entropy(test_queries)
        clustering = Clustering(test_queries)
        clusters = clustering.clusters

        outfile = infile + '_output_test'

        print 'Clustered'

        with open(outfile + '.csv', 'wb') as f:
    #    f.write('Output from simpleROCK clustering algorithm \n')
            f.write(str(len(clusters)) + '\n')
            ctr = 1
            for c in clusters: 
                f.write('-----------------------\n')
                f.write('Cluster ' + str(ctr) + '\n')
                f.write('# of Queries: ' + str(len(c)) + '\n')
            #print 1.0*c.min_query_len/len(c.span)
            #        f.write('Span: ' + str(c.span) + '\n')
                f.write(c.aligned_output())
                f.write('-----------------------\n')
                ctr += 1
        print 'Clusters written to file'

        machines = generate(range(ndata), nmachines)
        dataunit_in_machine = generate_hash(machines, ndata)

        if gcpa_type == 'linear': 
            gcpa_data = GCPA(clustering,ndata)
        elif gcpa_type == 'better': 
            gcpa_data = GCPA_better(clustering, ndata)
#        start = time.time()
        gcpa_data.process(machines, dataunit_in_machine)
#        cover_time = time.time() - start
#        average = 1.0*cover_time/len(test_queries)
        return gcpa_data
