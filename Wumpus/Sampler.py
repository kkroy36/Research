from Matrix import matrix
from random import random
from copy import deepcopy
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator,  FormatStrFormatter
from sklearn import ensemble
from sklearn.tree import DecisionTreeRegressor,export_graphviz
from sklearn.neural_network import MLPRegressor
from os import system

class Sampler(object):
    '''class for sampling based on domain'''
    
    def __init__(self,grid):
        '''constructor to initialize sampler'''
        self.grid = grid
        self.value = {}
        self.count = {}
        self.transferModel = None

    def getTransferModel(self):
        '''returns the transfer model to use
           in another wumpus world
        '''
        return self.transferModel

    def start(self):
        '''returns a random initial state'''
        x,y = int(random()*self.grid.size),int(random()*self.grid.size)
        while True:
            if self.grid.valid(x,y):
                return (x,y)
            x,y = int(random()*self.grid.size),int(random()*self.grid.size)

    def getValue(self,s):
        '''returns state value'''
        if s in self.value.keys():
            return self.value[s]
        else:
            return 0

    def chooseAction(self,s):
        '''decides optimal action to choose in s
           breaks ties at random
        '''
        actionValues = []
        bestAction = None
        bestValue = float("-inf")
        for action in self.grid.actions:
            s_t = self.grid.takeAction(s[0],s[1],action)
            value = self.getValue(s_t)
            actionValues += [value]
            if value > bestValue:
                bestValue = value
                bestAction = action
        if sum(actionValues) == 4*actionValues[0]:
            bestAction = self.grid.actions[int(random()*len(self.grid.actions))]
        return bestAction     

    def sample(self,discount,action,MAX):
        '''generates one sample i.e. trajectory'''
        s = self.start()
        #print "start state: ",s,
        s0 = deepcopy(s)
        t = [s0]
        if action:
            print "actions taken: "
        while True:
            if len(t) > MAX:
                break
            if s[0] == self.grid.goal_x and s[1] == self.grid.goal_y:
                if s0 == s:
                    if action:
                        print "noOp"
                else:
                    break
            if self.grid.grid[s[0]][s[1]] == 1:
                break
            a = self.chooseAction(s)
            s = self.grid.takeAction(s[0],s[1],a)
            #print "next state: ",s,
            if action:
                print a,
            t += [s]
        if action:
            print "\n"
        print "\n"
        return t

    def getCountMatrix(self):
        '''returns a diagonal matrix of counts for each state'''
        n = len(self.count)
        C = [[0 for i in range(n)] for i in range(n)]
        pos = 0
        for key in self.count:
            C[pos][pos] = self.count[key]
            pos += 1
        return matrix(C)

    def getDataMatrix(self):
        '''returns the data matrix of values'''
        X = []
        for key in self.value:
            X.append(self.grid.factored(key[0],key[1]))
        return matrix(X)

    def getRegressionValues(self):
        '''returns the values of each state'''
        Y = []
        for key in self.value:
            Y.append([self.value[key]])
        return matrix(Y)

    def getWeight(self,X,Y,C):
        '''returns the weights if succeeded else returns false'''
        XtransposeCXinverse,XtransposeCY = None,None
        try:
            XtransposeCXinverse = (X.transpose()*C*X).inverse()
        except:
            print "Matrix not invertible, generating new sample"
            return False
        try:
            XtransposeCY = (X.transpose()*C*Y)
        except:
            print "matrix operation failure, generating new sample"
            return False
        return XtransposeCXinverse*XtransposeCY

    def getPhiNew(self,X,BE):
        '''appends bellman error as new basis'''
        Xnew = []
        k = 0
        for item in self.value:
            x = X.value[k]
            Xnew.append(x+[BE[k]])
            k += 1
        return matrix(Xnew)

    def visualize_tree(self,tree,feature_names,treeName):
        '''create tree png file'''
        with open(treeName+".dot",'w') as f:
            export_graphviz(tree,out_file=f,feature_names=feature_names)
        system("dot -Tpng "+treeName+".dot "+"-o "+treeName+".png")
        #system("open "+treeName+".png")

    def GBFit(self,X,Y,loss="ls",printTree=False,treeName=False,initModel=False):
        '''fits gradient boosted regression trees
           using specified loss function to minimize
           bellman error
        '''
        Xnew = []
        Ynew = []
        for item in X.value:
            Xnew.append(item)
            Ynew.append(Y.value[X.value.index(item)][0])
        Xnew,Ynew = np.array(Xnew),np.array(Ynew)
        #print Xnew
        #print Ynew
        params = {'n_estimators':500, 'max_depth': 2, 'min_samples_split':2, 'learning_rate': 0.01, 'loss': loss, 'subsample':0.9}
        if initModel:
            return initModel.predict(Xnew)
        reg = ensemble.GradientBoostingRegressor(**params)
        reg.fit(Xnew,Ynew)
        Y_hat = reg.predict(Xnew)
        if printTree:
            self.transferModel = reg
            #dt = DecisionTreeRegressor(random_state=0)
            #dt.fit(Xnew,Y_hat)
            #self.visualize_tree(dt,["row","col","stench","breeze"],treeName)
        Y_hat_return = {}
        N = len(Y_hat)
        for i in range(N):
            xi = Xnew[i]
            yi = Y_hat[i]
            print xi, yi
            xiUnfactored = self.grid.unfactored(xi)
            Y_hat_return[xiUnfactored] = float(reg.predict(np.array(xi)))
        return Y_hat_return

    def NNFit(self,X,Y):
        '''fits neural network with
           stochastic gradient descent
           and logistic activation
        '''
        Xnew,Ynew = [],[]
        for item in X.value:
            Xnew.append(item)
            Ynew.append(Y.value[X.value.index(item)][0])
        Xnew,Ynew = np.array(Xnew),np.array(Ynew)
        reg = MLPRegressor(solver='lbfgs',activation='logistic',alpha=1e-5,hidden_layer_sizes=(10,2),random_state=1)
        reg.fit(Xnew,Ynew)
        Y_hat = reg.predict(Xnew)
        return Y_hat 

    def getSamples(self,N,discount=1,action=False,approx=False,method='LSReg',init=False):
        '''generates N samples'''
        MAX = self.grid.size**4
        values = {}
        self.value = {}
        for i in range(N):
            print "="*20 + " trajectory "+str(i+1)+" "+"="*20
            print "generating sample: ",i
            t = self.sample(discount,action,MAX)
            if len(t) < MAX:
                dataSet = deepcopy(self.updateValues(t,discount))
            print "value before: ",self.value
            if approx:
                if method == 'LSReg':
                    print "method is LSReg"
                    if len(self.value) > 0:
                        C = self.getCountMatrix()
                        X = self.getDataMatrix()
                        Y = self.getRegressionValues()
                        W = self.getWeight(X,Y,C)
                        if not W:
                            continue
		        BE = []
                        for key in self.value:
                            x = [[v] for v in self.grid.factored(key[0],key[1])]
                            Y_hat = (W.transpose()*matrix(x)).value[0][0]
                            BE.append(self.value[key] - Y_hat)
                        X = self.getPhiNew(X,BE)
                        W = self.getWeight(X,Y,C)
                        if not W:
                            continue
                        j = 0
                        for key in self.value:
                            Xj = X.value[j]
                            Xj = matrix([[item] for item in Xj])
                            Y_hat = (W.transpose()*Xj).value[0][0]
                            self.value[key] = Y_hat
                            j += 1
                elif method == 'GB':
                    print "method is GB"
                    if len(self.value) > 0:
                        X = dataSet[0]
                        Y = dataSet[1]
                        #X = self.getDataMatrix()
                        #Y = self.getRegressionValues()
                        Y_hat = self.GBFit(X,Y,loss="ls")
                        '''
                        if i ==0 and init:
                            Y_hat = self.GBFit(X,Y,loss="ls",initModel=init)
                        elif i == N-1 or i == N-2:
                            Y_hat = self.GBFit(X,Y,loss="ls",printTree=True,treeName="basis"+str(i))
                        else:
                            Y_hat = self.GBFit(X,Y,loss="ls")
                        '''
                        j = 0
                        nY = len(Y_hat)
                        for i in range(nY):
                            unfactoredState = self.grid.unfactored(X.value[i])
                            print "compressed state: ",unfactoredState
                            print "keys: ",self.value
                            print unfactoredState in self.value.keys()
                            if unfactoredState in self.value.keys():
                                self.value[unfactoredState] = Y_hat[unfactoredState]
                        '''
                        for key in self.value:
                            y_hat = self.grid.factored(key[0],key[1])
                            self.value[key] = Y_hat[j]
                            j += 1
                        '''
                elif method == 'NN':
                    print "method is NN"
                    if len(self.value) > 0:
                        X = self.getDataMatrix()
                        Y = self.getRegressionValues()
                        Y_hat = self.NNFit(X,Y)
                        j = 0
                        for key in self.value:
                            self.value[key] = Y_hat[j]
                            j += 1
            print "value after: ",self.value                 
            values[i] = deepcopy(self.value)
        return values

    def getValue(self,s):
        '''returns the current estimate of the value of the state'''
        if s in self.value.keys():
            return self.value[s]
        else:
            return 0

    def setValue(self,s,v,discount,exponent):
        '''performs gradient update to value of state'''
        if s in self.value.keys():
            alpha = 1/float(self.count[s])
            self.value[s] += alpha*(v-self.value[s])*(discount**exponent)
        elif s not in self.value.keys():
            self.value[s] = v*(discount**exponent)

    def setCount(self,s):
        '''update sthe count of the state being visited'''
        if s in self.count.keys():
            self.count[s] += 1
        elif s not in self.count.keys():
            self.count[s] = 1

    def updateValues(self,t,discount):
        '''update values based on trajectory'''
        n = len(t)
        print "updating value of state sequence: ",t
        R  = [self.grid.reward(s[0],s[1]) for s in t]
        X = []
        Y = []
        for i in range(n-1,-1,-1):
            self.setCount(t[i])
            X.append(self.grid.factored(t[i][0],t[i][1]))
            exponent = (n-1)-i
            if i == n-1:
                self.setValue(t[i],R[i],discount,exponent)
                Y.append(R[i])
            else:
                transitionValue =  self.getValue(t[i+1])
                self.setValue(t[i],R[i]+transitionValue,discount,exponent)
                Y.append(R[i]+transitionValue)
        return (matrix(X),matrix([[j] for j in Y]))
