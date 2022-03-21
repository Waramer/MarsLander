import numpy as np

class Individual :
    def __init__(self,orient,power,nbActions):
        self.actions = [[orient,power] for i in range(nbActions)]
        self.fitness = -1

class Genetic:

    def __init__(self,nbPop,initOrient,initPower,nbActions):
        self.population = [ Individual(initOrient,initPower,nbActions) for i in range(nbPop)]

    def evaluation(self,i,score):
        self.population[i].fitness = score

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