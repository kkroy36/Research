from math import exp
from PomdpSolve import PomdpSolve
from Utils import Utils
class Cluster(object):
    '''class to compress belief state by clustering similar states'''
    factors = {}
    clusters = {}
    
    @staticmethod
    def getUniqueStates():
        '''gets unique states'''
        uniqueStates = {}
        for state in Cluster.factors:
            factor = Cluster.factors[state]
            if round(factor,1) not in uniqueStates.keys():
                uniqueStates[round(factor,1)] = state
                Cluster.clusters[state] = [state]
            else:
                oldState = uniqueStates[round(factor,1)]
                Cluster.clusters[oldState].append(state)
                uniqueStates[round(factor,1)] = state
        return Cluster.clusters.keys()

    @staticmethod
    def modifyObservations(model,missingStates):
        '''removes observation lines containing missing states'''
        modifiedLines = []
        for line in model:
            if "observation:" in line:
                if not Utils.contains(line,missingStates):
                    modifiedLines.append(line)
            else:
                modifiedLines.append(line)
        return modifiedLines

    @staticmethod
    def modifyStates(model,missingStates):
        '''modifies state descriptions to reflect clustering'''
        modifiedLines = []
        for line in model:
            if "states" in line:
                for state in missingStates:
                    newLine = line.replace(state,"")
                    newLine = newLine.replace(",,",",").replace("[,","[").replace(",]","]")
                    modifiedLines.append(newLine)
            elif "stateFacts" in line:
                factParts = line.split(",")
                if Utils.contains(factParts[0],missingStates):
                    factParts.remove(factParts[0])
                    factParts.insert(0,"stateFacts = [")
                for part in factParts[1:]:
                    if Utils.contains(part,missingStates):
                        factParts.remove(part)
                modifiedLines.append(",".join(factParts).replace("[,","["))
            else:
                modifiedLines.append(line)
        return modifiedLines

    @staticmethod
    def modifyInitialBelief(model,missingStates):
        '''modify the initial belief to sum over clustered states'''
        modifiedLines = []
        for line in model:
            if "initialBelief" in line:
                lineParts = line.split("=")
                for item in missingStates:
                    stateIndex = int(item.split("s")[1])-1
                    beliefs = lineParts[1].strip()[1:-1].split(",")
                    beliefs = [float(item) for item in beliefs]
                    item = beliefs[stateIndex]
                    n = len(beliefs)
                    for i in range(n):
                        if ("s"+str(i)) in Cluster.clusters.keys():
                            beliefs[i-1] *= len(Cluster.clusters[("s"+str(i))])
                    beliefs.remove(item)
                    beliefs = str(beliefs).replace(" ","")
                    modifiedLines.append(" = ".join([lineParts[0]]+[beliefs]))
            else:
                modifiedLines.append(line)
        return modifiedLines

    @staticmethod
    def modifyTransitionModel(model,missingStates):
        '''modifies the transition model with clusters'''
        modifiedLines = []
        for line in model:
            if "transition:" in line:
                if not Utils.contains(line,missingStates):
                    for state in Cluster.clusters:
                        n = len(Cluster.clusters[state])
                        if n > 1:
                            if state+","+state in line:
                                lineParts = line.split(" ")
                                lineParts[2] = str(n * float(lineParts[2]))
                                modifiedLines.append(" ".join(lineParts))
                            else:
                                modifiedLines.append(line)
            else:
                modifiedLines.append(line)
        return modifiedLines

    @staticmethod
    def modifyRewards(model,missingStates):
        '''modifies reward model'''
        modifiedLines = []
        for line in model:
            if "reward" in line:
                if not Utils.contains(line,missingStates):
                    modifiedLines.append(line)
            else:
                modifiedLines.append(line)
        return modifiedLines

    @staticmethod
    def modify(pomdpFile,pomdp):
        '''modifies pomdp description as per clusters formed'''
        uniqueStates = Cluster.getUniqueStates()
        missingStates = Utils.difference(pomdp.states,uniqueStates)
        model = Utils.readFile(pomdpFile)
        model = Cluster.modifyObservations(model,missingStates)
        model = Cluster.modifyStates(model,missingStates)
        model = Cluster.modifyInitialBelief(model,missingStates)
        model = Cluster.modifyTransitionModel(model,missingStates)
        model = Cluster.modifyRewards(model,missingStates)
        Utils.writeFile("modifiedPOMDP.pomdp",model)
        return "modifiedPOMDP.pomdp"
    
    @staticmethod
    def cluster(pomdp):
        '''cluster states according to signature'''
        numberOfStates = len(pomdp.states)
        for state in pomdp.states:
            Cluster.factors[state] = exp(numberOfStates) #for scaling small values
        for action in pomdp.actions:
            for observation in pomdp.observations:
                newBelief = PomdpSolve.computeNewBelief(pomdp,observation,action,pomdp.beliefState)
                Cluster.factors[state] *= newBelief[pomdp.factoredStates[state]]
        print Cluster.factors
