from Utils import Utils
class POMDP(object):
    '''class for pomdp'''
    states = []
    actions = []
    observations = []
    obsModel = {}
    transModel = {}
    @staticmethod
    def readStates(model):
        '''reads the states of the model'''
        for line in model:
            if "states" in line.lower():
                POMDP.states = line.split("=")[1].strip()[1:-1].split(',')
                break

    @staticmethod
    def readActions(model):
        '''reads the possible actions'''
        for line in model:
            if "actions" in line.lower():
                POMDP.actions = line.split("=")[1].strip()[1:-1].split(',')
                break

    @staticmethod
    def readObservations(model):
        '''reads observations on states and updates dictionary'''
        for line in model:
            if "observations" in line and '(' not in line.lower():
                POMDP.observations = line.split("=")[1].strip()[1:-1].split(',')
                break
        for line in model:
            if "observations(" in line.lower():
                state = line.split("=")[0].split('(')[1].strip()[:-1]
                POMDP.obsModel[state] = {}
                obsAndProbs = line.split("=")[1].strip()[1:-1].split(',')
                for item in obsAndProbs:
                    obs,value = item.split(':')[0],float(item.split(':')[1])
                    POMDP.obsModel[state][obs] = value

    @staticmethod
    def readTransitionModel(model):
        '''reads in the transition model'''
        for line in model:
            if 't(' in line.lower():
                action = line.split("=")[0].split('(')[1].strip()[:-1]
                POMDP.transModel[action] = {}
                matrixRows = line.split("=")[1].strip()[1:-1].split(';')
                nRows = len(matrixRows)
                for i in range(nRows):
                    state1 = "s"+str(i+1)
                    POMDP.transModel[action][state1] = {}
                    row = matrixRows[i][1:-1]
                    values = [float(item) for item in row.split(',')]
                    nValues = len(values)
                    for j in range(nValues):
                        state2 = "s"+str(j+1)
                        POMDP.transModel[action][state1][state2] = values[j]
        
    @staticmethod
    def readModel(fileName):
        '''reads the pomdp model'''
        model = Utils.readFile(fileName)
        POMDP.readStates(model)
        POMDP.readActions(model)
        POMDP.readObservations(model)
        POMDP.readTransitionModel(model)
