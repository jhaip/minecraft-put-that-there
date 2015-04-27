from botchallenge import *
import sys

def go_there(robot):
    teleportThreshold = 50
    thereLoc = robot.get_owner_target_block()
    initialDist = int(robot.get_location().distance(thereLoc))
    if initialDist < teleportThreshold:
        robot.message_owner("I'm going over there.")
        while robot.get_location().distance(thereLoc) > 1:
            direction = robot.find_path(thereLoc)
            robot.turn(direction)
            robot.move(direction)        
    else:
        maxRadius = 3
        destLoc = find_air_near(robot, thereLoc, maxRadius)
        if destLoc == None:
            robot.message_owner("I can't find space to teleport there.")
            print("teleportation failed with maxRadius", maxRadius)
            return
        robot.message_owner("I'm teleporting over there.")
        print("teleporting to", destLoc)
        robot.teleport(destLoc)
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)

    robot.message_owner("I've arrived!")

def find_air_near(robot, loc, maxRadius): #inefficient (todo)
    for r in range(1, maxRadius + 1):
        for x in range(loc.x_coord - r, loc.x_coord + r+1):
            for y in range(loc.y_coord, loc.y_coord + r+1):
                for z in range(loc.z_coord - r, loc.z_coord + r+1):
                    newLoc = Location(x, y, z)
                    if robot.get_block_type_at(newLoc) == BlockType.AIR:
                        return newLoc
    return None

robot = Robot(str(sys.argv[1]), "localhost")
go_there(robot)

sys.exit() # make sure the program dies
