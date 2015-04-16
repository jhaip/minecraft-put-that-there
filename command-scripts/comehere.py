from botchallenge import *
import sys

def come_here(robot):
    ownerLoc = robot.get_owner_location()
    robot.message_owner("I'm coming from " + str(int(robot.get_location().distance(ownerLoc))) + " units away.")
    while robot.get_location().distance(ownerLoc) > 2:
        direction = robot.find_path(ownerLoc)
        robot.turn(direction)
        robot.move(direction)
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)
    robot.message_owner("I'm here!")

robot = Robot(str(sys.argv[1]), "localhost")
come_here(robot)

sys.exit() # make sure the program dies