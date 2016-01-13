from cluster import *
#from simple_entropy import *
import time
from math import log

class Clustering: 

    def __init__(self, queries=[], theta_1=.3, theta_2=.3, notif='silent'): 
        self.theta_1 = theta_1
        self.theta_2 = theta_2
        self.notif=notif
        queries = map(set, queries)
        N = len(queries)
        print N
        clusters = [Cluster([queries[0]])]
        cl_entropies = []
        cluster_count = 1
        cl_entropies.append(self.add_to_cluster(queries[0],[0,0,dict()],0.0))
        data_hash = dict()
        prev_exp_entropy = 0
        self.queries_processed = 1
        t = time.time()
        for idx, q in enumerate(queries[1:]):
            self.queries_processed += 1
            i = idx + 1
            if notif=='loud' and (i % 1000) == 0: 
                t2 = time.time()
                print i, t2 - t
                t = t2
            data_freq = 0
            potential_clusters = set()
            for dp in q:
                if dp in data_hash: 
                    data_freq += 1
                    potential_clusters |= data_hash[dp]
                    
            min_total_exp = float('inf')
            min_exp = float('inf')

            min_j = -1
            if data_freq >= theta_1*len(q): 
                for j in potential_clusters:
                    c_data = cl_entropies[j]
                    exp = self.expected_entropy(q, c_data)
                    total_exp = 1.0/(i+1)*(i*prev_exp_entropy - c_data[0]*c_data[1] + exp)
                    if total_exp < min_total_exp: 
                        min_total_exp = total_exp
                        min_j = j
                        min_exp = exp
#            print idx, min_total_exp
        # If we add to an existing cluster
            if min_total_exp < float('inf'): 
                clusters[min_j] |= Cluster([q])
                cl_entropies[min_j] = self.add_to_cluster(q, cl_entropies[min_j], min_exp/len(clusters[min_j]))
                prev_exp_entropy = min_total_exp            
                for dp in q: 
                    if cl_entropies[min_j][2][dp] > theta_1*cl_entropies[min_j][0]:
                        if dp in data_hash: 
                            data_hash[dp].add(min_j)
                        else: 
                            data_hash[dp] = set([min_j])
            else: 
                clusters.append(Cluster([q]))
                cl_entropies.append(self.add_to_cluster(q,[0,0,dict()], 0.0))
                cluster_count += 1
                if notif == 'loud':
                    print 'Clusters: ', cluster_count, 'out of', i+1
                for dp in q: 
                    if dp in data_hash: 
                        data_hash[dp].add(cluster_count-1)
                    else: 
                        data_hash[dp] = set([cluster_count-1])

        self.clusters = clusters
        self.cl_entropies = cl_entropies
        self.cluster_count = cluster_count
        self.data_hash = data_hash
        self.prev_exp_entropy = prev_exp_entropy
        
    

    # Much faster method of real-time insertion. We look at just one potential cluster and put it in. 
    def insert_rt_fast(self, query): 
        dp = query.pop()
        query.add(dp)
        if dp in self.data_hash: 
            clusterind = self.data_hash[dp].pop()
            self.data_hash[dp].add(clusterind)
            return clusterind
        else:
            return -1
    
    def insert_rt_noupdate(self, query): 
        potential_clusters = set()

        data_freq = 0
        for dp in query: 
            if dp in self.data_hash: 
                data_freq += 1
                potential_clusters |= self.data_hash[dp]

        min_total_exp = float('inf')
        min_exp = float('inf')

        if data_freq >= self.theta_1 * len(query): 
            for j in potential_clusters: 
                c_data = self.cl_entropies[j]
                exp = self.expected_entropy(query, c_data)
                qp = self.queries_processed
                total_exp = 1.0/(qp+1)*(qp*self.prev_exp_entropy - c_data[0]*c_data[1] + exp)
                if total_exp < min_total_exp: 
                    min_total_exp = total_exp
                    min_j = j
                    min_exp = exp
        if min_total_exp < float('inf'): 
            return min_j 
        else: 
            return -1 

    def insert_rt_update(query): 
        potential_clusters = set()
        data_freq = 0
        for dp in q: 
            if dp in self.data_hash: 
                data_freq += 1
                potential_clusters |= data_hash[dp]

        min_total_exp = float('inf')
        min_exp = float('inf')

        if data_freq >= theta_1 * len(query): 
            for j in potential_clusters: 
                c_data = self.cl_entropies[j]
                exp = self.expected_entropy(query, c_data)
                qp = self.queries_processed
                total_exp = 1.0/(qp+1)*(qp*self.prev_exp_entropy - c_data[0]*cdata[1] + exp)
                if total_exp < min_total_exp: 
                    min_total_exp = total_exp
                    min_j = j
                    min_exp = exp
                    
        if min_total_exp < float('inf'): 
            self.clusters[min_j] |= Cluster([query])
            self.cl_entropies[min_j] = self.add_to_cluster(query, self.cl_entropies[min_j], 
                                                           min_exp/len(clusters[min_j]))
            self.prev_exp_entropy = min_total_exp
        else: 
            self.clusters.append(Cluster[query])
            self.cl_entropies.append(self.add_to_cluster(query, [0,0,dict()], 0.0))
            self.cluster_count += 1
            for dp in query: 
                if dp in self.data_hash: 
                    self.data_hash[dp].add(self.cluster_count -1)
                else: 
                    self.data_hash[dp] = set([self.cluster_count-1])
        

    def expected_entropy(self, query, cl_entropy, r=.5):
        n = cl_entropy[0]
        prev_entropy = cl_entropy[1]
        freq_dict = cl_entropy[2]
        new_entropy = 0
        valid_entries = 0
        for dp in query: 
            if dp in freq_dict:
                p = 1.0*(freq_dict[dp] + 1)/(n+1)
                if p >= .5: 
                    valid_entries += 1
            else: 
                p = 1.0/(n+1)
            if 0.0 < p < 1.0:
                new_entropy -= (p*log(p,2) + (1-p)*log(1-p,2))
        for dp in freq_dict: 
            if dp not in query: 
                p = 1.0*freq_dict[dp]/(n+1)
                new_entropy -= (p*log(p,2) + (1-p)*log(1-p,2))
        if valid_entries >= r*len(query):
            return new_entropy*(n+1)
        else: 
            return float('inf')

    def add_to_cluster(self, query, cl_entropy, new_entropy): 
        cl_entropy[0] += 1
        cl_entropy[1] = new_entropy
        freq_dict = cl_entropy[2]
        for dp in query: 
            if dp in freq_dict:
                freq_dict[dp] += 1
            else: 
                freq_dict[dp] = 1
        return cl_entropy
