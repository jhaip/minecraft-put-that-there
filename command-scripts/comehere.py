from botchallenge import *
import sys

def come_here(robot):
    teleportThreshold = 50
    ownerLoc = robot.get_owner_location()
    initialDist = int(robot.get_location().distance(ownerLoc))
    if initialDist < teleportThreshold:
        robot.message_owner("I'm coming from " + str(initialDist) + " units away.")
        while robot.get_location().distance(ownerLoc) > 2:
            direction = robot.find_path(ownerLoc)
            robot.turn(direction)
            robot.move(direction)
    else:
        robot.message_owner("I'm teleporting from " + str(initialDist) + " units away.")
        destLoc = Location(103, 77, 94)
        print("teleporting to", destLoc)
        robot.teleport(destLoc)
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)
    robot.message_owner("I'm here!")

robot = Robot(str(sys.argv[1]), "localhost")
come_here(robot)

sys.exit() # make sure the program dies
