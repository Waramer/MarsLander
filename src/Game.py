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
    
    def step(self, dt):
        if self.goOn :
            for lander in self.landers:
                pass
        self.render()