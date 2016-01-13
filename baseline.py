import time

def better_baseline(query, machines, dataunit_in_machine): 
    start = time.time()
    cover = set()
    uncovered = set(query)
    while len(uncovered) > 0: 
        de_to_cover = uncovered.pop()
        machine_ind = dataunit_in_machine[de_to_cover].pop()
        dataunit_in_machine[de_to_cover].add(machine_ind)
        uncovered = uncovered - machines[machine_ind]
        cover.add(machine_ind)

    return cover, time.time() - start

def baseline(query, machines, dataunit_in_machine): 
    start = time.time()
    potential_machines = set()
    for de in query: 
        potential_machines |= dataunit_in_machine[de]
    
    uncovered = set(query)
    cover = set()
    while uncovered != set(): 
        chosen = potential_machines.pop()
        uncovered = uncovered - machines[chosen]
        cover.add(chosen)

    return cover, time.time() - start
