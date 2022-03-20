import numpy as np

class Individual :
    def __init__(self,orient,power):
        self.orient = orient
        self.power = power

class Genetic:

    def __init__(self,nbPop,initOrient,initPower):
        self.population = [ Individual(initOrient,initPower) for i in range(nbPop)]

    def evaluation(self):
        pass

    def stopCriteria(self):
        pass
    
    def selection(self):
        pass

    def crossover(self):
        pass

    def mutation(self):
        pass

    def replacement(self):
        pass