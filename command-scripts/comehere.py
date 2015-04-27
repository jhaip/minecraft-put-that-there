from botchallenge import *
import sys

def come_here(robot):
    teleportThreshold = 50
    ownerLoc = robot.get_owner_location()
    initialDist = int(robot.get_location().distance(ownerLoc))
    if initialDist < teleportThreshold:
        speak()
        robot.message_owner("I'm coming from " + str(initialDist) + " units away.")
        while robot.get_location().distance(ownerLoc) > 2:
            direction = robot.find_path(ownerLoc)
            robot.turn(direction)
            robot.move(direction)
    else:
        maxRadius = 3
        destLoc = find_air_near(robot, ownerLoc, maxRadius)
        if destLoc == None:
            speak()
            robot.message_owner("I can't find space near you to teleport.")
            print("teleportation failed with maxRadius", maxRadius)
            return
        speak()
        robot.message_owner("I'm teleporting from " + str(initialDist) + " units away.")
        print("teleporting to", destLoc)
        robot.teleport(destLoc)
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)
    speak()
    robot.message_owner("I'm here!")

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
come_here(robot)

sys.exit() # make sure the program dies
