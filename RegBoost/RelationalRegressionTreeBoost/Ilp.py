from Utils import Utils
from Prover import Prover
class Predicate(object):
    '''relation object'''
    def __init__(self,predicate):
        '''constructor for relation object'''
        self.relation = predicate.split("(")[0]
        arguments = predicate.split("(")[1][:-1]
        if ',' not in arguments:
            self.arity = 1
            self.variables = [arguments]
        else:
            self.arity = len(arguments.split(','))
            self.variables = arguments.split(',')
            
class Clause(object):
    '''clause object'''
    def __init__(self,clause):
        '''constructor for clause object'''
        if ":-" in clause:
            self.head = Predicate(clause.split(":-")[0])
            bodyElements = clause.split(":-")[1]
            if '^' not in bodyElements:
                self.body = [Predicate(bodyElements)]
            else:
                bodyClauses = bodyElements.split("^")
                self.body = [Predicate(bodyClause) for bodyClause in bodyClauses][::-1]
        else:
            self.head = Predicate(clause)
            self.body = False
    
class Fact(object):
    '''fact object'''
    def __init__(self,fact):
        '''constructor'''
        self.relation = fact.split("(")[0]
        arguments = fact.split("(")[1][:-2]
        if ',' not in arguments:
            self.arity = 1
            self.objects = [arguments]
        else:
            self.arity = len(arguments.split(','))
            self.objects = arguments.split(',')
                
class Ilp(object):
    '''class for inductive logic programming'''
    facts = None
    examples = None
    types = None
    target = None
    regValues = {}
    trueValues = {}
    inferenceValues = {}
    clauses = []
    prior = None
    
    @staticmethod
    def readFacts(fileName):
        '''reads facts into facts list'''
        facts = Utils.readFile(fileName)
        print "="*80,"\n----------------FACTS READ-------------------: "
        for fact in facts:
            print fact
        Ilp.facts = [Fact(fact) for fact in facts]

    @staticmethod
    def readExamples(fileName):
        '''reads positive examples into pos list'''
        print "="*80,"\n---------------POSITIVE EXAMPLES---------------:"
        examples = Utils.readFile(fileName)
        for example in examples:
            print example
        Ilp.examples = examples

    @staticmethod
    def readRegressionValues(fileName):
        '''reads the regression values for the positive examples'''
        values = Utils.readFile(fileName)[0].split(',')
        nValues = len(values)
        Ilp.prior = sum([float(value) for value in values])/float(nValues)
        for i in range(nValues):
            Ilp.trueValues[Ilp.examples[i]] = values[i]
        for example in Ilp.examples:
            Ilp.regValues[example] = float(Ilp.trueValues[example]) - Ilp.prior
            Ilp.inferenceValues[example] = Ilp.prior
            
    @staticmethod
    def readTypes(fileName):
        '''reads the type of each variable in the predicate'''
        types = Utils.readFile(fileName)
        Ilp.target = types[0]
        Ilp.types = types[1:]

    @staticmethod
    def getMeanRegressionValue(examples):
        '''returns mean regression value of examples'''
        total = 0
        for example in examples:
            total += Ilp.regValues[example]
        return total/float(len(examples))

    @staticmethod
    def getVariance(examples):
        '''returns mean regression value for all examples'''
        variance,total,squaredDifference = 0,0,0
        nExamples = len(examples)
        if nExamples == 0:
            return total
        for example in examples:
            total += float(Ilp.regValues[example])
        mean = total/float(nExamples)
        for example in examples:
            squaredDifference += (float(Ilp.regValues[example])-mean)**2
        return squaredDifference/float(nExamples)

    @staticmethod
    def updateInferenceValues(examples):
        '''updates inference values after each iteration of boosting'''
        total = 0
        for example in examples:
            total += float(Ilp.regValues[example])
        for example in examples:
            Ilp.inferenceValues[example] += total/float(len(examples))

    @staticmethod
    def updateRegValues(examples,iteration):
        '''updates regression values to error for boosting'''
        for example in examples:
            Ilp.regValues[example] = (float(Ilp.trueValues[example]) - float(Ilp.inferenceValues[example]))
                
    @staticmethod
    def scoreClause(clause,examples):
        '''scores a clause'''
        trueExamples = []
        for example in examples:
            if Prover.proveClause(Ilp.facts,clause,Fact(example)):
                trueExamples.append(example)
        return trueExamples
