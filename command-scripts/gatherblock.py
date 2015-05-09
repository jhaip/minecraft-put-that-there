"""
Example robot which finds trees and gathers wood.
"""
from botchallenge import *
from pathfindingUtils import *
import sys

def gather_block(robot, TARGET_LIST):
    print("*** STARTING GATHER_BLOCK SCRIPT")
    startLocation = robot.get_location()

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    if len(locations) == 0:
        message_all(robot, "I didn't find any.")
        return

    def coordDist(x):
        return int(x.distance(startLocation))

    locations.sort(key=coordDist)

    limit1 = 0
    while len(locations) > 0 and limit1 < 20000:
        limit1 += 1
        location = locations[0]
        block_type = robot.get_block_type(robot.get_location().direction(location))
        pathfinding_locations = []
        while block_type not in TARGET_LIST:
            robot.move(robot.find_path(location))
            if len(pathfinding_locations) > 3 and pathfinding_locations[-2] == robot.get_location():
                message_all(robot, "I got stuck so I gave up. :(")
                return
            pathfinding_locations.append(robot.get_location())
            robot.turn(robot.get_location().direction(location))
            block_type = robot.get_block_type(robot.get_location().direction(location))
        robot.mine(robot.get_location().direction(location))
        locations = []
        for t in TARGET_LIST:
            locations += robot.find_type_nearby(t)
        locations.sort(key=coordDist)
    message_all(robot, "I'm done gathering!")
    print("done!")

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
gather_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies



