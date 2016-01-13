from clustering import *
from linear_greedy import *

class GCPA:
    def __init__(self, clustering, ndataunits, outfile=''): 
        nprocessed=0
        self.queues = []
        self.datapart_in_query_lists = []
        self.uppersets_list = []
        self.nqueries_in_clusters = []

#        with open(outfile, 'wb') as myfile:
#        wr = csv.writer(myfile)
        for cluster in clustering.clusters:
            nqueriesincluster=len(cluster)
            self.nqueries_in_clusters.append(nqueriesincluster)

            dataunit_in_query={}

            for queryindex in xrange(nqueriesincluster):
                for dataunit in cluster[queryindex]:
                    if dataunit in dataunit_in_query:
                        dataunit_in_query[dataunit].add(queryindex)
                    else:
                        dataunit_in_query[dataunit]=set([queryindex])

            depths_of_data_parts={}
            for dataunit in dataunit_in_query:
                if len(dataunit_in_query[dataunit]) in depths_of_data_parts:
                    didweaddit=0
                    for data_part in depths_of_data_parts[len(dataunit_in_query[dataunit])]:
                        if dataunit_in_query[dataunit]==dataunit_in_query[list(data_part)[0]]: #BETTER????
                            data_part.add(dataunit)
                            didweaddit=1
                            break
                    if didweaddit==0:
                        depths_of_data_parts[len(dataunit_in_query[dataunit])].append(set([dataunit]))
                else:
                    depths_of_data_parts[len(dataunit_in_query[dataunit])]=[set([dataunit])]

            queue=[]
            datapart_in_query=[]
            depthqueue=depths_of_data_parts.keys()
            depthqueue.sort(reverse=True)
            for depth in depthqueue:
                for datapart in depths_of_data_parts[depth]:

                    queue.append(datapart)
                    datapart_in_query.append(dataunit_in_query[list(datapart)[0]])

            uppersets=[]
            for datapartindex in xrange(len(queue)):
                upperset=set()
                for otherdatapartindex in xrange(len(queue)):
                    if datapart_in_query[otherdatapartindex]<=datapart_in_query[datapartindex]:
                        upperset|=queue[otherdatapartindex]
                uppersets.append(upperset)

            self.queues.append(queue)
            self.datapart_in_query_lists.append(datapart_in_query)
            self.uppersets_list.append(uppersets)
            self.partindex_by_cluster = []
            self.partcover_by_cluster = []
            self.covers = [None for i in xrange(len(self.queues))]
            nprocessed+=1
            print nprocessed

    def process(self, machines, dataunit_in_machine): 
        nprocessed=0
        queues = self.queues
        datapart_in_query_lists = self.datapart_in_query_lists
        uppersets_list = self.uppersets_list
        nqueriesinclusters = self.nqueries_in_clusters
#        covers = self.covers
#        covers=[None for i in xrange(len(queues))]
        for index in range(len(queues)):
            self.covers[index]=[set() for i in xrange(nqueriesinclusters[index])]

        start=time.time()

        for queueindex,queue in enumerate(queues):
        #    queue=queues[queueindex]

            dataunit_in_part = dict()
            part_cover = dict()

            covered=set()
            part_index = -1
            for datapartindex in xrange(len(queue)):

                part_index += 1
                datapart=queue[datapartindex]-covered

                if datapart!=set():

                    #now we make machinesintersected
                    machinesintersected={}

                    for dataunit in datapart:
                        dataunit_in_part[dataunit] = part_index
                        for machine in dataunit_in_machine[dataunit]:
                            if machine in machinesintersected:
                                machinesintersected[machine].add(dataunit)
                            else:
                                machinesintersected[machine]=set([dataunit])
                    
                    #then use the linear greedy
                    cover, dt = linear_greedy(datapart, machines, dataunit_in_machine)
                    part_cover[part_index] = cover
                    #now we add the cover to appropriate covers for queries
                    for queryindex in datapart_in_query_lists[queueindex][datapartindex]:
        #                smartload+=len(cover-covers[queueindex][queryindex])
                        self.covers[queueindex][queryindex]|=cover

                    #and the last thing, we need to remove appropriate elements from appropriate data parts
                    coveredinupperset=datapart.copy()
                    for dataunit in uppersets_list[queueindex][datapartindex]-datapart:
                        if not (dataunit_in_machine[dataunit]&cover)==set():
                            coveredinupperset.add(dataunit)

                    covered|=coveredinupperset
            self.partindex_by_cluster.append(dataunit_in_part)
            self.partcover_by_cluster.append(part_cover)
        #    nprocessed+=1
        #    print nprocessed

        end=time.time()


