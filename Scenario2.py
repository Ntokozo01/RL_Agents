from FourRooms import FourRooms
import numpy as np
import random

import sys

NUM_ROWS = 13
NUM_COLS = 13

BARRIER = -1

observed_environment = np.zeros((NUM_COLS, NUM_ROWS))
MOVES = [FourRooms.UP, FourRooms.DOWN, FourRooms.LEFT, FourRooms.RIGHT]

gTypes = ['EMPTY', 'RED', 'GREEN', 'BLUE']

# Initialise the 3D Q-table of size 13 X 13 X 4 to Zeros
# where q_table[y][x] represents the state with 4 moves and q_table[y][x][a] is the Q(s|a)  
q_table = np.zeros((NUM_ROWS, NUM_COLS, len(MOVES)))
 
# Initialise the reward function of same size as Q-table to Null(-1) rewards
rewards = np.full((NUM_ROWS, NUM_COLS, len(MOVES)), -1)

discount_rate = 0.5 # gamma
learning_rate = 0.4 # alpha
exploration_rate = 1 # epsilon greedy
min_exploration = 0.01
exploitation = 0


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

def train(i, fourRoomsObj, packagesToCollect):
    global cummulative_reward
    state = fourRoomsObj.getPosition() # Get initial State of the Agent in the environment
    
    for j in range(MAX_ITERATIONS):
        action = nextAction(state, exploration_rate)
        
        gridType, nextState, packagesRemaining, isTerminal = fourRoomsObj.takeAction(action)
        
        reward = rewards[state][action]  
        if state != nextState:
            reward -= 1
            #rewards[state][action] = max(0, reward)
            
            if (packagesToCollect > packagesRemaining):
                if packagesRemaining == 0 and len(package_locations) != 3:
                    reward = 500
                    
                #print("Current reward at {0} is {1}".format(state, reward))
                package_locations.update({gTypes[gridType]: nextState})
                if reward < 100:
                    reward = 100
                #print("Package of type {0} collected at {1} with reward {2}".format(gTypes[gridType],nextState, reward))
                packagesToCollect -= 1   
                #print("Agent took {0} action and moved to {1} of type {2}".format (action, nextState, gTypes[gridType]))
        else:
            reward -= 10
            #print("collision")
        
        rewards[state][action] = reward
        #if i == NUM_EPOCHS -1:
        #    print("Agent took {0} action and moved to {1}".format (action, nextState))
        cummulative_reward += reward
        q_learn(state, action, nextState) 
        
        
        if packagesRemaining == 0:
            #fourRoomsObj.showPath(-1, "image_{0}.png".format(i))
            return j+1, isTerminal
    
        state = nextState
        
    return MAX_ITERATIONS, False

bStochastic = False
if len(sys.argv) >= 2:
    if sys.argv[1] == "-stochastic":
        bStochastic = True

fourRoomsObj = FourRooms("multi", bStochastic)

NUM_EPOCHS = 1000
MAX_ITERATIONS = 5000

k = fourRoomsObj.getPackagesRemaining()
print("Packages to collect:", k)

(startX, startY) = fourRoomsObj.getPosition() 
print("Agent starts at: {0}".format((startX, startY)))

package_locations = {}
cummulative_reward = 0

count_success = 0
for i in range(NUM_EPOCHS):
    cummulative_reward = 0
    fourRoomsObj.newEpoch()
    print('Epoch {0}/{1}'.format(i+1, NUM_EPOCHS))
    
    #print("Epsilon greedy is {0}".format(exploration_rate))
    
    total_actions, isDone = train(i, fourRoomsObj, k)
    
    if isDone:
        count_success += 1
    
    #print("Is done:", isDone)
    
    print("Completed: ", isDone, ", Total actions taken:", total_actions)
    
    exploration_rate = max(min_exploration, exploration_rate * 0.99)
    
exploration_rate = exploitation # exploits the environment to test the learned policy

# print("Q function")
# for y in range(NUM_ROWS):
#     for x in range(NUM_COLS):
#         state = (x, y)
#         #print("Q-values at {0} is for actions: {1}".format((x,y), q_table[(x,y)]))
#         print("{:>6}".format(round(max(q_table[state]))), end=" ")
#     print("")
# print(q_table) 

#print("Rewards function")
# The reward function provides the representation of the observed environment
# for y in range(NUM_ROWS):
#     for x in range(NUM_COLS):
#         state = (x, y)
#         # print("Reward value at {0} is {1}".format((x,y), max(rewards[(x,y)])))
#         print("{:>6}".format(max(rewards[state])), end=" ")
#     print("")
# #print(rewards) 
print(package_locations)

fourRoomsObj.showPath(-1, "image_N.png")

print("Success rate is {0}/{1} which is {2}%".format(count_success, NUM_EPOCHS, (count_success / NUM_EPOCHS * 100) ))

# Display the agent's path to collect the package using 100% explotation
fourRoomsObj.newEpoch()
train(0, fourRoomsObj, k)
fourRoomsObj.showPath(-1, "image_N1.png")