class Cluster: 
    
    def __init__(self, queries=[]): 
        self.queries = queries
        self.span = set([])
        if len(queries) == 0: 
            min_len = 0
        else: 
            min_len = len(queries[0])
        for q in queries: 
            self.span = self.span | set(q)
            if len(q) < min_len: 
                min_len = len(q)
        self.min_query_len = min_len

    def __iter__(self):
        return iter(self.queries)

    def __str__(self): 
        return str(self.queries)

    def __or__(self, other): 
        out = Cluster(self.queries + other.queries)
        return out
    
    def __ior__(self,other): 
        out = Cluster(self.queries + other.queries)
        return out
    
    def __getitem__(self,k): 
        return self.queries[k]
    
    def __len__(self): 
        return len(self.queries)

    def check_merge(self, other, factor): 
        return len((self | other).span) <= factor*min(self.min_query_len, other.min_query_len)
    
    def similarity(self, other): 
        return 1.0*len(self.span & other.span)/len(self.span | other.span)

    def distance(self, other): 
        return 1 - self.similarity(other)
    
    def aligned_output(self): 
        out_str = ''
        key = list(self.span)
        key.sort()
#        print key
        out_str += 'Span,' + str(key)[1:-1] + '\n'
        for query in self.queries:
            query = list(query)
            query.sort()
#            print query
            q_str = ' ,'
            q_ind = 0
            key_ind = 0
            while q_ind < len(query): 
                q = query[q_ind]
                k = key[key_ind]
                if q == k: 
                    q_str += str(q)
                    q_ind += 1
                q_str += ', '
                key_ind +=1 
            out_str += (q_str + '\n')
        return out_str
#        self.queries.extend(other.queries)
#        self.min_query_len = min(self.min_query_len,other.min_query_len)
#        return self


#temp = Cluster([[1,2,3],[1,2],[1,2,3,4]])
#for c in temp: 
#    c.append(10)
#    print c
