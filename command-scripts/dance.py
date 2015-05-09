from botchallenge import *
from pathfindingUtils import *
import sys
from random import randint

def do_something(robot):
    random_length = randint(1,5)
    for i in range(random_length):
        random_value = randint(0,3)
        if random_value == 0:
            robot.move(Dir.FORWARD)
            robot.move(Dir.BACKWARD)
            robot.move(Dir.BACKWARD)
            robot.move(Dir.FORWARD)
            robot.move(Dir.LEFT)
            robot.move(Dir.RIGHT)
            robot.move(Dir.RIGHT)
            robot.move(Dir.LEFT)
        elif random_value == 1:
            robot.turn(Dir.LEFT)
            speak()
            robot.turn(Dir.LEFT)
            speak()
            robot.turn(Dir.LEFT)
            speak()
            robot.turn(Dir.LEFT)
            speak()
        else:
            robot.move(Dir.UP)
            robot.move(Dir.DOWN)


robot = Robot(str(sys.argv[1]), "localhost")
do_something(robot)

sys.exit() # make sure the program dies
