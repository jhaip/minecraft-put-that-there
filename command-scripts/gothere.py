from botchallenge import *
from pathfindingUtils import *
import sys

def go_there(robot, teleportThreshold):
    thereLoc = robot.get_owner_target_block()
    initialDist = int(robot.get_location().distance(thereLoc))
    if initialDist < teleportThreshold:
        message_all(robot, "I'm going over there.")
        walk_toward_location(robot, thereLoc, 1)
    else:
        destLoc = find_air_near(robot, thereLoc)
        if destLoc == None:
            message_all(robot, "I can't find space to teleport there.")
            return
        message_all(robot, "I'm teleporting over there.")
        robot.teleport(destLoc)
    move_to_ground(robot)
    message_all(robot, "I've arrived!")

robot = Robot(str(sys.argv[1]), "localhost")

if len(sys.argv) > 2:
    teleportThreshold = int(sys.argv[2])
else:
    teleportThreshold = 50

go_there(robot, teleportThreshold)

sys.exit() # make sure the program dies
