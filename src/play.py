import matplotlib.pyplot as plt
from Game import Game
from Game import Map
from Genetic import Genetic
from Lander import Lander
import numpy as np

# CONSTANTES
DEBUG = False
ANCETRES = 0
ENFANTS = 1
map1 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,500,1000,1200,200,200,500,1300]],[4,5])
map2 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,750,1200,1800,1000,1000,1200,2000]],[4,5])
map3 = Map([[0,1000,2000,3000,4000,4000,3000,3000,4000,5000,6000,7000],[2000,1500,800,500,500,800,1200,1500,1800,1500,1000,1500]],[3,4])

# ========== FUNCTIONS ==========

def gameRun(popID):
    # GAME INITIALISATION
    landers = [Lander(initX,initY) for i in range(nombrePopulation) ]
    landersTrajectories = [ [[initX],[initY]] for i in range(nombrePopulation) ]
    game = Game(map,landers)

    # # INITIALISATION AFFICHAGE

    # START GAME
    game.start()
    timer = 0
    compteurAction = 0

    # INITIALISATION AFFICHAGE
    ax = plt.axes()
    plt.xlim(0,7000) 
    plt.ylim(0,3000)
    ax.set_facecolor((0.05,0.05,0.05))
    ax.plot(game.map.points[0],game.map.points[1],color='r')
    ax.plot([game.map.points[0][game.map.lz[0]],game.map.points[0][game.map.lz[1]]],[game.map.points[1][game.map.lz[0]],game.map.points[1][game.map.lz[1]]],color='r',linewidth=3)

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

    # GAME END
    game.stop()
    plt.draw()

def gameRunOptimal(actions):
    # GAME INITIALISATION
    landers = [Lander(initX,initY)]
    landersTrajectories = [[[initX],[initY]]]
    game = Game(map,landers)

    # START GAME
    game.start()
    timer = 0
    compteurAction = 0

    # INITIALISATION AFFICHAGE
    ax = plt.axes()
    plt.xlim(0,7000) 
    plt.ylim(0,3000)
    ax.set_facecolor((0.05,0.05,0.05))
    ax.plot(game.map.points[0],game.map.points[1],color='r')
    ax.plot([game.map.points[0][game.map.lz[0]],game.map.points[0][game.map.lz[1]]],[game.map.points[1][game.map.lz[0]],game.map.points[1][game.map.lz[1]]],color='r',linewidth=3)

    # GAME LOOP
    for i in range(tempsSimualtion):
        game.step(1/echantillonnage)

        # Actions des individus appliqués aux landers
        if timer in np.linspace(0,tempsSimualtion,nbActions+1):
            game.landers[0].input(actions[compteurAction][0],actions[compteurAction][1])
            compteurAction += 1
        timer += 1

        # Add to display list
        landersTrajectories[0][0].append(landers[0].pose[0])
        landersTrajectories[0][1].append(landers[0].pose[1])

    # DISPLAY OF THE GAME
    ax.plot(landersTrajectories[0][0],landersTrajectories[0][1],color='g')

    # GAME END
    game.stop()
    plt.draw()

# ============ MAIN =============
if __name__ == '__main__':

    # VARIABLES PROGRAMME A CHOISIR
    nombrePopulation = 20                    # nombre d'individu dans une génération
    map = map3                               # choisir la map
    nbActions = 100                          # nombre d'actions prises par un individu
    tempsSimualtion = 10000                   # Nombre de tics pour la simulation
    echantillonnage = 10                     # Nb de tic du moteur de jeu par secondes de simulation
    initX = 5500                               # position initiale X
    initY = 2500                            # position initiale Y
    tauxCross = 0.3                          # Taux de croisement
    tauxMut = 0.5                           # Taux de mutation

    # PROGRAMME INITIALISATION
    if initX>map.points[0][map.lz[1]] : initOrient = -1
    else : initOrient = 1
    genetic = Genetic(nombrePopulation,initOrient,nbActions,tauxCross,tauxMut)

    # ============ GENETIC RUNS ============

    gameRun(ANCETRES)
    plt.pause(0.01)
    goOn = genetic.stopCriteria()
    generations = 1
    while(goOn==True):

        print("GENERATION",generations)
        genetic.selection()
        genetic.crossover()
        genetic.mutation()
        plt.clf()
        gameRun(ENFANTS)
        plt.pause(0.01)
        genetic.replacement()
        goOn = genetic.stopCriteria()
        generations += 1
    
    # SHOW OPTIMAL
    gameRunOptimal(goOn)
    plt.show()

# ============ FIN MAIN =============