import matplotlib.pyplot as plt
from Game import Game
from Game import Map
from Lander import Lander
import time

nombrePopulation = 1
initX = 3500
initY = 2800
ax = plt.axes()
plt.xlim(0,7000) 
plt.ylim(0,3000)

map1 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,500,1000,1200,200,200,500,1300]],[[4000,5000],[200,200]])

landers = [Lander(initX,initY) for i in range(nombrePopulation) ]
landersInputs = []
landersTrajectories = [ [[initX],[initY]] for i in range(nombrePopulation) ]

game = Game(map1,landers)

ax.plot(game.map.points[0],game.map.points[1],color='r')
ax.plot(game.map.lz[0],game.map.lz[1],color='r',linewidth=3)
ax.set_facecolor((0.05,0.05,0.05))

game.start()
for i in range(1000):
    game.step(0.1)

    # Events
    if i == 50 :
        for lander in landers :
            lander.input(30,4)
    if i == 250 :
        for lander in landers :
            lander.input(-30,4)
    if i == 450 :
        for lander in landers :
            lander.input(0,4)
    if i == 550 :
        for lander in landers :
            lander.input(-30,4)

    # Add to display list
    for j in range(nombrePopulation) :
        landersTrajectories[j][0].append(landers[j].pose[0])
        landersTrajectories[j][1].append(landers[j].pose[1])

#display
for i in range(nombrePopulation):
    ax.plot(landersTrajectories[i][0],landersTrajectories[i][1],color='r')

game.stop()
plt.show()