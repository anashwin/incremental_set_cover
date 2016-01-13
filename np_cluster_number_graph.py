import csv
import numpy as np
import matplotlib.pyplot as plt

infile_narrow = 'cluster_lens_file'
infile_wide = 'cluster_lens_wide_file'

np_narrow = []
len_narrow = []

np_wide = []
len_wide = []

nqueries = 50000.0

with open (infile_narrow + '.csv', 'rb') as f: 
    r = csv.reader(f) 
    for row in r: 
        np_narrow.append(float(row[0]))
        len_narrow.append(float(row[1]))

with open (infile_wide + '.csv', 'rb') as f: 
    r = csv.reader(f) 
    for row in r: 
        np_wide.append(float(row[0]))
        len_wide.append(float(row[1]))

fig1 = plt.figure()
ax1 = fig1.add_subplot(111)

ax1.scatter(np_narrow, len_narrow, marker='.', color='k')
ax1.set_xlabel('$np$', fontsize=16)
old_ylim = ax1.get_ylim()
ax1.set_ylim(max([old_ylim[0], 0]), old_ylim[1])

ax1.set_ylabel('Clusters',fontsize=16)
#ax1.set_title('Clusters',fontsize=16)
plt.savefig('narrow_plot.png', bbox_inches='tight')

plt.cla()

ax1.scatter(np_wide, len_wide, marker='.', color='k')
ax1.set_xlabel('$np$', fontsize=16)
ax1.set_ylabel('Clusters',fontsize=16)
old_ymax = ax1.get_ylim()[1]
ax1.set_ylim([0, old_ymax])

#ax1.set_title('Average Queries per Cluster',fontsize=16)
plt.savefig('wide_plot.png', bbox_inches='tight')

#plt.show()
