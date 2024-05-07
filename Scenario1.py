from FourRooms import FourRooms
import numpy as np

NUM_ROWS = 13
NUM_COLS = 13

observed_env = np.zeros((NUM_COLS, NUM_ROWS))

MOVES = [FourRooms.UP, FourRooms.DOWN, FourRooms.LEFT, FourRooms.RIGHT]

FourRooms_obj = FourRooms("simple")
print("Agent starts at: {0}".format(FourRooms_obj.getPosition()))

FourRooms_obj.showPath(-1, "image_0.png")