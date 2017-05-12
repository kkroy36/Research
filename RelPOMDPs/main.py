from PomdpSolve import PomdpSolve
from POMDP import POMDP
from Cluster import Cluster
from sys import argv
def main():
    '''main method'''
    pomdp = POMDP()
    pomdpFileIndex = argv.index("-pomdp")+1
    pomdpFile = argv[pomdpFileIndex]
    pomdp.readModel(pomdpFile)
    if "-cluster" in argv:
        Cluster.cluster(pomdp)
        modifiedFile = Cluster.modify(pomdpFile,pomdp)
        modifiedPOMDP = POMDP()
        modifiedPOMDP.readModel(modifiedFile)
        print PomdpSolve.computeValue(modifiedPOMDP,modifiedPOMDP.beliefState,1)
    else:
        print PomdpSolve.computeValue(pomdp,pomdp.beliefState,1)
main()
