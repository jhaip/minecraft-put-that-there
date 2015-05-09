from botchallenge import *
from pathfindingUtils import *
import sys

def place_block(robot, TARGET_LIST):
    print("*** STARTING PLACE_BLOCK SCRIPT")
    print(TARGET_LIST)
    
    inventory = tuple_list_to_dict(robot.get_inventory())
    placed_something = False
    for blockType in TARGET_LIST:
        blockStr = str(blockType)
        if blockStr in inventory.keys():
            robot.mine(Dir.FORWARD)
            robot.place(Dir.FORWARD, blockType)
            placed_something = True
    if placed_something is False:
        message_all(robot, "I don't have any " + blockStr.lower()
                    + " in my inventory.")
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
place_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies



