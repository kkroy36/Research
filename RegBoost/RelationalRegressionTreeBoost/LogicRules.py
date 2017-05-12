from Ilp import Ilp,Clause
from Utils import Utils
from os import system
class node(object):
    '''class that represents the logic nodes'''
    maxDepth = 20
    def __init__(self,clause,level,examples,parent,kind="root"):
        '''class constructor'''
        self.level = level
        self.clause = clause
        self.examples = examples
        self.parent = parent
        self.kind = kind

    def findBestClause(self,queue,iteration):
        '''finds best clause based on score'''
        if self.level == node.maxDepth:
            print "Found Rule: ",
            rule=""
            curr = self
            while curr.parent!="root":
                if curr.kind == "left":
                    rule += curr.parent.clause+"^"
                elif curr.kind == "right":
                    rule += "!"+curr.parent.clause+"^"
                curr = curr.parent
            ruleScore = Ilp.getMeanRegressionValue(self.examples)
            Ilp.updateInferenceValues(self.examples)
            Ilp.updateRegValues(self.examples,iteration)
            Utils.writeToFile(Ilp.target+" :- "+rule[:-1]+" score: "+str(ruleScore),"rules"+str(iteration+1)+".txt")
            print Ilp.target,":-",rule[:-1],"with Score: ",ruleScore
            return
        bestClause,bestScore = "",999
        bestTExamples,bestFExamples = None,None
        for typ in Ilp.types:
            clause = Clause(Ilp.target+":-"+typ)
            tExamples = Ilp.scoreClause(clause,self.examples)
            fExamples = Utils.difference(self.examples,tExamples)
            totalNumberOfExamples = len(self.examples)
            if totalNumberOfExamples == 0:
                break
            tScore = (len(tExamples)/float(totalNumberOfExamples))*Ilp.getVariance(tExamples)
            fScore = (len(fExamples)/float(totalNumberOfExamples))*Ilp.getVariance(fExamples)
            score = tScore + fScore
            if score < bestScore:
                bestScore = score
                bestClause = typ
                bestTExamples = tExamples
                bestFExamples = fExamples
        self.clause = bestClause
        if bestClause!="":
            Ilp.types.remove(bestClause)
            if len(bestTExamples) > 0:
                queue.insert(0,node(None,self.level+1,bestTExamples,self,"left"))
            if len(bestFExamples) > 0:
                queue.insert(0,node(None,self.level+1,bestFExamples,self,"right"))
        print "Found Rule: ",
        rule=""
        curr = self
        while curr.parent!="root":
            if curr.kind == "left":
                rule += curr.parent.clause+"^"
            elif curr.kind == "right":
                rule += "!"+curr.parent.clause+"^"
            curr = curr.parent
        if rule!="":
            ruleScore = Ilp.getMeanRegressionValue(self.examples)
            Ilp.updateInferenceValues(self.examples)
            Ilp.updateRegValues(self.examples,iteration)
            Utils.writeToFile(Ilp.target+" :- "+rule[:-1]+" score: "+str(ruleScore),"rules"+str(iteration+1)+".txt")
            print Ilp.target,":-",rule[:-1],"with Score: ",ruleScore

class logicRules(object):
    '''class that learns the logic rules'''
    nodeQueue = None
    boostingIterations = 5

    @staticmethod
    def readData():
        '''reads all ilp data to ilp structures'''
        Ilp.readFacts("facts.txt")
        Ilp.readExamples("examples.txt")
        Ilp.readRegressionValues("exampleReg.txt")
    
    @staticmethod
    def setup(combined=False):
        '''set's up the ilp variables and the queue'''
        logicRules.nodeQueue = []
        Ilp.readTypes("types.txt")
        if not combined:
            print "="*80,"\n---------------LEARNING LOGIC RULES---------------:"
        else:
            print "="*80,"\n---------------COMBINED LOGIC RULES---------------:"
        logicRules.nodeQueue.insert(0,node(None,0,Ilp.examples,"root"))

    @staticmethod
    def getCombinedTree():
        '''builds combined tree on final Regression values'''
        logicRules.setup(True)
        while len(logicRules.nodeQueue) > 0:
            curr = logicRules.nodeQueue.pop()
            curr.findBestClause(logicRules.nodeQueue,(logicRules.boostingIterations))

    @staticmethod
    def getFinalRegValues():
        '''returns combined regression values for combined tree'''
        for example in Ilp.examples:
            Ilp.regValues[example] = float(Ilp.prior) - float(Ilp.inferenceValues[example])

    @staticmethod
    def learnRules():
        '''learns the rules by repeatedly calling the theorem prover'''
        logicRules.readData()
        for iteration in range(logicRules.boostingIterations):
            logicRules.setup()
            while len(logicRules.nodeQueue) > 0:
                curr = logicRules.nodeQueue.pop()
                curr.findBestClause(logicRules.nodeQueue,(iteration))
        logicRules.getFinalRegValues()
        logicRules.getCombinedTree()
