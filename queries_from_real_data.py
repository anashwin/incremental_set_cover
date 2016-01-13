import pickle 
import random
import csv
import time


master_dict = pickle.load(open('real_data_dict.p', 'rb'))

for key in master_dict.keys(): 
    master_dict[key] = map(int, master_dict[key])


# Now we generate the queries

n_queries = 70000
min_len = 20
max_len = 40
n_baskets = 100 

frac_used = .15

query_list = []


if frac_used < 1: 
    pruned_dict = dict()
    for key in master_dict: 
        to_sample = max(int(frac_used*len(master_dict[key])),max_len)
        to_sample = min(to_sample, len(master_dict[key]))
        pruned_dict[key] = random.sample(master_dict[key], to_sample)

else: 
    pruned_dict = master_dict


while len(query_list) < n_queries: 
    basket = random.randint(0, n_baskets-1)
    basket_name = 'all-' + str(basket)
    length = min(random.randint(min_len, max_len), len(pruned_dict[basket_name]))
    query = random.sample(pruned_dict[basket_name], length)

    query_list.append(query)


query_file = 'real_queries_' + str(frac_used) + '_' + str(time.time())
# Time guarantees uniqueness

with open(query_file + '.csv', 'wb') as f: 
    w = csv.writer(f)
    for query in query_list: 
        w.writerow(query)
