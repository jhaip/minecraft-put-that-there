from botchallenge import *
from pathfindingUtils import *
import sys

def gather_block(robot, TARGET_LIST):
    print("*** STARTING GATHER_BLOCK SCRIPT")
    startLocation = robot.get_location()

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    if len(locations) == 0:
        message_all(robot, "I didn't find any.")
        return

    def coordDist(x):
        return int(x.distance(startLocation))

    locations.sort(key=coordDist)

    limit1 = 0
    while len(locations) > 0 and limit1 < 20000:
        limit1 += 1
        location = locations[0]
        block_type = robot.get_block_type(robot.get_location().direction(location))
        pathfinding_locations = []
        while block_type not in TARGET_LIST:
            robot.move(robot.find_path(location))
            if len(pathfinding_locations) > 3 and pathfinding_locations[-2] == robot.get_location():
                message_all(robot, "I got stuck so I gave up. :(")
                return
            pathfinding_locations.append(robot.get_location())
            robot.turn(robot.get_location().direction(location))
            block_type = robot.get_block_type(robot.get_location().direction(location))
        robot.mine(robot.get_location().direction(location))
        locations = []
        for t in TARGET_LIST:
            locations += robot.find_type_nearby(t)
        locations.sort(key=coordDist)
    message_all(robot, "I'm done gathering!")
    print("done!")

def mine_if_solid(robot, direction):
    """Mines the block only if it's a solid block (won't mine torches away)."""
    is_solid = robot.is_block_solid(direction)
    if is_solid:
        robot.mine(direction)

def touching_target_block(robot, TARGET_LIST):
    if robot.get_block_type(Dir.FORWARD) in TARGET_LIST:
        return True
    if robot.get_block_type(Dir.BACKWARD) in TARGET_LIST:
        return True
    if robot.get_block_type(Dir.LEFT) in TARGET_LIST:
        return True
    if robot.get_block_type(Dir.RIGHT) in TARGET_LIST:
        return True
    if robot.get_block_type(Dir.UP) in TARGET_LIST:
        return True
    if robot.get_block_type(Dir.DOWN) in TARGET_LIST:
        return True
    return False

def mine_tunnel(robot, END_LAYER, TARGET_LIST):
    print("*** STARTING MINE_TUNNEL SCRIPT")
    print(robot.get_location().y_coord)
    print(END_LAYER)
    while robot.get_location().y_coord > END_LAYER:

        mine_if_solid(robot, Dir.FORWARD)
        robot.move(Dir.FORWARD)

        if touching_target_block(robot, TARGET_LIST):
            print("Found target block during mining -- stopping mining.")
            return True

        # Clear space above and below
        mine_if_solid(robot, Dir.DOWN)
        mine_if_solid(robot, Dir.UP)
        
        # Mine and move right
        mine_if_solid(robot, Dir.RIGHT)
        robot.move(Dir.RIGHT)

        if touching_target_block(robot, TARGET_LIST):
            print("Found target block during mining -- stopping mining.")
            return True

        # Clear space above and below
        mine_if_solid(robot, Dir.DOWN)
        mine_if_solid(robot, Dir.UP)
        
        # Move left + down
        mine_if_solid(robot, Dir.LEFT)
        robot.move(Dir.LEFT)
        mine_if_solid(robot, Dir.DOWN)
        robot.move(Dir.DOWN)

        if touching_target_block(robot, TARGET_LIST):
            print("Found target block during mining -- stopping mining.")
            return True

    return False # didn't find target block on the way down

    message_all(robot, "Tunnel complete!")
    print("done!")

def strip_mine(robot, TARGET_LIST):
    print("*** STARTING TO STRIP MINE")
    for j in range(10):
        print("mining another strip")
        for i in range(20):
            mine_if_solid(robot, Dir.FORWARD)
            robot.move(Dir.FORWARD)
            if touching_target_block(robot, TARGET_LIST):
                print("Found target block during mining -- stopping mining.")
                return True
        for i in range(20):
            mine_if_solid(robot, Dir.BACKWARD)
            robot.move(Dir.BACKWARD)
        for i in range(3):
            mine_if_solid(robot, Dir.LEFT)
            robot.move(Dir.LEFT)
            if touching_target_block(robot, TARGET_LIST):
                print("Found target block during mining -- stopping mining.")
                return True
    return False