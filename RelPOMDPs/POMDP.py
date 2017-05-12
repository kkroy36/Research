from Utils import Utils
class POMDP(object):
    '''class for the pomdp model'''
    def __init__(self):
        '''constructor for the model'''
        self.stateVariables=None
        self.states=None
        self.factoredStates=None
        self.stateFacts=None
        self.observations=None
        self.observationModel=None
        self.actions=None
        self.transitionMatrix=None
        self.immediateRewards=None
        self.beliefState=None
        self.horizon=None
        self.discountFactor=None

    def readModel(self,file):
        '''reads the pomdp model file'''
        model = Utils.readFile(file)
        self.getStates(model)
        self.getObservationModel(model)
        self.getActions(model)
        self.getTransitionMatrix(model)
        self.getImmediateRewards(model)
        self.getInitialBelief(model)
        self.getHorizon(model)
        self.getDiscountFactor(model)

    def getHorizon(self,model):
        '''returns the horizon length'''
        for line in model:
            if "horizon" in line:
                self.horizon = float(line.split("=")[1].strip())
                break
    def getDiscountFactor(self,model):
        '''returns discount factor'''
        for line in model:
            if "discountFactor" in line:
                self.discountFactor = float(line.split("=")[1].strip())
                break

    def getInitialBelief(self,model):
        '''returns the initial belief of the model'''
        self.beliefState = {}
        for line in model:
            if "initialBelief" in line:
                beliefs = line.split("=")[1].strip()[1:-1].split(",")
                break
        for state in self.states:
            self.beliefState[self.factoredStates[state]] = float(beliefs[self.states.index(state)])

    def getImmediateRewards(self,model):
        '''returns the immediate reward model'''
        self.immediateRewards = {}
        for line in model:
            if "reward:" in line:
                state = line.split(":")[1].strip().split("(")[1].split(",")[0]
                reward = float(line.split(":")[1].strip().split("(")[1].split(",")[1][:-1])
                self.immediateRewards[state] = reward

    def getActions(self,model):
        '''returns the actions possible in the model'''
        for line in model:
            if "actions = " in line:
                self.actions = line.split("=")[1].strip()[1:-1].split(",")
                break

    def getTransProbFromLine(self,line):
        '''returns transition probability from a transition line in the model'''
        return float(line.split(" ")[2].strip())

    def getActionFromLine(self,line):
        '''returns action from a transition line in the model'''
        return line.split("^")[1].split("(")[0]

    def getStateOneFromLine(self,line):
        '''returns state1 from a transition line in the model'''
        return line.split(" ")[1].split("^")[0][2:-1].split(",")[0]

    def getStateTwoFromLine(self,line):
        '''returns state2 from a transition line in the model'''
        return line.split("^")[0][2:-1].split(",")[1]

    def getTransitionMatrix(self,model):
        '''returns the transition matrix per action'''
        self.transitionMatrix = {}
        for action in self.actions:
            self.transitionMatrix[action] = {}
            for state1 in self.states:
                self.transitionMatrix[action][state1] = {}
                for state2 in self.states:
                    self.transitionMatrix[action][state1][state2] = False
        for line in model:
            if "transition:" in line:
                transProb = self.getTransProbFromLine(line)
                action = self.getActionFromLine(line)
                state1 = self.getStateOneFromLine(line)
                state2 = self.getStateTwoFromLine(line)
                self.transitionMatrix[action][state1][state2] = transProb
        for action in self.transitionMatrix.keys():
            for state1 in self.transitionMatrix[action].keys():
                missingStates = []
                for state2 in self.states:
                    if self.transitionMatrix[action][state1][state2] == False:
                        missingStates.append(state2)
                numberOfMissingStates = len(missingStates)
                total = sum([item for item in  self.transitionMatrix[action][state1].values() if item])
                for state in missingStates:
                    self.transitionMatrix[action][state1][state] = (1 - total)/float(numberOfMissingStates)

    def getStateVariables(self,model):
        '''returns the state variables used to describe a state'''
        for line in model:
            if "stateVariables" in line:
                return line.split("=")[1].strip()[1:-1].split(",")

    def getStateFacts(self,model):
        '''returns the facts of the states described by the state variables'''
        for line in model:
            if "stateFacts" in line:
                return line.split("=")[1].strip()[1:-1].split(",")

    def getFactoredState(self,state,stateFacts,model):
        '''returns the factored state as supported by the state facts'''
        factoredState = ""
        for variable in self.stateVariables:
            fact = variable+"("+state+")"
            if fact in stateFacts:
                factoredState += fact+"^"
            else:
                factoredState += "~"+fact+"^"
        return factoredState[:-1]

    def getFactoredStates(self,model):
        '''returns the states as conjunction of state variables'''
        stateDict = {}
        self.states = []
        self.stateFacts = self.getStateFacts(model)
        for line in model:
            if "states" in line:
                self.states = line.split("=")[1].strip()[1:-1].split(",")
                break
        for state in self.states:
            stateDict[state] = self.getFactoredState(state,self.stateFacts,model)
        return stateDict

    def getObservations(self,model):
        '''returns the observations of the pomdp model'''
        return [line.split("=")[1].strip()[1:-1].split(",") for line in model if "observations" in line][0]

    def getObservationFromLine(self,line):
        '''returns the observation part of the line'''
        return line.split("=>")[1].split(" ")[0].split("(")[0]

    def getObservationProbabilityFromLine(self,line):
        '''returns the observation probability of the line'''
        return float(line.split("=>")[1].split(" ")[1])

    def getObservationStateFromLine(self,line,model):
        '''returns the state for the observation'''
        state = line.split("=>")[1].split(" ")[0].split("(")[1][:-1]
        return self.getFactoredState(state,self.stateFacts,model)
    
    def getObservationModel(self,model):
        #method to constructs the observation model
        self.observationModel = {}
        self.observations = self.getObservations(model)
        for state in self.factoredStates:
            self.observationModel[self.factoredStates[state]] = {}
            for observation in self.observations:
                self.observationModel[self.factoredStates[state]][observation] = False
        for line in model:
            if "observation:" in line:
                obs = self.getObservationFromLine(line)
                obsProb = self.getObservationProbabilityFromLine(line)
                factoredState = self.getObservationStateFromLine(line,model)
                self.observationModel[factoredState][obs] = obsProb
        for factoredState in self.observationModel:
            missingObservations = []
            for observation in self.observationModel[factoredState]:
                if self.observationModel[factoredState][observation] == False:
                    missingObservations.append(observation)
            numberOfMissingObservations = len(missingObservations)
            if numberOfMissingObservations == 0:
                continue
            total = sum([item for item in  self.observationModel[factoredState].values() if item])
            for observation in missingObservations:
                self.observationModel[factoredState][observation] = (1 - total)/float(numberOfMissingObservations)
                    
    def getStates(self,model):
        '''method that returns the states of the model'''
        self.stateVariables = self.getStateVariables(model)
        self.factoredStates = self.getFactoredStates(model)
