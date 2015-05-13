from botchallenge import *
from pathfindingUtils import *
import sys

def come_here(robot):
    print("*** In come here script")
    teleportThreshold = 50
    go_to_owner(robot, teleportThreshold)

robot = Robot(str(sys.argv[1]), "localhost")
come_here(robot)

sys.exit() # make sure the program dies
