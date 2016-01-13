import csv

# Just give the filename of the clusters you want returned, and the output will be of the form:
# [[cluster 1: [query11], ... [query i]], [cluster 2: [] ... []], ... ]
# i.e. clusters[0][0][0] returns the 1st element of the first query of the first cluster
def extract_clusters(filename):
    clusters = []
    with open(filename, 'rb') as f: 
        start = True
        r = csv.reader(f)
        for row in r: 
            if row[0] == '-----------------------':
                if start:
                    to_append = []
                    start = False
                else: 
                    clusters.append(to_append)
                    start = True
            elif row[0] == ' ':
                temp = row[1:]
                query = []
                for i in xrange(len(temp)): 
                    if temp[i] != ' ' and temp[i] != '':
                        query.append(int(temp[i]))
                to_append.append(query)
    return clusters
