import random
def generate(data, m, rep=3): 
#m is the number of machines

# There have to be at least as many machines as the repetition
    if m < rep: 
        m = rep

    machines = [set([]) for i in range(m)]
    
    for d in data: 
        for r in range(rep):
            flag = True
            while flag or (d in machines[i]): 
                flag = False
                i = random.randint(0,m-1)
            machines[i].add(d)
    return machines

def test(data, machines, rep): 
    for d in data: 
        counter = 0
        for m in machines: 
            if d in m: 
                counter += 1

        if counter != rep:
            print "ERROR"
            print d
            print counter, ' in machines'
    
    print 'Done'

#data = range(100)
#machines = generate(data, 10)
#test(data, machines, 3)

