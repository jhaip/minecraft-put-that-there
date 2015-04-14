from botchallenge import *

def find_block(robot, TARGET_LIST):
    print("*** STARTING FIND_BLOCK SCRIPT")

    locations = []
    for t in TARGET_LIST:
        locations += robot.find_type_nearby(t)
    print(locations)

    if len(locations) >= 1:
        robot.message_all("I found it nearby!")
    else:
        robot.message_all("I don't think there is any near here.")

    print("done!")