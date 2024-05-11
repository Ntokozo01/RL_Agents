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

discount_rate = 0.9 # gamma
learning_rate = 0.6 # alpha
exploration_rate = 1 # epsilon greedy

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
    q_table[currentState][action] = (1 - learning_rate) * current_q + learning_rate * (reward + discount_rate * max_next_q)


# Predicts the next action
def nextAction(currentState, exploration_rate):
    a = 0
    if random.uniform(0,1) < exploration_rate:
        a = random.randint(0, 3)
    else:
        a = np.argmax(q_table[currentState])
        
    return MOVES[a]   

def findPackage(fourRoomsObj, packagesToCollect, exploration_rate):
    state = fourRoomsObj.getPosition()
    print("Agent starts at: {0}".format(state))

    for j in range(MAX_ITERATIONS):
        action = nextAction(state, exploration_rate)
        
        gridType, nextState, packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
        print("Agent took {0} action and moved to {1}".format (action, nextState))
        
        if (packagesToCollect > packagesRemaining):
            print("Package collected at {0}".format(nextState))
            packagesToCollect -= 1
        
        if packagesRemaining == 0:
            fourRoomsObj.showPath(-1, "image_N1.png")
            return j+1
        
        state = nextState
        
    return MAX_ITERATIONS

def train(i, fourRoomsObj, packagesToCollect):
    state = fourRoomsObj.getPosition() # Get initial State of the Agent in the environment
    
    for j in range(MAX_ITERATIONS):
        action = nextAction(state, exploration_rate)
        
        gridType, nextState, packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
        
        if state != nextState:
           rewards[state][action] = 0

        #if i == NUM_EPOCHS -1:
        #    print("Agent took {0} action and moved to {1}".format (action, nextState))
        
        if (packagesToCollect > packagesRemaining):
            packagesToCollect -= 1
            
            rewards[state][action] = 100
            #print("Package collected at {0}".format(nextState))            
        
        q_learn(state, action, nextState) 
        
        if packagesRemaining == 0:
            #fourRoomsObj.showPath(-1, "image_{0}.png".format(i))
            return j+1
    
        state = nextState
        
    return MAX_ITERATIONS

fourRoomsObj = FourRooms("simple")

NUM_EPOCHS = 100
MAX_ITERATIONS = 2500

k = fourRoomsObj.getPackagesRemaining()
print("Packages to collect:", k)

(startX, startY) = fourRoomsObj.getPosition() 
print("Agent starts at: {0}".format((startX, startY)))

for i in range(NUM_EPOCHS):
    fourRoomsObj.newEpoch()
    print('Epoch {0}/{1}'.format(i+1, NUM_EPOCHS))
    
    #print("Epsilon greedy is {0}".format(exploration_rate))
    
    total_actions = train(i, fourRoomsObj, k)
    
    #print("Total actions taken:", total_actions)
    
    exploration_rate = max(0.01, exploration_rate * 0.99)
    
exploration_rate = 0

print("Q function")
for y in range(NUM_ROWS):
    for x in range(NUM_COLS):
        state = (x, y)
        #print("Q-values at {0} is for actions: {1}".format((x,y), q_table[(x,y)]))
        print("{:>3}".format(round(max(q_table[state]))), end=" ")
    print("")
#print(q_table) 

# print("Rewards function")
# # The reward function provides the representation of the observed environment
# for y in range(NUM_ROWS):
#     for x in range(NUM_COLS):
#         state = (x, y)
#         # print("Reward value at {0} is {1}".format((x,y), max(rewards[(x,y)])))
#         print("{:>3}".format(max(rewards[state])), end=" ")
#     print("")
# #print(rewards) 

# Display the last training agent path
fourRoomsObj.showPath(-1, "image_N.png")

# Display the agent's path to collect the package using 100% explotation
fourRoomsObj.newEpoch()
#findPackage(fourRoomsObj, k, 0)
train(0, fourRoomsObj, k)
fourRoomsObj.showPath(-1, "image_N1.png")