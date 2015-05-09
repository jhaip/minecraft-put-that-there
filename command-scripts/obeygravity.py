from botchallenge import *
from pathfindingUtils import *
import sys

def obey_gravity(robot):
    move_to_ground(robot)
    message_all(robot, "I'm obeying gravity.")

robot = Robot(str(sys.argv[1]), "localhost")
obey_gravity(robot)

sys.exit() # make sure the program dies
