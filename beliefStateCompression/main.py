from POMDP import POMDP
from random import randint
from Cluster import Cluster
from sys import argv
def main():
    '''main method'''
    POMDP.readModel(argv[1])
    nStates = len(POMDP.states)
    randomNumbers = [randint(1,10) for i in range(nStates)]
    initialBelief = {}
    for i in range(nStates):
        initialBelief[POMDP.states[i]] = randomNumbers[i]/float(sum(randomNumbers))
    print "initialBelief: ",initialBelief
    Cluster.cluster(POMDP.states,POMDP.obsModel,POMDP.transModel,POMDP.actions,POMDP.observations,initialBelief)

main()
