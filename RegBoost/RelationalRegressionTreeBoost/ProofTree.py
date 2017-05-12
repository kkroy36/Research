from copy import deepcopy
class treeNode(object):
    '''class for a node in the proof tree'''
    def __init__(self,variableBindings,predicate):
        '''constructor for the class'''
        self.variableBindings = variableBindings
        self.predicate = predicate
        self.proved = False

    def allVariablesBound(self,fact):
        '''check if proved'''
        for variable in self.variableBindings:
            if self.variableBindings[variable] == "unbound":
                return False
            else:
                if variable in self.predicate.variables:
                    pos = self.predicate.variables.index(variable)
                    if not fact.objects[pos] == self.variableBindings[variable]:
                        return False
        return True

    def matchFound(self,fact):
        '''find a fact that matches'''
        match = True
        for variable in self.variableBindings:
            if not self.variableBindings[variable] == "unbound":
                obj = self.variableBindings[variable]
                if variable in self.predicate.variables:
                    if fact.objects[self.predicate.variables.index(variable)] != obj:
                        match = False
                        break
        return match

    def bindUnboundVariables(self,fact):
        '''binds unbound variables if match found'''
        newVariableBindings = deepcopy(self.variableBindings)
        for variable in newVariableBindings:
            if newVariableBindings[variable] == "unbound":
                pos = self.predicate.variables.index(variable)
                newVariableBindings[variable] = fact.objects[pos]
        return newVariableBindings

    def searchFacts(self,facts,stack):
        '''searches facts for variable bindings'''
        for fact in facts:
            if self.predicate.relation == fact.relation:
                if self.allVariablesBound(fact):
                    self.proved = True
                else:
                    if self.matchFound(fact):
                        stack.append(treeNode(self.bindUnboundVariables(fact),self.predicate))
                        
class ProofTree(object):
    '''class for proof tree'''
    stack = [] #node stack
    
    @staticmethod
    def constructProofTree(predicate,facts,variableBindings):
        '''method that constructs proof tree'''
        ProofTree.stack.append(treeNode(variableBindings,predicate))
        while len(ProofTree.stack)!=0:
            node = ProofTree.stack.pop()
            node.searchFacts(facts,ProofTree.stack)
            if node.proved:
                return True
                #print node.variableBindings,node.predicate.relation
            else:
                return False
                #print node.variableBindings,node.predicate.relation
