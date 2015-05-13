"""
Mines a set of stairs 2 blocks wide going down in whatever direction the bot
is facing when it starts.
"""

from botchallenge import *
from gatherUtils import *
import sys

END_LAYER = int(sys.argv[2])

TARGET_LIST_ARG = str(sys.argv[3])
if TARGET_LIST_ARG == "[]": # to handle cases were we aren't looking for a target block
    TARGET_LIST_ARG = []
else:
    TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
    TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
    TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
    TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
mine_tunnel(robot, END_LAYER, TARGET_LIST_ARG)

sys.exit() # make sure the program dies
