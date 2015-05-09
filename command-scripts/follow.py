from botchallenge import *
from pathfindingUtils import *
import sys

def follow(robot):
    teleportThreshold = 30
    followDist = 3
    while True:
        ownerLoc = robot.get_owner_location()
        dist = int(robot.get_location().distance(ownerLoc))
        if dist > followDist:
            if dist < teleportThreshold:
                walk_toward_location(robot, ownerLoc, followDist)
            else:
                maxDestRadius = 3
                destLoc = find_air_near(robot, ownerLoc, maxDestRadius)
                if destLoc is not None:
                    robot.teleport(destLoc)
            face_owner(robot)

robot = Robot(str(sys.argv[1]), "localhost")
follow(robot)

sys.exit() # make sure the program dies
