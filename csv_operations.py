import csv

# Reads the csv file located at the file specifiec
# Returns as a list of lists
def read_csv(filename, data_type='int'):
    out_list = []
    with open(filename, 'rb') as f:
        r = csv.reader(f)
        for row in r: 
            if data_type == 'int':
                row = map(int, row)

            out_list.append(row)
    return out_list

# Writes data to the given filename, using the 
# (optional) specified delimiter
# The data needs to be either in list of list form
# or dictionary 
def write_csv(filename, data, delim=','):
    with open(filename, 'wb') as f:
        w = csv.writer(f, delimiter=delim)
        if type(data) == type([]):
            for row in data: 
                w.writerow(row)
        elif type(data) == type(dict()):
            for key in data: 
                to_write = [key]
                info = data[key]
                if type(info) == type([]):
                    to_write.extend(info)
                else: 
                    to_write.append(info)
                w.writerow(to_write)
