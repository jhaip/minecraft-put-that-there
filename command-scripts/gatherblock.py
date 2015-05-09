from botchallenge import *
from gatherUtils import *
from pathfindingUtils import *
import sys

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")

if BlockType.COAL_ORE in TARGET_LIST_ARG or \
   BlockType.IRON_ORE in TARGET_LIST_ARG or \
   BlockType.DIAMOND_ORE in TARGET_LIST_ARG:
    message_all(robot, "I'm going to dig a tunnel to find it.")
    found_target_block_during_mining = mine_tunnel(robot, 15, TARGET_LIST_ARG)
    if found_target_block_during_mining:
        message_all(robot, "I found some!")
        gather_block(robot, TARGET_LIST_ARG)
    else:
        message_all(robot, "Didn't find any as I was digging the tunnel.")
        message_all(robot, "I'm going to start strip mining")
        found_target_block_during_strip_mining = strip_mine(robot, TARGET_LIST_ARG)
        if found_target_block_during_strip_mining:
            message_all(robot, "I found some!")
            gather_block(robot, TARGET_LIST_ARG)
        else:
            message_all(robot, "Didn't find any as I was strip mining.  I give up!")
else:
    gather_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies



