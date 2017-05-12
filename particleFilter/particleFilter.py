from random import random
from math import exp
class particleFilter(object):

    def __init__(self,world,robot):
        self.world = world
        self.robot = robot

    def initParticles(self,N):
        x = [random()*2 for i in range(N)]
        y = [random()*2 for i in range(N)]
        p = zip(x,y)
        return p

    def weights(self,p):
        weights = []
        r = self.robot
        w = self.world
        for particle in p:
            obs = r.getObs(w,particle)
            obsProb = w.getObsProb(obs,r.sense(w))
            weights.append(obsProb)
        return weights

    def resample(self,weights,p):
        wSum = sum(weights)
        a = sorted([item/float(wSum) for item in weights])
        n = len(p)
        pnew = []
        for k in range(n):
            rn = random()
            lb = 0
            for i in range(n):
                j = i+1
                ub = sum(a[:j])
                if lb <= rn < ub:
                    pnew.append(p[i])
                    break
                lb = ub
        return pnew

    def localize(self,p,N):
        for i in range(N):
            weights = self.weights(p)
            p = self.resample(weights,p)
        return p
