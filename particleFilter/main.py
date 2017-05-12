from world import world
from robot import robot
from particleFilter import particleFilter
        
def main():

    w = world()
    r = robot()
    moves = [[45,2],[-45,-1]]
    for i in range(2):
        r.move(w,moves[i][0],moves[i][1])
        pf = particleFilter(w,r)
        p = pf.initParticles(10)
        p = pf.localize(p,10)
main()
