"""
Builds a simple dirt hut to shelter you from the enemies at night.
"""
from botchallenge import *
from pathfindingUtils import *
from gatherUtils import *
import sys

def build_roof_or_floor(robot, size, place_direction, place_material):
    for y in range(size+1):
        if robot.is_block_solid(place_direction) is False:
            robot.place(place_direction, place_material)
        for x in range(size):
            mine_if_solid(robot, Dir.RIGHT)
            robot.move(Dir.RIGHT)
            if robot.is_block_solid(place_direction) is False:
                robot.place(place_direction, place_material)
        for x in range(size):
            robot.move(Dir.LEFT)
        if y < size:
            mine_if_solid(robot, Dir.BACKWARD)
            robot.move(Dir.BACKWARD)
    for y in range(size):
        robot.move(Dir.FORWARD)

def build_floor(robot, size):
    build_roof_or_floor(robot, size, Dir.DOWN, BlockType.DIRT)

def build_roof(robot, size):
    build_roof_or_floor(robot, size, Dir.UP, BlockType.COBBLESTONE)

def build_layer(robot, size):
    for i in range(4):
        if robot.is_block_solid(Dir.FORWARD) is False:
            robot.place(Dir.FORWARD, BlockType.COBBLESTONE) 
        for x in range(size):
            mine_if_solid(robot, Dir.RIGHT)
            robot.move(Dir.RIGHT)
            if robot.is_block_solid(Dir.FORWARD) is False:
                robot.place(Dir.FORWARD, BlockType.COBBLESTONE) 
        robot.turn(Dir.RIGHT)

    robot.move(Dir.RIGHT)
    mine_if_solid(robot, Dir.BACKWARD)
    robot.move(Dir.BACKWARD)

    for y in range(size-2):
        for x in range(size-3):
            mine_if_solid(robot, Dir.RIGHT)
            robot.move(Dir.RIGHT)
        for x in range(size-3):
            robot.move(Dir.LEFT)
        mine_if_solid(robot, Dir.BACKWARD)
        robot.move(Dir.BACKWARD)

    robot.move(Dir.LEFT)
    for y in range(size-1):
        robot.move(Dir.FORWARD)

def build_house(robot):
    print("*** STARTING BUILD_HOUSE SCRIPT")

    # go back to the ground, we don't want floating houses
    while (robot.is_block_solid(Dir.DOWN) is False):
        robot.move(Dir.DOWN)

    size = 5 # building a 5x5 house
    height = 3 # blocks height inside

    build_floor(robot, size) # the floor

    # build the walls and clear out the center
    for i in range(height):
        build_layer(robot, size)
        if i < height-1:
            mine_if_solid(robot, Dir.UP)
            robot.move(Dir.UP)

    build_roof(robot, size) # the roof

    # go back to the ground
    while (robot.is_block_solid(Dir.DOWN) is False):
        robot.move(Dir.DOWN)

    # make a door
    robot.move(Dir.RIGHT)
    robot.move(Dir.UP)
    robot.mine(Dir.FORWARD)
    robot.move(Dir.DOWN)
    robot.mine(Dir.FORWARD)

    message_all(robot, "Our home is ready!")
    print("done!")

robot = Robot(str(sys.argv[1]), "localhost")
build_house(robot)

sys.exit() # make sure the program dies


