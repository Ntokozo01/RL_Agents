from FourRooms import FourRooms
import numpy as np
import random

NUM_ROWS = 13
NUM_COLS = 13

observed_environment = np.zeros((NUM_COLS, NUM_ROWS))

MOVES = [FourRooms.UP, FourRooms.DOWN, FourRooms.LEFT, FourRooms.RIGHT]

def findPackage(i, fourRoomsObj):
    for j in range(num_iterations):
        action = MOVES[random.randint(0, 3)]
        
        
        gridType, (nextPosX, nextPosY), packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
    
        print("Agent took {0} action and moved to {1}".format (action, (nextPosX, nextPosY)))
        
        if packagesRemaining == 0:
            print("Package collected")
            fourRoomsObj.showPath(-1, "image_{0}.png".format(i))
            return j
    
        if isTerminal:
            print("Reached Terminal")
            fourRoomsObj.showPath(-1, "image_{0}.png".format(i))
            return j

fourRoomsObj = FourRooms("simple")

NUM_EPOCHS = 10

k = fourRoomsObj.getPackagesRemaining()
print("Packages to collect:", k)

(startX, startY) = fourRoomsObj.getPosition() 
print("Agent starts at: {0}".format((startX, startY)))

for i in range(NUM_EPOCHS):
    fourRoomsObj.newEpoch()
    
    num_iterations = 1000
    total_actions = findPackage(i, fourRoomsObj)
    
    print("Total actions taken:", total_actions)
    
    
     

fourRoomsObj.showPath(-1)