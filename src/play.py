from turtle import color
import matplotlib.pyplot as plt
from Game import Game
from Game import Map
# generate axes object
ax = plt.axes()

# set limits
plt.xlim(0,7000) 
plt.ylim(0,3000)

map1 = Map([[0,1000,2000,3000,4000,5000,6000,7000],[1500,500,1000,1200,200,200,500,1300]],[4,5])

game = Game(map1,[])

ax.plot(game.map.points[0],game.map.points[1],color='r')

for i in range(10):        
    #  add something to axes    
     ax.scatter([70*i], [30*i]) 
     ax.plot([70*i], [30*i+1], 'rx')

     # draw the plot
     plt.draw() 
     plt.pause(0.1) #is necessary for the plot to update for some reason

plt.show()