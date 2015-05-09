from botchallenge import *
import random
import subprocess

def go_to_owner(robot, teleportThreshold):
    ownerLoc = robot.get_owner_location()
    initialDist = int(robot.get_location().distance(ownerLoc))
    if initialDist < teleportThreshold:
        message_all(robot, "I'm coming from " + str(initialDist) + " units away.")
        walk_toward_location(robot, ownerLoc, 2)
    else:
        maxDestRadius = 3
        destLoc = find_air_near(robot, ownerLoc, maxDestRadius)
        if destLoc == None:
            message_all(robot, "I can't find space near you to teleport.")
            return
        message_all(robot, "I'm teleporting from " + str(initialDist) + " units away.")
        robot.teleport(destLoc)
        face_owner(robot)
    message_all(robot, "I'm here!")

def walk_toward_location(robot, destLoc, radius):
    while robot.get_location().distance(destLoc) > radius:
        direction = robot.find_path(destLoc)
        robot.turn(direction)
        robot.move(direction)

def face_owner(robot):
    face_location(robot, robot.get_owner_location())

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

def speak():
    num = random.randint(1,3)
    audio_file = "sounds/voice-short-"+str(num)+".wav"
    return_code = subprocess.call(["afplay", audio_file])

def message_all(robot, text):
    speak()
    robot.message_all(text)
