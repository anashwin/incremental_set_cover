
with open ('trec_data', 'rb') as f: 
    filestring = f.read()

newstring = filestring.replace('  1', '')

with open('trec_clean', 'wb') as f: 
    f.write(newstring)


