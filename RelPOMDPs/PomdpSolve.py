from Utils import Utils
class PomdpSolve(object):
    '''value iteration class'''
    @staticmethod
    def computeNewBelief(pomdp,observation,action,beliefState):
        '''computes new belief state'''
        newBeliefState = {}
        for state2 in pomdp.states:
            probOfObsInState2 = pomdp.observationModel[pomdp.factoredStates[state2]][observation]
            dotProduct = 0
            numberOfStates = len(pomdp.states)
            for state1 in pomdp.states:
                dotProduct += pomdp.transitionMatrix[action][state1][state2]*beliefState[pomdp.factoredStates[state1]]
            newBeliefState[pomdp.factoredStates[state2]] = probOfObsInState2*dotProduct
        return Utils.normalize(newBeliefState)

    @staticmethod
    def immediateValueOfBeliefState(pomdp,beliefState):
        '''returns immediate value of beliefState'''
        value = 0
        for state in pomdp.states:
            value += beliefState[pomdp.factoredStates[state]]*pomdp.immediateRewards[state]
        return value

    @staticmethod
    def computeActionObservationValue(pomdp,beliefState,horizon,action,observation):
        '''computes the value of a pomdp recursively'''
        if horizon == pomdp.horizon:
            return PomdpSolve.immediateValueOfBeliefState(pomdp,beliefState)
        beliefState = PomdpSolve.computeNewBelief(pomdp,observation,action,beliefState)
        value = PomdpSolve.computeActionObservationValue(pomdp,beliefState,(horizon+1),action,observation)*pomdp.discountFactor
        return value

    @staticmethod
    def computeValue(pomdp,beliefState,horizon):
        '''computes the value of belief state by value iteration'''
        maxValue = -99999
        for action in pomdp.actions:
            actionValue = 0
            for observation in pomdp.observations:
                value = PomdpSolve.computeActionObservationValue(pomdp,beliefState,horizon,action,observation)
                actionValue += value
                if actionValue > maxValue:
                    maxValue = actionValue
        return maxValue
