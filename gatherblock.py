"""
Example robot which finds trees and gathers wood.
"""
from botchallenge import *

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



