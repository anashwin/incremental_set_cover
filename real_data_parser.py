import pickle
import csv

infile = 'trec6-kmeans-xu99'

flag = False

master_dict = dict()
query_to_index = []

index = 0
with open(infile, 'rb') as f: 
    for line in f: 

        if '<COMMENT>' in line: 
            continue
        
        if index % 1000 == 0: 
            print index

        sp = line.find(' ')
        data_tag = line[:sp]
        basket = line[sp+1:-1]
        

        query_to_index.append(data_tag)
        if basket in master_dict: 
            master_dict[basket].append(index)
        else: 
            master_dict[basket] = [index]
            
        index += 1

masterlist_file = 'real_data_index_file'
dict_file = 'real_data_dict'
print 'saving files ...' 

with open(masterlist_file + '.csv', 'wb') as f: 
    w = csv.writer(f) 
    for index, item in enumerate(query_to_index): 
        w.writerow([index, item])

pickle.dump(master_dict, open(dict_file + '.p', 'wb'))

 
