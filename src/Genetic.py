import numpy as np
import math as m
import random
import copy

ANCETRES = 0
ENFANTS = 1

class Individual :
    def __init__(self,orient,power,nbActions):
        self.nbActions = nbActions
        self.actions = [[orient,power] for i in range(nbActions)]
        self.fitness = -1

class Genetic:

    def __init__(self,nbPop,initOrient,nbActions,cross,mut):
        self.nbActions = nbActions
        self.nbPop = nbPop
        self.enfants = []
        self.tauxCross = cross
        self.tauwMut = mut
        self.rand = random.Random()
        self.population = [ Individual(initOrient*15*(self.rand.randint(1,6)),self.rand.randint(1,4),nbActions) for i in range(nbPop)]

    def evaluation(self,popID,ind,lander):
        if popID==ANCETRES:
            if lander.landed == "LANDED" :
                self.population[ind].fitness = 0
            elif lander.landed == "CRASHED" :
                self.population[ind].fitness = lander.dist + 10*abs(lander.spd[0]) + 10*abs(lander.spd[1]) + 10*abs(lander.pose[2])
            else :
                self.population[ind].fitness = 100000
        elif popID==ENFANTS:
            if lander.landed == "LANDED" :
                self.enfants[ind].fitness = 0
            elif lander.landed == "CRASHED" :
                self.enfants[ind].fitness = lander.dist + 10*abs(lander.spd[0]) + 10*abs(lander.spd[1]) + 10*abs(lander.pose[2])
            else :
                self.enfants[ind].fitness = 100000

    def stopCriteria(self):
        for ind in self.population:
            if ind.fitness == 0 :
                return ind.actions
        return True
    
    def selection(self):
        self.enfants = [Individual(0,0,self.nbActions) for i in range(self.nbPop)]
        for i in range(self.nbPop):
            # Tournoi 1v1 à sélection aléatoire
            a1 = self.rand.randint(0,self.nbPop-1)
            a2 = self.rand.randint(0,self.nbPop-1)
            if self.population[a1].fitness <= self.population[a2].fitness:
                self.enfants[i].actions = copy.deepcopy(self.population[a1].actions)
            else :
                self.enfants[i].actions = copy.deepcopy(self.population[a2].actions)
        self.printEnf()

    def crossover(self):
        i = 0
        for ind in range(self.nbPop//2):
            doOrNot = self.rand.random()
            if doOrNot <= self.tauxCross:
                i1 = self.rand.randint(0,self.nbPop-2)
                i2 = self.rand.randint(i1+1,self.nbPop-1)
                for t in range(i1,i2+1):
                    temp = copy.copy(self.enfants[2*ind].actions[t])
                    self.enfants[2*ind].actions[t] = copy.copy(self.enfants[2*ind+1].actions[t])
                    self.enfants[2*ind+1].actions[t] = copy.copy(temp)
                print(2*i,"-",2*i+1,",",doOrNot,":",i1,i2)
            i+=1
        self.printEnf()

    def mutation(self):
        i = 0
        for ind in range(self.nbPop):
            doOrNot = self.rand.random()
            if doOrNot <= self.tauwMut:
                i1 = self.rand.randint(0,self.nbPop-2)
                i2 = self.rand.randint(i1+1,self.nbPop-1)
                power = self.rand.choice([-1,1])
                orient = 15*self.rand.choice([-1,1])
                for t in range(i1,i2+1):
                    self.enfants[ind].actions[t][0] += orient
                    if self.enfants[ind].actions[t][0] > 90 : self.enfants[ind].actions[t][0] = 90
                    elif self.enfants[ind].actions[t][0] < -90 : self.enfants[ind].actions[t][0] = -90
                    self.enfants[ind].actions[t][1] += power
                    if self.enfants[ind].actions[t][1] > 4 : self.enfants[ind].actions[t][1] = 4
                    elif self.enfants[ind].actions[t][1] < 0 : self.enfants[ind].actions[t][1] = 0
                print(i,",",doOrNot,":",i1,i2,power,orient)
            i+=1
        self.correctPop()
        self.printEnf()
    
    def correctPop(self):
        for enf in self.enfants:
            for i in range(1,self.nbActions):
                if enf.actions[i][0] > enf.actions[i-1][0] + 15:
                    enf.actions[i][0] = enf.actions[i-1][0] + 15
                elif enf.actions[i][0] < enf.actions[i-1][0] - 15:
                    enf.actions[i][0] = enf.actions[i-1][0] - 15
                if enf.actions[i][1] > enf.actions[i-1][1] + 1:
                    enf.actions[i][1] = enf.actions[i-1][1] + 1
                elif enf.actions[i][1] < enf.actions[i-1][1] - 1:
                    enf.actions[i][1] = enf.actions[i-1][1] - 1


    def replacement(self):
        newPop = [Individual(0,0,self.nbActions) for i in range(self.nbPop)]
        # Sélectionner le meilleur ancêtre
        bestOfPop = 0
        for i in range(self.nbPop):
            if self.population[i].fitness < self.population[bestOfPop].fitness:
                bestOfPop = i
        newPop[0].actions = copy.deepcopy(self.population[bestOfPop].actions)
        newPop[0].fitness = copy.copy(self.population[bestOfPop].fitness)
        # Sélectionner le meilleur ancêtre
        bestOfEnf = 0
        for i in range(self.nbPop):
            if self.enfants[i].fitness < self.enfants[bestOfEnf].fitness:
                bestOfEnf = i
        newPop[1].actions = copy.deepcopy(self.enfants[bestOfEnf].actions)
        newPop[1].fitness = copy.copy(self.enfants[bestOfEnf].fitness)
        # Compléter avec des individus aléatoires des deux précédents groupes
        for i in range(2,self.nbPop):
            quellePop = self.rand.random()
            if quellePop<0.5:
                quelIndiv = self.rand.randint(0,self.nbPop-1)
                newPop[i].actions = copy.deepcopy(self.population[quelIndiv].actions)
                newPop[i].fitness = copy.copy(self.population[quelIndiv].fitness)
            else:
                quelIndiv = self.rand.randint(0,self.nbPop-1)
                newPop[i].actions = copy.deepcopy(self.enfants[quelIndiv].actions)
                newPop[i].fitness = copy.copy(self.enfants[quelIndiv].fitness)
        # Remplacement
        self.population = newPop
        self.printPop()
        
    def printPop(self):
        print("POPULATION : ")
        for ind in self.population:
            print(ind.actions,"=",ind.fitness)

    def printEnf(self):
        print("ENFANTS : ")
        for ind in self.enfants:
            print(ind.actions,"=",ind.fitness)