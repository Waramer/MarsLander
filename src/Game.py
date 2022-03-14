import numpy as np

### MAPS
class Map :
    def __init__(self,points,lz):
        self.points = points
        self.lz = lz

### GAME
class Game :

    def __init__(self,map,landers):
        self.landers = landers
        self.map = map
        self.goOn = False

    def start(self):
        self.goOn = True
    
    def stop(self):
        self.goOn = False
        for lander in self.landers:
            lander.pause()
    
    def collisionCheck(self, pose):
        for i in range(0,len(self.map.points[0])-1):
            if pose[0]>self.map.points[0][i] and pose[0]<self.map.points[0][i+1]:
                a = np.array([self.map.points[0][i],self.map.points[1][i]])
                p = np.array([pose[0],pose[1]])
                b = np.array([self.map.points[0][i+1],self.map.points[1][i+1]])
                print(str(a)+" "+str(p)+" "+str(b))
                if np.cross(p-a,b-a)>0:
                    return True
        return False

    def step(self, dt):
        if self.goOn :
            for lander in self.landers:
                if lander.awake:
                    lander.step(dt)
                    coll = self.collisionCheck(lander.pose)
                    if coll :
                        print("Collision")
                        lander.pause()