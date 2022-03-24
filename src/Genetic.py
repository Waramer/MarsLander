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
            if lander.landed == "LANDED":
                self.population[ind].fitness = 0
            else :
                self.population[ind].fitness = lander.dist + 10*abs(lander.spd[0]) + 10*abs(lander.spd[1]) + 10*abs(lander.pose[2])
        elif popID==ENFANTS:
            if lander.landed == "LANDED":
                self.enfants[ind].fitness = 0
            else :
                self.enfants[ind].fitness = lander.dist + 10*abs(lander.spd[0]) + 10*abs(lander.spd[1]) + 10*abs(lander.pose[2])

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
                    temp = self.enfants[2*ind].actions[t]
                    self.enfants[2*ind].actions[t] = self.enfants[2*ind+1].actions[t]
                    self.enfants[2*ind+1].actions[t] = temp
                print(i,",",doOrNot,":",i1,i2)
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
        self.printEnf()

    def replacement(self):
        newPop = [Individual(0,0,self.nbActions) for i in range(self.nbPop)]
        # Remplacement
        self.population = newPop
        self.printPop()
        
        # # Sélectionner les deux meilleurs des ancetres
        # if self.population[0].fitness <= self.population[1].fitness:
        #     newPop.append(Individual(self.population[0].actions))
        #     newPop.append(Individual(self.population[1].actions))
        # else :
        #     newPop.append(Individual(self.population[1].actions))
        #     newPop.append(Individual(self.population[0].actions))
        # for anc in self.population:
        #     if anc.fitness < newPop[0].fitness and anc.fitness < newPop[1].fitness:
        #         newPop[1] = Individual(newPop[0].actions)
        #         newPop[0] = Individual(anc.actions)
        #     elif anc.fitness < newPop[1].fitness:
        #         newPop[1] = Individual(anc.actions)
        # # Prendre trois autres ancetres au hasard
        # a,b,c = self.rand.randint(0,self.nbPop-1),self.rand.randint(0,self.nbPop-1),self.rand.randint(0,self.nbPop-1)
        # newPop.append(Individual(self.population[a].actions))
        # newPop.append(Individual(self.population[b].actions))
        # newPop.append(Individual(self.population[c].actions))
        # # Sélectionner les deux meilleurs des enfants
        # if self.enfants[0].fitness <= self.enfants[1].fitness :
        #     newPop.append(Individual(self.enfants[0].actions))
        #     newPop.append(Individual(self.enfants[1].actions))
        # else :
        #     newPop.append(Individual(self.enfants[1].actions))
        #     newPop.append(Individual(self.enfants[0].actions))
        # for anc in self.enfants:
        #     if anc.fitness < newPop[0].fitness and anc.fitness < newPop[1].fitness :
        #         newPop[1] = Individual(newPop[0].actions)
        #         newPop[0] = Individual(anc.actions)
        #     elif anc.fitness < newPop[1].fitness :
        #         newPop[1] = Individual(anc.actions)
        # # Prendre trois autres enfants au hasard
        # a,b,c = self.rand.randint(0,self.nbPop-1),self.rand.randint(0,self.nbPop-1),self.rand.randint(0,self.nbPop-1)
        # newPop.append(Individual(self.enfants[a].actions))
        # newPop.append(Individual(self.enfants[b].actions))
        # newPop.append(Individual(self.enfants[c].actions))
        # # Remplacement
        # self.population = newPop
        # self.printPop()
    
    def printPop(self):
        print("POPULATION : ")
        for ind in self.population:
            print(ind.actions,"=",ind.fitness," -> ",ind)

    def printEnf(self):
        print("ENFANTS : ")
        for ind in self.enfants:
            print(ind.actions,"=",ind.fitness," -> ",ind)