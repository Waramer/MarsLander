import math as m

g = 3.711

class Lander :

    def __init__(self,x,y):
        self.pose = [x,y,0]
        self.orient_command = 0
        self.spd = [0,0]
        self.power = 0
        self.fuel = 2000
        self.awake = True
    
    def pause(self):
        self.awake = False
    
    def resume(self):
        self.awake = True

    def turn(self,orient):
        command = orient * m.pi / 180
        if command < -m.pi/2 :
            self.orient_command = -m.pi/2
        elif command > m.pi/2 :
            self.orient_command = m.pi/2
        else :
            self.orient_command = command
    
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
        if (abs(self.orient_command-self.pose[2])>0.01):
            if self.orient_command > self.pose[2] :
                self.pose[2] += min([0.5*dt,abs(self.orient_command-self.pose[2])*dt])
            else :
                self.pose[2] -= min([0.5*dt,abs(self.orient_command-self.pose[2])*dt])
        
        if (self.fuel>0):
            self.spd[0] += (self.power*m.sin(self.pose[2]))*dt
            self.spd[1] += (self.power*m.cos(self.pose[2]))*dt
            self.fuel -= self.power*dt
        self.spd[1] -= g*dt
        self.pose[0] += self.spd[0]*dt
        self.pose[1] += self.spd[1]*dt