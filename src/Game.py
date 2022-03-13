import numpy as np
import matplotlib.pyplot as plt

class Map :
    def __init__(self,points,lz):
        self.points = points
        self.lz = lz

map1 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,500,1000,1200,200,200,500,1300]],[4,5])
fig = plt.figure()


class Game :

    def __init__(self,map,landers):
        self.landers = landers
        self.map = map
        self.goOn = False

    def start(self):
        self.goOn = True
    
    def stop(self):
        self.goOn = False
    
    def step(self, dt):
        if self.goOn :
            for lander in self.landers:
                pass
        self.render()
    
    def render(self):
        