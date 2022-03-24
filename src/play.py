import matplotlib.pyplot as plt
from Game import Game
from Game import Map
from Genetic import Genetic
from Lander import Lander
import numpy as np
import time

# CONSTANTES
DEBUG = False
ANCETRES = 0
ENFANTS = 1
map1 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,500,1000,1200,200,200,500,1300]],[4,5])

# ========== FUNCTIONS ==========

def gameRun(popID):
    # GAME INITIALISATION
    landers = [Lander(initX,initY) for i in range(nombrePopulation) ]
    landersTrajectories = [ [[initX],[initY]] for i in range(nombrePopulation) ]
    game = Game(map,landers)

    # INITIALISATION AFFICHAGE
    ax = plt.axes()
    plt.xlim(0,7000) 
    plt.ylim(0,3000)
    ax.plot(game.map.points[0],game.map.points[1],color='r')
    ax.plot([game.map.points[0][game.map.lz[0]],game.map.points[0][game.map.lz[1]]],[game.map.points[1][game.map.lz[0]],game.map.points[1][game.map.lz[1]]],color='r',linewidth=3)
    ax.set_facecolor((0.05,0.05,0.05))

    # START GAME
    game.start()
    timer = 0
    compteurAction = 0
    # GAME LOOP
    for i in range(tempsSimualtion):
        game.step(1/echantillonnage)

        # Actions des individus appliqués aux landers
        if timer in np.linspace(0,tempsSimualtion,nbActions+1):
            for lnd in range(nombrePopulation):
                # Population parents
                if popID==ANCETRES : game.landers[lnd].input(genetic.population[lnd].actions[compteurAction][0],genetic.population[lnd].actions[compteurAction][1])
                # Population enfants
                elif popID==ENFANTS : game.landers[lnd].input(genetic.enfants[lnd].actions[compteurAction][0],genetic.enfants[lnd].actions[compteurAction][1])
            compteurAction += 1
        timer += 1

        # Add to display list
        for j in range(nombrePopulation) :
            landersTrajectories[j][0].append(landers[j].pose[0])
            landersTrajectories[j][1].append(landers[j].pose[1])
    for ind in range(nombrePopulation):
        genetic.evaluation(popID,ind,game.landers[ind])

    # DISPLAY OF THE GAME
    for i in range(nombrePopulation):
        ax.plot(landersTrajectories[i][0],landersTrajectories[i][1],color='r')
    if DEBUG :
        for i in range(nombrePopulation) :
            print(game.landers[i].landed," : [",game.landers[i].pose[0],";",game.landers[i].pose[1],"] : ",genetic.population[i].fitness)

    # GAME END
    game.stop()
    plt.draw()

# ============ MAIN =============
if __name__ == '__main__':

    # VARIABLES PROGRAMME A CHOISIR
    nombrePopulation = 10                    # nombre d'individu dans une génération
    map = map1                               # choisir la map
    nbActions = 10                          # nombre d'actions prises par un individu
    tempsSimualtion = 2000                   # temps maximum de la simulation (s)
    echantillonnage = 10                     # Nb de tic du moteur de jeu par secondes de simulation
    initX = 3500                             # position initiale X
    initY = 2800                             # position initiale Y
    tauxCross = 0.2                          # Taux de croisement
    tauxMut = 0.3                         # Taux de mutation

    # PROGRAMME INITIALISATION
    if initX>map.points[0][map.lz[1]] : initOrient = -1
    else : initOrient = 1
    genetic = Genetic(nombrePopulation,initOrient,nbActions,tauxCross,tauxMut)

    # ============ GENETIC RUNS ============

    # Evaluation post initialisation
    gameRun(ANCETRES)
    plt.pause(1.0)
    # Condition entrée en cycle
    goOn = genetic.stopCriteria()
    generations = 1
    print("INITIALISATION TERMINEE")
    genetic.printPop()
    while(goOn==True):

        print("GENERATION",generations)
        # SELECTION
        genetic.selection()
        print("SELECTION",generations,"TERMINEE")
        # CROISEMENT
        # genetic.crossover()
        # print("CROISEMENT",generations,"TERMINEE")
        # MUTATION
        genetic.mutation()
        print("MUTATION",generations,"TERMINEE")
        # EVALUATION ENFANTS
        gameRun(ENFANTS)
        genetic.printEnf
        print("EVALUATION",generations,"TERMINEE")
        plt.pause(1.0)
        # REMPLACEMENT
        genetic.replacement()
        print("REMPLACEMENT",generations,"TERMINEE")
        # CRITERE ARRET
        goOn = genetic.stopCriteria()
        generations += 1
        
        pass
    
    # SHOW OPTIMAL

    plt.show()

# ============ FIN MAIN =============