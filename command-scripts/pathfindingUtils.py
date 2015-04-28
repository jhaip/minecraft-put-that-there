from botchallenge import *

def go_to_owner(robot, teleportThreshold):
    ownerLoc = robot.get_owner_location()
    initialDist = int(robot.get_location().distance(ownerLoc))
    if initialDist < teleportThreshold:
        robot.message_owner("I'm coming from " + str(initialDist) + " units away.")
        walk_toward_location(robot, ownerLoc, 2)
    else:
        maxDestRadius = 3
        destLoc = find_air_near(robot, ownerLoc, maxDestRadius)
        if destLoc == None:
            robot.message_owner("I can't find space near you to teleport.")
            return
        robot.message_owner("I'm teleporting from " + str(initialDist) + " units away.")
        robot.teleport(destLoc)
        face_location(robot, ownerLoc)
    move_to_ground(robot)
    robot.message_owner("I'm here!")

def walk_toward_location(robot, destLoc, radius):
    while robot.get_location().distance(destLoc) > radius:
        direction = robot.find_path(destLoc)
        robot.turn(direction)
        robot.move(direction)

def face_location(robot, destLoc):
    direction = robot.find_path(destLoc)
    robot.turn(direction)

def move_to_ground(robot):
    while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
        robot.move(Dir.DOWN)    

def find_air_near(robot, loc, maxRadius=3): #inefficient (todo)
    for r in range(1, maxRadius + 1):
        for x in range(loc.x_coord - r, loc.x_coord + r+1):
            for y in range(loc.y_coord, loc.y_coord + r+1):
                for z in range(loc.z_coord - r, loc.z_coord + r+1):
                    newLoc = Location(x, y, z)
                    if robot.get_block_type_at(newLoc) == BlockType.AIR:
                        return newLoc
    return None
