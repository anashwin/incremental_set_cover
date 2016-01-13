import random
import csv

# N is the number of queries
# max_U is the number the data goes up to
# min_len and max_len are the min and max length of the queries
def generate_random_queries(N, max_U, min_len, max_len): 
    queries = []
    for i in range(N): 
        length = random.randint(min_len, max_len)
        this_query = set([])
        while len(this_query) < length:
            flag = True
            while flag or (x in this_query):
                flag = False
                x = random.randint(0, max_U-1)
            this_query.add(x)
        queries.append(this_query)
    return queries

#queries = generate_random_queries(100, 20, 5, 10)
#with open('entropy_training_data2.csv', 'wb') as f: 
#    w = csv.writer(f)
#    for q in queries: 
#        w.writerow(q)
