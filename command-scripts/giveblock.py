from botchallenge import *
from pathfindingUtils import go_to_owner
import sys

def give_block(robot, TARGET_LIST):
    print("*** STARTING GIVE_BLOCK SCRIPT")

    here = False
    ownerLoc = robot.get_owner_location()
    initialDist = int(robot.get_location().distance(ownerLoc))
    if initialDist < 5:
        here = True
    
    inventory = tuple_list_to_dict(robot.get_inventory())
    for blockType in TARGET_LIST:
        blockStr = str(blockType)
        if blockStr in inventory.keys():
            if not here:
                teleportThreshold = 20
                go_to_owner(robot, teleportThreshold)
                here = True
            qty = inventory[blockStr]
            robot.message_all("Here is all of my " + blockStr.lower())
            robot.drop_item(blockType, qty)
        else:
            robot.message_all("I don't have any "
                              + blockStr.lower() + " in my inventory.")
    print("done!")

def tuple_list_to_dict(tupleList): #hash by string
    resultDict = {}
    for tup in tupleList:
        resultDict[str(tup[0])] = tup[1]
    return resultDict

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
give_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies



