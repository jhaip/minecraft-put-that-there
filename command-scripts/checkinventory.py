from botchallenge import *
import sys

def check_inventory(robot, TARGET_LIST):
    print("*** STARTING CHECK_INVENTORY SCRIPT")

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    if len(locations) >= 1:
        robot.message_all("I found it nearby!")
    else:
        robot.message_all("I don't think there is any near here.")

    inventory = tuple_list_to_dict(robot.get_inventory())
    for blockType in TARGET_LIST:
        if blockType in inventory.keys():
            qty = inventory[blockType]
            robot.message_all("I have " + str(qty) + " "
                              + str(blockType) + " in my inventory.")
        else:
            robot.message_all("I don't have any "
                              + str(blockType) + " in my inventory.")

    print("done!")

def tuple_list_to_dict(tupleList):
    resultDict = {}
    for tup in tupleList:
        resultDict[tup[0]] = tup[1]
    return resultDict

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
check_inventory(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies

