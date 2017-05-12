from random import randrange,gauss
from math import sqrt,pi,exp
class world(object):

    def __init__(self):
        self.grid = [["corridor" for i in range(3)] for j in range(3)]
        self.color = [["red","red","green"],
                      ["white","white","white"],
                      ["red","red","green"]]
        for i in range(3):
            for j in range(3):
                if i == 0 or i == 2:
                    self.grid[i][j] ="room"
        cPos = randrange(3)
        self.grid[1][cPos] += "(robot)"
        self.xy = [1,cPos]
        self.beta = 0.0

    def boundXY(self):
        if self.xy[0] < 0:
            self.xy[0] = 0
        if self.xy[0] > 2:
            self.xy[0] = 2
        if self.xy[1] < 0:
            self.xy[1] = 0
        if self.xy[1] > 2:
            self.xy[1] = 2

    def noise(self,x):
        return gauss(x,0.1)

    def gaussProb(self,mu,sigma,x):
        nC = 1/float(sqrt(2*pi*sigma))
        pstar = exp(-1*(((x-mu)**2)/float(2*sigma)))
        return pstar/float(nC)

    def getObsProb(self,obs,act):
        p = 1
        for item in [[0,0],[2,0],[0,2],[2,2]]:
            ssuma = 0
            ssumo = 0
            for i in range(2):
                ssuma += (act[i]-item[i])**2
                ssumo += (obs[i]-item[i])**2
            da = sqrt(ssuma)
            do = sqrt(ssumo)
            p *= self.gaussProb(da,0.01,do)
        return p
        
    def __repr__(self):
        for i in range(3)[::-1]:
            walls = ""
            for j in range(3):
                walls += "                         |"
            print walls[:-1]
            for j in range(3):
                if self.color[i][j]!="white":
                    print " "*10+self.color[i][j]+" "*8,
                else:
                    print " "*8+self.grid[i][j]+" "*8,
            print "\n"
            print walls[:-1]
            print "\n"+"-"*100
        return ""
