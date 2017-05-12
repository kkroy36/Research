from math import exp
class Cluster(object):
    '''clustering class'''
    clusters = {}
    factors = {}
    @staticmethod
    def computeNewBelief(transState,action,observation,beliefState,obsModel,transModel,states):
        '''computes the new belief state'''
        if observation in obsModel[transState].keys():
            probOfObsInState = obsModel[transState][observation]
            dotProduct = 0
            nStates = len(states)
            for state in states:
                dotProduct += transModel[action][state][transState]*beliefState[state]
            return probOfObsInState*dotProduct*exp(nStates) #to scale up the values
        else:
            return 1
        
    @staticmethod
    def cluster(states,obsModel,transModel,actions,observations,beliefState):
        '''clusters the states according to the definition'''
        for state in states:
            product = 1
            for action in actions:
                for observation in observations:
                    newBelief = Cluster.computeNewBelief(state,action,observation,beliefState,obsModel,transModel,states)
                    product *= newBelief+0.00001 #smoothing for zero values
            Cluster.factors[state] = product
        li = []
        for i in range(len(Cluster.factors)):
            li.append(str(beliefState["s"+str(i+1)]))
        print str("[")+",".join(li)+str("]")
        print Cluster.factors
