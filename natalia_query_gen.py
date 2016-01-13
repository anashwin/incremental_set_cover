from igraph import *
import random
import networkx as nx
import csv

def iterative_dfs(graph, start, path=[],min_len=6, max_len = 15):
    QueryLength=random.randint(min_len,max_len)
    q=[start]
    i=0  
    while i<QueryLength and q:
        v=random.choice(q)
        q.remove(v)
        if v not in path:
          i+=1 #i is an iterator which count how many nodes we add to the path 
          path=path+[v]
          q=graph.neighbors(v)+q 
#          print "smonething"
#    if i!=QueryLength:  #that statement check if query is long enough
#        node=random.randrange(NoNodes-1) #if query is not long enough we choose another node and do recursive function
#        iterative_dfs(graph, node, path=[])
    return path


# #here we can set number of queries
# NoNodes=100000#
N = 1000000
# #we genarate random graph on NoNodes vertexes (need to set probability)
#NoNodes = 10
#g=Graph.Erdos_Renyi(n=NoNodes, p=.999/NoNodes)

# #taking random node from the graph
# node=random.randrange(NoNodes-1)

# #the DFS function, as arguments we have name of the graph, first node
# output = []

# #the loop on the number of queries
# for q in range(N):
#     node=random.randrange(NoNodes-1)
#     output.append(iterative_dfs(g, node, path=[]))

# with open('n1000np.999.csv','wb') as f:
#     w = csv.writer(f)
#     for line in output:
#         if len(line)>5:
#             w.writerow(line)

