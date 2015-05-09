"""
Go there, then gather block.
"""
from botchallenge import *
from gatherUtils import *
import sys

TARGET_LIST_ARG = str(sys.argv[2])
TARGET_LIST_ARG = TARGET_LIST_ARG[1:-1]
TARGET_LIST_ARG = TARGET_LIST_ARG.split(',')
TARGET_LIST_ARG = [x[:-1].split('(') for x in TARGET_LIST_ARG]
TARGET_LIST_ARG = [BlockType(x[0], int(x[1])) for x in TARGET_LIST_ARG]

robot = Robot(str(sys.argv[1]), "localhost")
go_there(robot, 20)
gather_block(robot, TARGET_LIST_ARG)

sys.exit() # make sure the program dies
