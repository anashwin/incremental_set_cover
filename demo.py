from gcpa_fast import *
from gcpa_better import *
from clustering import *
from full_clustering_procedure import *
from full_clustering_procedure_comparisons import *
from full_realtime import *
from full_realtime_comparisons import *

# Set parameters here
ndata = 100000
nqueries = 50000
nmachines = 50
min_q_len = 6
max_q_len = 15
rep = 3
theta_1 = .5
theta_2 = .5
np = .995
# Here we run the full clustering procedure in non-real-time with default parameters

#gcpa_1 = full_clustering_procedure()

# gcpa_1.covers gives the covers, and gcpa_1.clusters gives the queries that each cover goes with (both 
# are indexed with the same number)

# we can now compare the results of our algorithm v. the baseline and greedy algorithms.
# (we use a different np here so the filenames don't overlap ... a bug that should be fixed
#full_clustering_procedure_comparisons(ndata=1000000, queryfile = 'trec_clean', delim=' ')
#full_clustering_procedure_comparisons(np=2.0)

# Read the output files to see and analyze comparisons

# Now we do real-time 
#gcpa_3, rt_queries, rt_covers = full_realtime(np=.996)

# And with comparisons
full_realtime_comparisons(queryfile = 'trec_clean', delim=' ')

# We can also use query input files, just add the query filename as an argument to any of the algorithms
