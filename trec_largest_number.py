import csv


max_elem = 0 
min_elem = 100000000
with open('trec_clean', 'rb') as f: 
    r = csv.reader(f, delimiter=' ')
    for row in r: 
        for item in row: 
            if int(item) > max_elem: 
                max_elem = int(item)
            if int(item) < min_elem: 
                min_elem = int(item)

print min_elem, max_elem
