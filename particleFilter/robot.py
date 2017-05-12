from math import cos,sin,pi,sqrt
class robot():

    def __init__(self):
        return
    
    def move(self,world,theta,d):
        world.beta += theta
        x = int(world.xy[0])
        y = int(world.xy[1])
        if not (theta==0 and d==0):
            world.grid[x][y] = world.grid[x][y][:-7]
            radians = (world.beta*pi)/float(180)
            world.xy[1] += d*cos(radians)
            world.xy[0] += d*sin(radians)
            world.boundXY()
            if world.color[int(world.xy[0])][int(world.xy[1])] == "white":
               world.grid[int(world.xy[0])][int(world.xy[1])] += "(robot)"
            else:
                world.color[int(world.xy[0])][int(world.xy[1])] += "(robot)"
        print "\nmoved: "+str(d)+" units at an angle of "+str(theta)+" degrees\n"

    def sense(self,world):
        obs = []
        pos = world.xy
        for item in [[0,0],[2,0],[0,2],[2,2]]:
            ssum = 0
            for i in range(2):
                ssum += (item[i]-pos[i])**2
            obs.append(sqrt(ssum))
        return obs

    def getObs(self,world,pos):
        obs = []
        for item in [[0,0],[2,0],[0,2],[2,2]]:
            ssum = 0
            for i in range(2):
                ssum += (item[i]-pos[i])**2
            obs.append(sqrt(ssum))
        return obs
