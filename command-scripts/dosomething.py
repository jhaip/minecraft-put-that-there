from botchallenge import *
from pathfindingUtils import *
import sys
from random import randint

def mine_if_solid(robot, direction):
    """Mines the block only if it's a solid block (won't mine torches away)."""
    is_solid = robot.is_block_solid(direction)
    if is_solid:
        robot.mine(direction)

def do_something(robot):
    random_value = randint(0,3)
    speak()
    if random_value == 0:
        mine_if_solid(robot, Dir.DOWN)
        robot.move(Dir.DOWN)

        mine_if_solid(robot, Dir.FORWARD)
        robot.move(Dir.FORWARD)
        mine_if_solid(robot, Dir.LEFT)
        robot.place(Dir.LEFT, BlockType.COBBLESTONE)
        mine_if_solid(robot, Dir.RIGHT)
        robot.place(Dir.RIGHT, BlockType.COBBLESTONE)

        robot.move(Dir.BACKWARD)
        mine_if_solid(robot, Dir.LEFT)
        robot.place(Dir.LEFT, BlockType.COBBLESTONE)
        mine_if_solid(robot, Dir.RIGHT)
        robot.place(Dir.RIGHT, BlockType.COBBLESTONE)

        mine_if_solid(robot, Dir.BACKWARD)
        robot.move(Dir.BACKWARD)
        mine_if_solid(robot, Dir.LEFT)
        robot.place(Dir.LEFT, BlockType.COBBLESTONE)
        mine_if_solid(robot, Dir.RIGHT)
        robot.place(Dir.RIGHT, BlockType.COBBLESTONE)

        robot.move(Dir.FORWARD)
        robot.place(Dir.FORWARD, BlockType.COBBLESTONE)
        robot.place(Dir.BACKWARD, BlockType.COBBLESTONE)

        robot.move(Dir.UP)
        robot.place(Dir.DOWN, BlockType.COBBLESTONE)
        speak()
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
