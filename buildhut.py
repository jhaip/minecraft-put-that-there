"""
Builds a simple dirt hut to shelter you from the enemies at night.
"""
from botchallenge import *
import sys

print("INSIDE BUILD HUT")

robot = None
robot_ready = False

if len(sys.argv) == 2:
    MINECRAFT_USERNAME = str(sys.argv[1])
    MINECRAFT_SERVER = "localhost"
    try:
        robot = Robot(MINECRAFT_USERNAME, MINECRAFT_SERVER)
    except:
        print("")
        print("WARNING: Could not connect to Minecraft server")
        print("Did you really want to connect as "+MINECRAFT_USERNAME+" to the server at "+MINECRAFT_SERVER+"?")
        print("And make sure the Modified Bukkit Server is running!")
    else:
        robot_ready = True
        print("SUCCESS: Connected to Minecraft Server at "+MINECRAFT_SERVER+" with username "+MINECRAFT_USERNAME)
else:
    print("No Minecraft username given - skipping connection to server")


hut_layout = """
 xxxxx 
x     x
x     x
x     x
x     x
x     x
 xx xx 
"""
hut_layout_2 = """
 xxxxx 
x     x
x     x
x     x
x     x
x     x
 xxxxx 
"""
hut_layout_roof = """
  xxx  
 xxxxx 
xxxxxxx
xxxxxxx
xxxxxxx
 xxxxx 
  xxx  
"""

def build_layer(robot, layer):
    # Move up one so we're placing the blocks downward
    robot.move(Dir.UP)
    lines = layer.split("\n")
    num_lines = len(lines)
    print("There are", num_lines, "lines")
    for line in lines:
        line_len = len(line)
        for char in line:
            if char == "x":
                robot.place(Dir.DOWN, BlockType.COBBLESTONE)
            robot.move(Dir.LEFT)
        # End of the line, go back to the beginning for the next line
        for i in range(line_len):
            robot.move(Dir.RIGHT)
        robot.move(Dir.FORWARD)
    # End of the layer, go back to the start position
    for l in range(num_lines):
        robot.move(Dir.BACKWARD)


def build_house(robot):
    print("*** STARTING BUILD_HOUSE SCRIPT")
    for layer in range(2):
        build_layer(robot, hut_layout)

    build_layer(robot, hut_layout_2)
    build_layer(robot, hut_layout_roof)
    robot.message_all("Our home is ready!")
    print("done!")

if robot_ready is True:
    build_house(robot)


