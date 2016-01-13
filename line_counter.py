counter = 0
with open('trec_clean.csv', 'rb') as f: 
    for line in f: 
        counter += 1

print counter
