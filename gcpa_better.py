from clustering import *
from linear_greedy import *

class GCPA_better: 
    def __init__(self, clustering, ndataunits, outfile = ''): 
#with open('PrecomputedBG.csv', 'wb') as myfile:
#        wr = csv.writer(myfile)
        print 'PRECOMPUTING'
        nprocessed = 0
        self.queues = []
        self.datapart_in_query_lists = []
        self.uppersets_list = []
        self.nqueriesinclusters = []
        self.setsforbg_lists = []

        for cluster in clustering.clusters:
            if nprocessed % 100 == 0: 
                print 'Cluster: ', nprocessed
            nprocessed += 1
            nqueriesincluster=len(cluster)
            self.nqueriesinclusters.append(nqueriesincluster)

            dataunit_in_query={}

            for queryindex in xrange(nqueriesincluster):
                for dataunit in cluster[queryindex]:
                    if dataunit in dataunit_in_query:
                        dataunit_in_query[dataunit].add(queryindex)
                    else:
                        dataunit_in_query[dataunit]=set([queryindex])

            depths_of_data_parts={}

            for dataunit in xrange(ndataunits):
                if dataunit in dataunit_in_query:
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
            setsforbg=[]
            for datapartindex in xrange(len(queue)):
                upperset=queue[datapartindex].copy()
                setforbg=set()
                for otherdatapartindex in xrange(len(queue)):
                    if datapartindex!=otherdatapartindex:
                        if datapart_in_query[otherdatapartindex]<datapart_in_query[datapartindex]:
                            upperset|=queue[otherdatapartindex]
                            setforbg|=queue[otherdatapartindex]
                        elif datapart_in_query[otherdatapartindex]&datapart_in_query[datapartindex]!=set():
                            setforbg|=queue[otherdatapartindex]
                uppersets.append(upperset)
                setsforbg.append(setforbg)
            
            self.queues.append(queue)
            self.datapart_in_query_lists.append(datapart_in_query)
            self.uppersets_list.append(uppersets)
            self.setsforbg_lists.append(setsforbg)
            self.partindex_by_cluster = []
            self.partcover_by_cluster = []
            self.covers = [None for i in xrange(len(self.queues))]
        print 'PRECOMPUTING DONE'
            
    def process(self, machines, dataunit_in_machine):
        nprocessed = 0
        smartload = 0
        queues = self.queues
        datapart_in_query_lists = self.datapart_in_query_lists
        uppersets_list = self.uppersets_list
        nqueriesinclusters = self.nqueriesinclusters
        setsforbg_lists = self.setsforbg_lists

        for index in range(len(queues)):
            self.covers[index]=[set() for i in xrange(nqueriesinclusters[index])]

        start=time.time()

        for queueindex in xrange(len(queues)):
            queue=queues[queueindex]

            covered=set()
            dataunit_in_part = dict()
            part_cover = dict()
            part_index = -1
            for datapartindex in xrange(len(queue)):
                part_index += 1
                datapart=queue[datapartindex]-covered

                if datapart!=set():

                    #now we make machinesintersected
                    machinesintersected={}
                    machine_size={}

                    for dataunit in datapart:
                        dataunit_in_part[dataunit] = part_index
                        for machine in dataunit_in_machine[dataunit]:
                            if machine in machinesintersected:
                                machinesintersected[machine].add(dataunit)
                            else:
                                machinesintersected[machine]=set([dataunit])
                                machine_size[machine]=0

                    #now me make machine_size
                    for dataunit in setsforbg_lists[queueindex][datapartindex]:
                        for machine in dataunit_in_machine[dataunit]:
                            if machine in machinesintersected:
                                machine_size[machine]+=1


                    ncolumns=max(machine_size.itervalues())
                    columncounter=ncolumns

                    #then use the linear greedy

                    uncovered=datapart.copy()
                    cover=set()   

                    #make sets_of_size
                    sets_of_size={}
                    for machine in machinesintersected:
                        if len(machinesintersected[machine]) in sets_of_size:
                            sets_of_size[len(machinesintersected[machine])][machine_size[machine]].add(machine)
                        else:
                            sets_of_size[len(machinesintersected[machine])]=[set() for i in xrange(ncolumns+1)]
                            sets_of_size[len(machinesintersected[machine])][machine_size[machine]].add(machine)

                    rowcounter=max(sets_of_size.keys())

                    for i in range(1,rowcounter):
                        if not i in sets_of_size:
                            sets_of_size[i]=[set() for j in xrange(ncolumns+1)]

        #            for machine in machinesintersected:
        #                print machine
        #                print len(machinesintersected[machine])
        #                print machine_size[machine]
        #                print sets_of_size[len(machinesintersected[machine])][machine_size[machine]]
        #                print 'next'
        #            input("Press Enter to continue...")
                    while uncovered!=set():
                        if sets_of_size[rowcounter][columncounter]!=set():
                            #choose machine with biggest size in upperset
                            chosenmachine=sets_of_size[rowcounter][columncounter].pop()
                            cover.add(chosenmachine)

                            #do the post processing
                            for dataunit in machinesintersected[chosenmachine]:
                                for machine in dataunit_in_machine[dataunit]:
                                    if machine!=chosenmachine:
                                        length=len(machinesintersected[machine])
                                        size=machine_size[machine]
                                        machinesintersected[machine].remove(dataunit)
                                        # print length
                                        # print size
                                        # print sets_of_size
                                        # print uncovered
                                        sets_of_size[length][size].remove(machine)
                                        if length!=1:
                                            sets_of_size[length-1][size].add(machine)
                                uncovered.remove(dataunit)
                        else:
                            if columncounter>0:
                                columncounter-=1
                            else:
                                columncounter=ncolumns
                                rowcounter-=1

                    part_cover[part_index] = cover

                    #now we add the cover to appropriate covers for queries
                    for queryindex in datapart_in_query_lists[queueindex][datapartindex]:
                        smartload+=len(cover-self.covers[queueindex][queryindex])
                        self.covers[queueindex][queryindex]|=cover

                    #and the last thing, we need to remove appropriate elements from appropriate data parts
                    coveredinupperset=datapart.copy()
                    for dataunit in uppersets_list[queueindex][datapartindex]-datapart:
                        if not (dataunit_in_machine[dataunit]&cover)==set():
                            coveredinupperset.add(dataunit)

                    covered|=coveredinupperset
            self.partindex_by_cluster.append(dataunit_in_part)
            self.partcover_by_cluster.append(part_cover)
            nprocessed+=1
            print nprocessed
            
 #       end=time.time()

        #let's check this

        print 'COVERED'

        print 'SMART TOTAL LOAD'
#        print smartload

#        print (end-start)/float(nqueries)
