import numpy as np
import math as m
import random

ANCETRES = 0
ENFANTS = 1

class Individual :
    def __init__(self,orient,power,nbActions):
        self.actions = [[orient,power] for i in range(nbActions)]
        self.fitness = -1

class Genetic:

    def __init__(self,nbPop,initOrient,nbActions,cross,mut):
        self.nbPop = nbPop
        self.population = [ Individual(initOrient*15*(random.randint(1,6)),random.randint(1,4),nbActions) for i in range(nbPop)]
        self.enfants = []
        self.tauxCross = cross
        self.tauwMut = mut

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
        for i in range(self.nbPop):
            # Tournoi 1v1 à sélection aléatoire
            a1 = random.randint(0,self.nbPop-1)
            a2 = random.randint(0,self.nbPop-1)
            if self.population[a1].fitness >= self.population[a2].fitness:
                self.enfants.append(self.population[a1])
            else :
                self.enfants.append(self.population[a2])

    def crossover(self):
        for ind in range(self.nbPop//2):
            doOrNot = random.random()
            if doOrNot <= self.tauxCross:
                i1 = random.randint(0,self.nbPop-2)
                i2 = random.randint(i1+1,self.nbPop-1)
                for t in range(i1,i2+1):
                    temp = self.enfants[2*ind].actions[t]
                    self.enfants[2*ind].actions[t] = self.enfants[2*ind+1].actions[t]
                    self.enfants[2*ind+1].actions[t] = temp

    def mutation(self):
        for ind in range(self.nbPop):
            doOrNot = random.random()
            if doOrNot <= self.tauwMut:
                i1 = random.randint(0,self.nbPop-2)
                i2 = random.randint(i1+1,self.nbPop-1)
                power = random.randint(-1,1)
                orient = 15*random.randint(-1,1)
                for t in range(i1,i2+1):
                    self.enfants[ind].actions[t][0] += orient
                    self.enfants[ind].actions[t][0] += power

    def replacement(self):
        newPop = []
        # Sélectionner les deux meilleurs des ancetres
        if self.population[0].fitness >= self.population[1].fitness:
            newPop.append(self.population[0])
            newPop.append(self.population[1])
        else :
            newPop.append(self.population[1])
            newPop.append(self.population[0])
        for anc in self.population:
            if anc.fitness > newPop[0].fitness and anc.fitness > newPop[1].fitness:
                newPop[1] = newPop[0]
                newPop[0] = anc
            elif anc.fitness > newPop[1].fitness:
                newPop[1] = anc
        # Prendre trois autres ancetres au hasard
        a,b,c = random.randint(0,self.nbPop-1),random.randint(0,self.nbPop-1),random.randint(0,self.nbPop-1)
        newPop.append(self.population[a])
        newPop.append(self.population[b])
        newPop.append(self.population[c])
        # Sélectionner les deux meilleurs des enfants
        if self.enfants[0].fitness >= self.enfants[1].fitness :
            newPop.append(self.enfants[0])
            newPop.append(self.enfants[1])
        else :
            newPop.append(self.enfants[1])
            newPop.append(self.enfants[0])
        for anc in self.enfants:
            if anc.fitness > newPop[0].fitness and anc.fitness > newPop[1].fitness :
                newPop[1] = newPop[0]
                newPop[0] = anc
            elif anc.fitness > newPop[1].fitness :
                newPop[1] = anc
        # Prendre trois autres enfants au hasard
        a,b,c = random.randint(0,self.nbPop-1),random.randint(0,self.nbPop-1),random.randint(0,self.nbPop-1)
        newPop.append(self.enfants[a])
        newPop.append(self.enfants[b])
        newPop.append(self.enfants[c])
        # Remplacement
        self.population = newPop
        self.enfants = []

    # def crossover(self, parent1, parent2):
    #     parent1 = np.array(parent1)
    #     parent2 = np.array(parent2)
    #     rows, columns = parent1.shape

    #     beta = random.random()   ##coeficient pour le crossover de l'angle
    #     alpha = random.random()  ##coeficient pour le crossover de la puissance

    #     child1=[]
    #     child2=[]

    #     for i in range(0,rows):

    #         ##Méthode: moyenne ponderé des parents (poids aleatoires)
    #         ##enfant numero 1 enf=beta ou alpha*p1 + (1-beta ou alpha)*p2
    #         child1.append(beta*parent1[i,0] + (1-beta)*parent2[i,0])
    #         child1.append(alpha*parent1[i,1] + (1-alpha)*parent2[i,1])

    #         ##enfant numero 2 
    #         child2.append((1-beta)*parent1[i,0] + beta*parent2[i,0])
    #         child2.append((1-alpha)*parent1[i,1] + alpha*parent2[i,1])

    #       ##matrices pour les enfants
    #     child1=np.array(child1).reshape(rows,columns)
    #     child2=np.array(child2).reshape(rows,columns)

    #     return child1, child2
    
    # def mutation(self,chrom):
        
    #     chrom = np.array(chrom)
    #     mut_rate=0.2
    #     rows, columns = chrom.shape
    #     num_mut = m.ceil(mut_rate*rows*columns)  ##calcul du nombre de mutation selon la taux de mutation et la cantité d'individus dispo
    #                                           #comme ca y a une meilleure exploration de l'espace de recherche

    #     for i in range (num_mut):

    #       ##position a changer (choix aleatoire) 
    #       a=random.randint(0,rows-1)
    #       b=random.randint(0,columns-1)
    #       if b==0:    ##si l'info a changer c'est un angle
    #         d = random.randint(-1,1)

    #         while( (chrom[a,b] + (m.pi/12)*d <-m.pi/2) | (chrom[a,b] + (m.pi/12)*d > m.pi/2) ):
    #           d = random.randint(-1,1)

    #         chrom[a,b]= chrom[a,b] + (m.pi/12) * d


    #       else:       ##si l'info a changer c'est une puissance
    #         e = random.randint(-1,1)

    #         while( (chrom[a,b] + e < 0) | (chrom[a,b] + e > 4) ):
    #             e = random.randint(-1,1)

    #         chrom[a,b] = chrom[a,b] + e

    #     return chrom