from botchallenge import *
import sys

def find_block(robot, TARGET_LIST):
    print("*** STARTING FIND_BLOCK SCRIPT")

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    if len(locations) >= 1:
        robot.message_all("I found it nearby!")
    else:
        robot.message_all("I don't think there is any near here.")

    print("done!")

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [int(x) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
find_block(robot, TARGET_LIST_ARG)


