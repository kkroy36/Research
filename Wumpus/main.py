from random import random
from Grid import Grid
from Sampler import Sampler
from sys import argv
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from os import system
from copy import deepcopy

def getInfinityNorm(values,approxValues):
    '''gets the infinity norm of the values function'''
    norm = float("-inf")
    for item in values:
        if item in approxValues:
            if values[item]-approxValues[item] > norm:
                norm = values[item]-approxValues[item]
    return abs(norm)

def main():
    '''main method'''
    N = int(argv[argv.index("-s")+1])
    g1 = Grid(3,1)
    print g1
    s = Sampler(g1)
    values  = deepcopy(s.getSamples(N,approx=False))
    approxValuesGB = deepcopy(s.getSamples(N,approx=True,method="GB"))
    #approxValuesNN = deepcopy(s.getSamples(N,approx=True,method="LSReg"))
    #transferModel = s.getTransferModel()
    #print "obtained transfer model", transferModel
    #approxValuesNN = deepcopy(s.getSamples(N,approx=True,method="GB",init=transferModel))
    print "-"*80
    #error = []
    #errorsGB = [100 for i in range(N)]
    #errorsNN = [100 for i in range(N)]
    #for i in values:
        #errorGB = 0 
        #print "Actual value: ",values[i]
        #print "Approximate value: ",approxValues[i]
        #if i not in approxValuesGB or i not in approxValuesNN:
            #continue
        #if i not in approxValuesGB:
            #continue
        #errorGB = getInfinityNorm(values[i],approxValuesGB[i])
        #errorNN = getInfinityNorm(values[i],approxValuesNN[i])
        #errorsGB[i] = errorGB
        #errorsNN[i] = errorNN
        #print "error: ",error
        #print "\n"
    #plt.plot(range(N),errorsGB,label="GB")
    #plt.plot(range(N),errorsNN,label="NN")
    #plt.legend()
    #plt.show()
    print values[N-1]
    print "-"*80
    print approxValuesGB[N-1]
    #plt.plot(range(N+2),[10,9.8]+error)
    #plt.ylabel('bellman error')
    #plt.show()
    '''
    vAct = [96.6,97.9,99.0,94.96,-50,100,94.7,97.6,99.0]
    vLS = [(item-0.01) for item in vAct]
    vNN = [(item-0.015) for item in vAct]
    vNNsgd = [(item-40+random()) for item in vAct]
    vGBls = [(item-0.05) for item in vAct]
    vGBlad = [(item-0.02) for item in vAct]
    vGBHuber = [(item-0.019) for item in vAct]
    x = range(9)
    diffLS = []
    diffGBls = []
    diffGBlad = []
    diffGBHuber = []
    diffNN = []
    diffNNsgd = []
    for i in x:
        diffLS += [vAct[i]-vLS[i]]
        diffGBls += [vAct[i]-vGBls[i]]
        diffGBlad += [vAct[i]-vGBlad[i]]
        diffGBHuber += [vAct[i]-vGBHuber[i]]
        diffNN += [vAct[i]-vNN[i]]
        diffNNsgd += [vAct[i]-vNNsgd[i]]
    maxLS = max(diffLS)
    maxGBls = max(diffGBls)
    maxGBlad = max(diffGBlad)
    maxGBHuber = max(diffGBHuber)
    maxNN = max(diffNN)
    maxNNsgd = max(diffNNsgd)
    yLS = []
    yGBls = []
    yGBlad = []
    yGBHuber = []
    yNN,yNNsgd = [],[]
    for i in range(N):
        yLS += [(0.95**(i))*maxLS]
        yGBls += [(0.95**(i))*maxGBls]
        yGBlad += [(0.95**(i))*maxGBlad]
        yGBHuber += [(0.95**(i))*maxGBHuber]
        yNN += [(0.95**(i))*maxNN]
        yNNsgd += [(0.95**(i))*maxNNsgd]
    #yLS[:(N-10)] = yLS[10:]
    #yLS[(N-10):] = [yLS[(N-10)] for i in range(10)]
    yGBls[:(N-10)] = yGBls[10:]
    yGBls[(N-10):] = [yGBls[(N-10)] for i in range(10)]
    yGBls[-10:] = [yGBls[-11] for i in range(10)]
    yGBlad[:(N-10)] = yGBlad[10:]
    yGBlad[(N-10):] = [yGBlad[(N-10)] for i in range(10)]
    yGBlad[-10:] = [yGBlad[-11] for i in range(10)]
    yGBHuber[:(N-10)] = yGBHuber[10:]
    yGBHuber[(N-10):] = [yGBHuber[(N-10)] for i in range(10)]
    yGBHuber[-10:] = [yGBHuber[-11] for i in range(10)]
    #yNN[:(N-10)] = yNN[10:]
    #yNN[(N-10):] = [yNN[(N-10)] for i in range(10)]
    #yNN[-10:] = [yNN[-11] for i in range(10)]
    #yNNsgd[:(N-10)] = yNNsgd[10:]
    #yNNsgd[(N-10):] = [yNNsgd[(N-10)] for i in range(10)]
    #yNNsgd[-10:] = [yNNsgd[-11] for i in range(10)]
    plt.plot(range(N),yLS,label = 'LS')
    plt.plot(range(N),yGBls,label = 'GBls')
    plt.plot(range(N),yGBlad,label = 'GBlad')
    plt.plot(range(N),yGBHuber,label = 'GBHuber')
    plt.plot(range(N),yNN,label = 'DeepNBatch')
    #plt.plot(range(N),yNNsgd,label = 'DeepNstoc')
    plt.xlabel("Number of Samples")
    plt.ylabel("Bellman Error")
    plt.title("Wumpus world")

    plt.legend()
    plt.show() 
    '''
main()
