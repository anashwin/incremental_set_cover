import csv

final_number = 50000

outstring = ''
counter = 0
with open('trec_clean.csv', 'rb') as f: 
    for line in f: 
        if counter >= final_number: 
            break
        outstring += line

with open('trec_small_' + str(final_number/1000) + '.csv', 'wb') as f: 
    f.write(outstring)
        
