from ProofTree import ProofTree
class Prover(object):
    '''theorem prover'''
    variableBindings = {}

    @staticmethod
    def getVariables(clause):
        '''get variables in head and body'''
        for variable in clause.head.variables:
            Prover.variableBindings[variable] = "unbound"
        if not clause.body:
            return
	for predicate in clause.body:
            for variable in predicate.variables:
                Prover.variableBindings[variable] = "unbound"

    @staticmethod
    def bindVariables(clause,fact):
        '''bind variables in clause head'''
        head = clause.head
        if head.relation != fact.relation:
            print "relations dont match!"
            exit()
        objectsInFact = fact.objects
        variablesInHead = head.variables
        for variable in variablesInHead:
            Prover.variableBindings[variable] = objectsInFact[variablesInHead.index(variable)]
    
    @staticmethod
    def proveClause(facts,clause,fact):
        '''proves the clause based on facts'''
        Prover.getVariables(clause)
        Prover.bindVariables(clause,fact)
	if not clause.body:
	    return ProofTree.constructProofTree(clause.head,facts,Prover.variableBindings)
	else:
            for predicate in clause.body:
                 return ProofTree.constructProofTree(predicate,facts,Prover.variableBindings)
