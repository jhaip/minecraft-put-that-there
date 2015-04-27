"""
Mines a set of stairs 2 blocks wide going down in whatever direction the bot
is facing when it starts.
"""

from botchallenge import *
import sys

def mine_if_solid(robot, direction):
    """Mines the block only if it's a solid block (won't mine torches away)."""
    is_solid = robot.is_block_solid(direction)
    if is_solid:
        robot.mine(direction)

def flatten_layer(robot, side_length, backwards):
    order = range(1,side_length)
    if backwards:
        order = order[::-1]
        robot.turn(Dir.LEFT)
    for i in order:
        repeat = 3 if (i == side_length-1) else 2
        for k in range(repeat):
            for x in range(i):
                mine_if_solid(robot, Dir.FORWARD)
                robot.move(Dir.FORWARD)
            if backwards:
                robot.turn(Dir.RIGHT)
            else:
                robot.turn(Dir.LEFT)
    print("level clear")

def flatten(robot, side_length, height):
    backwards = False
    for i in range(height):
        flatten_layer(robot, side_length, backwards)
        mine_if_solid(robot, Dir.UP)
        robot.move(Dir.UP)
        backwards = not backwards
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)
    speak()
    robot.message_all("All clear!")

robot = Robot(str(sys.argv[1]), "localhost")
flatten(robot, 5, 4)

sys.exit() # make sure the program dies
