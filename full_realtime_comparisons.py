from natalia_query_gen import *
from clustering import Clustering
from linear_greedy import *
from generate_machines import *
# from gcpa import *
from gcpa_fast import *
from gcpa_better import *
from baseline import *
import time
#from igraph import *
#import networkx as nx
#import random

def precompute_clustering(pre_computed, machines, dataunit_in_machine):

    clustering = Clustering(pre_computed)
    # Indexed with the clusters. This array will store the necessary G-part information for each of the clusters
    parts_data = []
    ctr = 0

    for cluster in clustering.clusters: 
        print '%d out of %d'  % (ctr, len(clustering.clusters))
        ctr += 1
        part_covers, dataunit_in_parts = gcpa_precompute_rt(cluster, machines, dataunit_in_machine)
        parts_data.append((part_covers, dataunit_in_parts))

    return clustering, parts_data

def cluster_timings(query, clustering): 
    start_full = time.time()
    clusterind = clustering.insert_rt_noupdate(query)
    dt_full = time.time() - start_full

    start_fast = time.time()
    clusterind = clustering.insert_rt_fast(query)
    dt_fast = time.time() - start_fast

    return dt_full, dt_fast

def rt_query_process(query, clustering, gcpa_data, machines, dataunit_in_machine, ctype='fast'): 
    query = set(query)
    start = time.time()
    if ctype == 'fast': 
        cluster_index = clustering.insert_rt_fast(query)
    elif ctype=='full':
        cluster_index = clustering.insert_rt_noupdate(query)
    
    if cluster_index == -1: 
#        print 'JUST DID LG'
        return linear_greedy(query, machines, dataunit_in_machine)[0], time.time() - start

#    relevant_parts = parts_data[cluster_index]
    parts_cover = gcpa_data.partcover_by_cluster[cluster_index]
    dataunit_in_parts = gcpa_data.partindex_by_cluster[cluster_index]

    unprocessed = set(query)
    last_greedy = set()
    cover = set()
    while len(unprocessed) >0: 
        x = unprocessed.pop()
        # Depending on how you write rt-gcpa, one of these if statements can be removed
        if x in dataunit_in_parts: 
            x_part = dataunit_in_parts[x]
#            print x_part
#            print hello
            cover |= parts_cover[x_part]
            for machine in parts_cover[x_part]: 
                unprocessed = unprocessed - machines[machine]
                last_greedy = last_greedy - machines[machine]
        else: 
            last_greedy.add(x)
#    if len(last_greedy) == len(query): 
#        print 'BAD!'
    cover |= linear_greedy(last_greedy, machines, dataunit_in_machine)[0]
    dt = time.time() - start

#    # COVERED CHECK
    query_copy = set(query)
    for c in cover: 
        query_copy = query_copy - machines[c]
    if len(query_copy) > 0: 
        print 'NOT COVERED'

    return cover, dt

def full_realtime_comparisons(precompute_fraction=.2, nqueries=50000, ndataunits=100000, nmachines=50, r=3, np=.995,
                  min_q_len=6, max_q_len=15, ctype='fast', gcpatype='better', queryfile=None,delim=','): 
    queries = []

    if queryfile == None: 
        g = Graph.Erdos_Renyi(n=ndataunits, p = np/ndataunits)
        q = 0
        while q < nqueries: 
            node=random.randint(0, ndataunits-1)
            line = iterative_dfs(g, node, path=[])
            if len(line) >= min_q_len:
                queries.append(line)
                q += 1

        graphfile = 'n' + str(len(queries)/1000) + 'np' + str(np) +ctype + gcpatype + 'test'
        with open(graphfile + '.csv','wb') as f:
            w = csv.writer(f)
            for line in queries:
                w.writerow(line)

        print 'Queries generated', len(queries)
    else: 
        with open(queryfile + '.csv', 'rb') as f: 
            r = csv.reader(f, delimiter=delim)
            for row in r: 
                queries.append(map(int, row))
        graphfile = queryfile

    infile = graphfile
