"""
Example robot which finds trees and gathers wood.
"""
from botchallenge import *
import sys

def gather_block(robot, TARGET_LIST):
    print("*** STARTING GATHER_BLOCK SCRIPT")

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    limit1 = 0
    while len(locations) > 0 and limit1 < 20:
        limit1 += 1
        location = locations[0]
        block_type = robot.get_block_type(robot.get_location().direction(location))
        limit2 = 0
        while block_type not in TARGET_LIST and limit2 < 20:
            limit2 += 1
            robot.move(robot.find_path(location))
            robot.turn(robot.get_location().direction(location))
            block_type = robot.get_block_type(robot.get_location().direction(location))
        robot.mine(robot.get_location().direction(location))
        locations = []
        for t in TARGET_LIST:
            locations += robot.find_type_nearby(t)

    robot.message_all("I'm done gathering!")
    print("done!")

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
gather_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies



