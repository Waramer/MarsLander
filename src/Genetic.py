import numpy as np
import math as m
import random

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

    def crossover(self, parent1, parent2):
        parent1 = np.array(parent1)
        parent2 = np.array(parent2)
        rows, columns = parent1.shape

        beta = random.random()   ##coeficient pour le crossover de l'angle
        alpha = random.random()  ##coeficient pour le crossover de la puissance

        child1=[]
        child2=[]

        for i in range(0,rows):

            ##Méthode: moyenne ponderé des parents (poids aleatoires)
            ##enfant numero 1 enf=beta ou alpha*p1 + (1-beta ou alpha)*p2
            child1.append(beta*parent1[i,0] + (1-beta)*parent2[i,0])
            child1.append(alpha*parent1[i,1] + (1-alpha)*parent2[i,1])

            ##enfant numero 2 
            child2.append((1-beta)*parent1[i,0] + beta*parent2[i,0])
            child2.append((1-alpha)*parent1[i,1] + alpha*parent2[i,1])

          ##matrices pour les enfants
        child1=np.array(child1).reshape(rows,columns)
        child2=np.array(child2).reshape(rows,columns)

        return child1, child2

    
    def mutation(self):
        
        mut_rate=0.2
        rows, columns = chrom.shape
        num_mut = m.ceil(mut_rate*rows*columns)  ##calcul du nombre de mutation selon la taux de mutation et la cantité d'individus dispo
                                              #comme ca y a une meilleure exploration de l'espace de recherche

        for i in range (num_mut):

          ##position a changer (choix aleatoire) 
          a=random.randint(0,rows-1)
          b=random.randint(0,columns-1)
          if b==0:    ##si l'info a changer c'est un angle
            chrom[a,b]=random.uniform(-m.pi/2,m.pi/2)
          else:       ##si l'info a changer c'est une puissance
            chrom[a,b]=random.uniform(0,4)

        return chrom

    def replacement(self):
        pass