#    max_to_process = min(nqueries, len(queries))
#    queries = queries[:max_to_process]

    pre_computed = queries[:int(precompute_fraction*len(queries))]
    machines = generate(range(ndataunits), nmachines)
    dataunit_in_machine = generate_hash(machines, ndataunits)

    clustering = Clustering(pre_computed, notif='loud')

    rt_queries = queries[len(pre_computed):]
    
    if gcpatype == 'linear': 
        gcpa_data = GCPA(clustering, ndataunits)
    elif gcpatype == 'better': 
        gcpa_data = GCPA_better(clustering, ndataunits)
    elif gcpatype == 'both': 
        gcpa_linear = GCPA(clustering, ndataunits)
        gcpa_better = GCPA_better(clustering, ndataunits)
    
    if gcpatype != 'both':
        gcpa_data.process(machines, dataunit_in_machine)
    else: 
        gcpa_linear.process(machines, dataunit_in_machine)
        gcpa_better.process(machines, dataunit_in_machine)

    gcpa_rt_coverlens = []
    gcpa_times = []

    
    lg_coverlens = []
    baseline_coverlens = []
    baseline_times = []

    b_baseline_coverlens = []
    b_baseline_times = []
    smaller = 0

    lg_times = []
    for idx, query in enumerate(rt_queries):
        oldlen = len(query)
        if (idx % 1000) == 0: 
            print 'Query: ', idx

        if ctype != 'both': 
            cover, gcpa_dt = rt_query_process(query, clustering, gcpa_data, machines, dataunit_in_machine, ctype)
            gcpa_rt_coverlens.append(len(cover))
            gcpa_times.append(gcpa_dt)
        else: 
            cover_fast, gcpa_fast_dt = rt_query_process(query, clustering, gcpa_linear, machines, dataunit_in_machine, 'fast')
            cover_full, gcpa_full_dt = rt_query_process(query, clustering, gcpa_linear, machines, dataunit_in_machine, 'full')
            cover_better_fast, gcpa_better_fast_dt = rt_query_process(query, clustering, gcpa_better, machines, dataunit_in_machine, 'fast')
            cover_better_full, gcpa_better_full_dt = rt_query_process(query, clustering, gcpa_better, machines, dataunit_in_machine, 'full')
            gcpa_rt_coverlens.append(map(len,[cover_fast, cover_full, cover_better_fast, cover_better_full]))
            gcpa_times.append([gcpa_fast_dt, gcpa_full_dt, gcpa_better_fast_dt, gcpa_better_full_dt])
        
        lg_cover, lg_dt = linear_greedy(query, machines, dataunit_in_machine)
        
        lg_times.append(lg_dt)

        baseline_cover, baseline_time = baseline(query, machines, dataunit_in_machine)

        lg_coverlens.append(len(lg_cover))
        baseline_coverlens.append(len(baseline_cover))
        baseline_times.append(baseline_time)
        
        b_baseline_cover, b_baseline_time = better_baseline(query, machines, dataunit_in_machine)
        b_baseline_coverlens.append(len(b_baseline_cover))
        b_baseline_times.append(b_baseline_time)

    with open(infile +'_cover_len_comparison.csv', 'wb') as f:
        w = csv.writer(f)
        if ctype != 'both': 
            w.writerow(['GCPA', 'Greedy', 'Baseline', 'Better Baseline'])
            for idx, cl in enumerate(gcpa_rt_coverlens):
                w.writerow([cl, lg_coverlens[idx], baseline_coverlens[idx], b_baseline_coverlens[idx]])
        else: 
            w.writerow(['GCPA_G_A', 'GCPA_G_U', 'GCPA_DL_A', 'GCPA_DL_U', 'Greedy', 'Baseline', 'Better Baseline'])
            for idx, cl in enumerate(gcpa_rt_coverlens):
                cl.extend([lg_coverlens[idx], baseline_coverlens[idx], b_baseline_coverlens[idx]])
                w.writerow(cl)

    with open(infile +'_time_comparison.csv', 'wb') as f:
        w = csv.writer(f)
        if ctype != 'both':
            w.writerow(['GCPA', 'Greedy', 'Baseline', 'Better Baseline']) 
            for idx, gcpa_dt in enumerate(gcpa_times): 
                w.writerow([gcpa_dt, lg_times[idx], baseline_times[idx], b_baseline_times[idx]])
        else: 
            w.writerow(['GCPA_G_A', 'GCPA_G_U', 'GCPA_DL_A', 'GCPA_DL_U', 'Greedy', 'Baseline', 'Better Baseline'])
            for idx, gcpa_dt in enumerate(gcpa_times): 
                gcpa_dt.extend([lg_times[idx], baseline_times[idx], b_baseline_times[idx]])
                w.writerow(gcpa_dt)
        
# full_realtime(ctype='both', gcpatype='both')
