import math as m
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
    
    def collisionCheck(self, lander):
        for i in range(0,len(self.map.points[0])-1):
            if lander.pose[0]>self.map.points[0][i] and lander.pose[0]<self.map.points[0][i+1]:
                a = np.array([self.map.points[0][i],self.map.points[1][i]])
                p = np.array([lander.pose[0],lander.pose[1]])
                b = np.array([self.map.points[0][i+1],self.map.points[1][i+1]])
                if np.cross(p-a,b-a)>0:
                    return (True,[i,i+1])
        return (False,[])

    def landingCheck(self,lander):
        if lander.pose[0]>=self.map.points[0][self.map.lz[0]] and lander.pose[0]<=self.map.points[0][self.map.lz[1]] :
            if lander.pose[1]<=self.map.points[1][self.map.lz[0]] or lander.pose[1]>=self.map.points[1][self.map.lz[1]]:
                if abs(lander.spd[0])<=20 and abs(lander.spd[1])<=40 :
                    if abs(lander.pose[2])<0.01 :
                        lander.landed = "LANDED"
                        return True
        lander.landed = "CRASHED"
        return False

    def computeDist(self,lander,segment):
        if lander.landed == "LANDED":
            lander.distance(0)
        else :
            dist = 0
            if segment[1]<=self.map.lz[0]:
                dist = m.dist([lander.pose[0],lander.pose[1]],[self.map.points[0][segment[1]],self.map.points[1][segment[1]]])
                for i in range(segment[1],self.map.lz[0]):
                    dist += m.dist([self.map.points[0][i],self.map.points[1][i]],[self.map.points[0][i+1],self.map.points[1][i+1]])

            elif self.map.lz[1]<=segment[0]:
                dist = m.dist([lander.pose[0],lander.pose[1]],[self.map.points[0][segment[0]],self.map.points[1][segment[0]]])
                for i in range(self.map.lz[1],segment[0]):
                    dist += m.dist([self.map.points[0][i],self.map.points[1][i]],[self.map.points[0][i+1],self.map.points[1][i+1]])

            lander.distance(dist)

    def step(self, dt):
        if self.goOn :
            for lander in self.landers:
                if lander.awake:
                    lander.step(dt)
                    coll = self.collisionCheck(lander)
                    if coll[0] :
                        self.landingCheck(lander)
                        self.computeDist(lander,coll[1])
                        lander.pause()
                    if lander.pose[0]<0 or lander.pose[0]>7000:
                        lander.landed="OUT"
                        lander.pause()