import time 
import sys

def linear_greedy(query, machines, dataunit_in_machine):
    query = set(query)
    greedystart=time.time()
    if query == set(): 
        return set(), time.time() - greedystart
    machinesintersected = intersect_machine_query(query, machines, dataunit_in_machine)
    uncovered = set(query)
    cover=set()

    sets_of_size={}
    for i in range(1,len(query)+1):
        sets_of_size[i]=set([])
    for machine_ind in machinesintersected:        
        machine = machinesintersected[machine_ind]

        if len(machine) in sets_of_size:
            sets_of_size[len(machine)].add(machine_ind)
        else: 
            sets_of_size[len(machine)] = set([machine_ind])
    try: 
        counter=max(sets_of_size.keys())
    except ValueError: 
        print sets_of_size
        print machinesintersected
        print END

    while uncovered != set():
        if counter <= 0: 
            print 'ERROR!'
            print 'Covered:', cover
            print 'Query:', query
            print 'Uncovered:', uncovered
            return 'FUCK', 'BAD'
#        print len(uncovered)
        if counter in sets_of_size and sets_of_size[counter] != set():
            chosenmachine=sets_of_size[counter].pop()
            cover.add(chosenmachine)
#            greedyload+=1
            for dataunit in machinesintersected[chosenmachine]:
                for machine in dataunit_in_machine[dataunit]:
                    if machine!=chosenmachine:
                        length=len(machinesintersected[machine])
                        machinesintersected[machine].remove(dataunit)
                        sets_of_size[length].remove(machine)
                        if length!=1:
                            sets_of_size[length-1].add(machine)
                uncovered.remove(dataunit)
        else:
            counter-=1

    greedyend=time.time()
    
    return cover, greedyend - greedystart

def intersect_machine_query(query,machines, dataunit_in_machine):
    machinesintersected = {}
    for de in query: 
        for machine in dataunit_in_machine[de]:
            if machine in machinesintersected:
                machinesintersected[machine].add(de)
            else: 
                machinesintersected[machine] = set([de])

    return machinesintersected

def generate_hash(machines, data_size):
    dataunit_in_machine = [set() for i in xrange(data_size)]
    for idx, m in enumerate(machines): 
        for i in m: 
            dataunit_in_machine[i].add(idx)

    return dataunit_in_machine
