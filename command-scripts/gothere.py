from botchallenge import *
from pathfindingUtils import *
import sys

robot = Robot(str(sys.argv[1]), "localhost")

if len(sys.argv) > 2:
    teleportThreshold = int(sys.argv[2])
else:
    teleportThreshold = 50

go_there(robot, teleportThreshold)
move_to_ground(robot)
message_all(robot, "I've arrived!")

sys.exit() # make sure the program dies
