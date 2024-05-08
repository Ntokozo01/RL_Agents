from FourRooms import FourRooms
import numpy as np
import random

NUM_ROWS = 13
NUM_COLS = 13

BARRIER = -1

observed_environment = np.zeros((NUM_COLS, NUM_ROWS))
MOVES = [FourRooms.UP, FourRooms.DOWN, FourRooms.LEFT, FourRooms.RIGHT]

# Initialise the 3D Q-table of size 13 X 13 X 4 to Zeros
# where q_table[y][x] represents the state with 4 moves and q_table[y][x][a] is the Q(s|a)  
q_table = np.zeros((NUM_ROWS, NUM_COLS, len(MOVES)))
 
# Initialise the reward function of same size as Q-table to Null(-1) rewards
rewards = np.full((NUM_ROWS, NUM_COLS, len(MOVES)), -1)

discount_rate = 0.6 # gamma
learning_rate = 0.5 # alpha
exploration_rate = 0.6 # epsilon greedy

# Checks whether the future move will result in a BARRIER, out off-bounds or unmovable state from the observed environment

""" Calculate Q(S,a) for future rewards with great benefits
    currentState - (x, y) tuple
    action - action to take on the given state
    nextState - (x,y) tuple state will transition to when from currentState taking the given action
"""
def q_learn(currentState, action, nextState):
    reward = rewards[currentState][action]
    max_next_q = np.max(q_table[nextState])
    current_q = q_table[currentState][action]
    q_table[currentState][action] = (learning_rate) * current_q + learning_rate * (reward + discount_rate * max_next_q)


# Predicts the next action
def nextAction(currentState, exploration_rate):
    if random.uniform(0,1) < exploration_rate:
        return  random.randint(0, 3)
    else:
        return  np.argmax(q_table[currentState])
        
    
    return MOVES[a]
    

def checkValid(enviro, move, x, y):
    if (move % 4) == 0:  # UP
        y -= 1
    elif (move % 4) == 1:  # DOWN
        y += 1
    elif (move % 4) == 2:  # LEFT
        x -= 1
    elif (move % 4) == 3:  # RIGHT
        x += 1

    if enviro[y][x] != BARRIER:
        return x, y, True

    return x, y, False

def findPackage(i, fourRoomsObj, packagesToCollect):
    (prevPosX, prevPosY) = fourRoomsObj.getPosition() # Get initial State of the Agent in the environment
    
    for j in range(MAX_ITERATIONS):
        action = nextAction((prevPosX, prevPosY), exploration_rate)
        
        gridType, (nextPosX, nextPosY), packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
        
        if (prevPosX == nextPosX) and (prevPosY == nextPosY):
            observed_environment[prevPosY][prevPosX] = BARRIER
            rewards[(nextPosX, nextPosY)][action] += BARRIER
             
        else:
           rewards[(nextPosX, nextPosY)][action] = 0
    
        #print("Agent took {0} action and moved to {1}".format (action, (nextPosX, nextPosY)))
        
        if (packagesToCollect > packagesRemaining):
            packagesToCollect -= 1
            
            q_table[(nextPosX, nextPosY)] = [100, 100, 100, 100]
            print("Package collected")
            #print("Is terminal:", isTerminal)
            
        
        q_learn((prevPosX, prevPosY), action, (nextPosX, nextPosY)) 
        
        
        if packagesRemaining == 0:
            fourRoomsObj.showPath(-1, "image_{0}.png".format(i))
            return j+1
    
        
        prevPosX = nextPosX
        prevPosY = nextPosY
    return MAX_ITERATIONS

fourRoomsObj = FourRooms("simple")

NUM_EPOCHS = 15
MAX_ITERATIONS = 100000

k = fourRoomsObj.getPackagesRemaining()
print("Packages to collect:", k)

(startX, startY) = fourRoomsObj.getPosition() 
print("Agent starts at: {0}".format((startX, startY)))

for i in range(NUM_EPOCHS):
    fourRoomsObj.newEpoch()
    
    #print("Epsilon:", exploration_rate)
    
    total_actions = findPackage(i, fourRoomsObj, k)
    """try:
        total_actions = findPackage(i, fourRoomsObj, k)
    except:
        print("An Exception occured!")"""
    
    print("Total actions taken:", total_actions)
    exploration_rate = exploration_rate * 0.8
    
    
#print(q_table)     

fourRoomsObj.showPath(-1)