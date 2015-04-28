from botchallenge import *
from pathfindingUtils import *
import sys

def go_there(robot):
    teleportThreshold = 50
    thereLoc = robot.get_owner_target_block()
    initialDist = int(robot.get_location().distance(thereLoc))
    if initialDist < teleportThreshold:
        robot.message_owner("I'm going over there.")
        walk_toward_location(robot, thereLoc, 1)
    else:
        destLoc = find_air_near(robot, thereLoc)
        if destLoc == None:
            robot.message_owner("I can't find space to teleport there.")
            return
        robot.message_owner("I'm teleporting over there.")
        robot.teleport(destLoc)
    move_to_ground(robot)

    robot.message_owner("I've arrived!")

robot = Robot(str(sys.argv[1]), "localhost")
go_there(robot)

sys.exit() # make sure the program dies
