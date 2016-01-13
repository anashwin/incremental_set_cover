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

def full_clustering_procedure_comparisons(ndata = 100000, N=50000, nmachines = 50, min_q_len = 6, max_q_len = 15, number_of_clusterings=1, queryfile = None, np = .995, delim=','): 
    NoNodes = ndata

    for iteration in xrange(number_of_clusterings): 
        print 'ITERATION: ', iteration

#        np = .993
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
                r = csv.reader(f,delimiter=delim)
                for row in r:
                    output.append(map(int, row))
            print 'Queries imported'
            graphfile =  queryfile

        infile = graphfile

        test_queries = output

        max_len = len(test_queries)
        N = len(test_queries)
        #min(50000, len(test_queries))
        test_queries = test_queries[:max_len]

    #    clusters, disjoint, cluster_tracker, data_added_count, data_in_nclusters = simple_entropy(test_queries)
    #    clusters, cl_entropies = simple_entropy(test_queries)
        clustering = Clustering(test_queries, notif='loud')
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
        gcpa_data = GCPA(clustering,ndata)
        start = time.time()
        gcpa_data.process(machines, dataunit_in_machine)
        cover_time = time.time() - start
        average = 1.0*cover_time/len(test_queries)

        gcpa_better = GCPA_better(clustering, ndata)

        betterstart = time.time()
        gcpa_better.process(machines, dataunit_in_machine)
        better_dt = time.time() - betterstart
        better_average = 1.0*better_dt/len(test_queries)

        lg_start = time.time()
        for query in test_queries: 
            cover, dt = linear_greedy(query, machines, dataunit_in_machine)

        lg_dt = time.time() - lg_start
        lg_ave = 1.0*lg_dt/len(test_queries)

        baseline_start = time.time()
        for query in test_queries: 
            cover, dt = baseline(query, machines, dataunit_in_machine)
        baseline_dt = time.time() - baseline_start
        baseline_ave = 1.0*baseline_dt/len(test_queries)

        b_baseline_start = time.time()
        for query in test_queries: 
            cover, dt = better_baseline(query, machines, dataunit_in_machine)
        b_baseline_dt = time.time() - baseline_start
        b_baseline_ave = 1.0*b_baseline_dt/len(test_queries)

#        print average, better_average, lg_ave, baseline_ave, b_baseline_ave
        print baseline_ave, b_baseline_ave, lg_ave, average, better_average

        covers = gcpa_data.covers
        better_covers = gcpa_better.covers

        to_write = []
        total = 0
        for clusterind, coverset in enumerate(covers): 
            for query_ind, cover in enumerate(coverset): 
                if total % 1000 == 0: 
                    print total 
                total +=1 
                query = clustering.clusters[clusterind][query_ind]

                gcpa_fast_lin = cover
                gcpa_fast_better = better_covers[clusterind][query_ind]

                lg_cover, lg_dt = linear_greedy(query, machines, dataunit_in_machine)
                baseline_cover, baseline_dt = baseline(query, machines, dataunit_in_machine)
                b_baseline_cover, b_baseline_dt = better_baseline(query, machines, dataunit_in_machine)
    #            to_write.append(map(len, [gcpa_fast_lin, gcpa_fast_better, lg_cover, baseline_cover, b_baseline_cover]))
                to_write.append(map(len, [baseline_cover, b_baseline_cover, lg_cover, gcpa_fast_lin, gcpa_fast_better]))

        with open(infile + 'big_comparison.csv', 'wb') as f: 
            w = csv.writer(f)
            w.writerow(['Baseline', 'Better Baseline', 'N-Greedy', 'GCPA_G', 'GCPA_DL'])
            w.writerow([baseline_ave, b_baseline_ave, lg_ave, average, better_average])
            for row in to_write: 
                w.writerow(row)

