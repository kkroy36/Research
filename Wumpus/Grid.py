from random import random
class Grid(object):
    '''represents the 2D wumpus world'''
   
    def __init__(self,N,W):
        '''class constructor take dimensions
           and initializes NxN grid with W wumpus'
        '''
        self.size = N
        self.grid = [[0 for i in range(N)] for j in range(N)]
        self.goal_x,self.goal_y = 1,N-1 #int(random()*self.size),int(random()*self.size)
        self.obsMap = [[[] for i in range(N)] for j in range(N)]
        self.actions = ["left","right","top","down"]
        self.factoredState = {}
        '''
        for i in range(W):
            x_pos,y_pos = int(random()*self.size),int(random()*self.size)
            while x_pos!=self.goal_x and y_pos!=self.goal_y:
                x_pos,y_pos = int(random()*self.size),int(random()*self.size)
            self.grid[x_pos][y_pos] = 1
        '''
        self.grid[1][1] = 1
        self.getObs()
    
    def reward(self,x,y):
        '''returns the immediate reward of a state'''
        if self.grid[x][y] == 1:
            return -50
        elif x == self.goal_x and y == self.goal_y:
            return 100
        else:
            return -1

    def states(self,factored=False):
        '''returns all the grid states
           factored or just like that
           as desired
        '''
        allStates = []
        for x in range(self.size):
            for y in range(self.size):
                if factored:
                    allStates += [self.factored(x,y)]
                else:
                    allStates += [(x,y)]
        return allStates

    def takeAction(self,x,y,action):
        '''takes an action and returns new state'''
        ts = None
        if action in self.actions:
            if action == "left":
                if self.valid(x-1,y):
                    ts = (x-1,y)
                else:
                    ts = (x,y)
            elif action == "right":
                if self.valid(x+1,y):
                    ts = (x+1,y)
                else:
                    ts = (x,y)
            elif action == "top":
                if self.valid(x,y+1):
                    ts = (x,y+1)
                else:
                    ts = (x,y)                 
            elif action == "down":
                if self.valid(x,y-1):
                    ts = (x,y-1)
                else:
                    ts = (x,y)
        else:
            ts = (x,y)
        return ts
         
    def valid(self,x,y):
        '''checks if (x,y) is a valid
           position in the grid
        '''
        if x < 0 or x == self.size or y < 0 or y == self.size:
            return False
        return True

    def getObs(self):
        '''generates observations of stench
           and breeze, based on wumpus pos
        '''
        valid = self.valid
        for x in range(self.size):
            for y in range(self.size):
                if valid(x+1,y) and self.grid[x+1][y] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x-1,y) and self.grid[x-1][y] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x,y+1) and self.grid[x][y+1] == 1:
                    self.obsMap[x][y].append("stench")
                if valid(x,y-1) and self.grid[x][y-1] == 1:
                    self.obsMap[x][y].append("stench")
                if self.grid[x][y]!=1:
                    self.obsMap[x][y].append("breeze")

    def factored(self,x,y):
        '''returns a factored state of
           x,y,I(stench),I(breeze)
        '''
        if not self.valid(x,y):
            print "In valid grid cell"
            exit()
        state = [x]+[y]
        state += [1 if "stench" in self.obsMap[x][y] else 0]
        state += [1 if "breeze" in self.obsMap[x][y] else 0]
        self.factoredState[(x,y)] = state       
        return state

    def unfactored(self,factoredState):
        '''returns the compressed state
           from the factored state
        '''
        for key in self.factoredState:
            if self.factoredState[key] == [item for item in factoredState]:
                return key
        return False

    def __repr__(self):
        '''defines the representation of the grid
           that will be output on call to print
        '''
        string = "Wumpus map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.grid[i][j])+", " if j!=self.size-1 else str(self.grid[i][j])+"\n"][0]
        string += "\nObservation map: \n"
        for i in range(self.size):
            for j in range(self.size):
                string += [str(self.obsMap[i][j])+", " if j!=self.size-1 else str(self.obsMap[i][j])+"\n"][0]
        return string+"\nGoal Position: ("+str(self.goal_x)+","+str(self.goal_y)+")"+"\n"
