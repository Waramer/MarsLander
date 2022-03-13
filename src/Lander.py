from math import *

g = -3.711

class Lander :

    def __init__(self):
        self.pose = [0,0,0]
        self.orient_command = 0
        self.spd = [0,0]
        self.power = 0
        self.fuel = 2000
        self.awake = False

    def turn(self,orient):
        if orient < -90 :
            self.orient_command = -90
        elif orient > 90 :
            self.orient_command = 90
        else :
            self.orient_command = floor(orient)
    
    def thrust(self,pow):
        if pow < 1:
            self.power = 0
        elif pow < 2:
            self.power = 1
        elif pow < 3:
            self.power = 2
        elif pow < 4:
            self.power = 3
        else :
            self.power = 4

    def input(self,rotate,power):
        self.turn(rotate)
        self.thrust(power)

    def step(self,dt):
        pass
