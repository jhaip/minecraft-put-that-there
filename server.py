import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.httpserver
from botchallenge import *
import os
import sys
import subprocess
import signal
import ssl

class Actions:
    [Build, Get, Stop, Come, Hello, What, Where, Why, Flatten,
     CheckInventory] = range(10)

class Objects:
    [House, Tunnel, Tree, Coal, Dirt, Sand, Water, Stone, Iron,
     Diamond, Grass, Inventory, Jack, That] = range(14)

objToBlockTypes = {Objects.Tree: [BlockType.LOG, BlockType.LOG_2],
                          Objects.Coal: [BlockType.COAL_BLOCK, BlockType.COAL_ORE],
                          Objects.Dirt: [BlockType.DIRT, BlockType.GRASS],
                          Objects.Sand: [BlockType.SAND, BlockType.GRAVEL],
                          Objects.Water: [BlockType.WATER, BlockType.STATIONARY_WATER],
                          Objects.Stone: [BlockType.STONE, BlockType.COBBLESTONE],
                          Objects.Iron: [BlockType.IRON_ORE],
                          Objects.Diamond: [BlockType.DIAMOND_ORE, BlockType.DIAMOND_BLOCK],
                          Objects.House: [BlockType.COBBLESTONE],
                          Objects.Grass: [BlockType.LONG_GRASS]}

action = False
obj = False

robot = None
robot_ready = False

proc = False

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
        proc = False
else:
    print("No Minecraft username given - skipping connection to server")


def message_has_substring(message, substring_list):
    return any(substr in message for substr in substring_list)

def run_new_command(command_line_array):
    global proc
    if proc is not False:
        print("found a command already running in the background")
        proc.terminate()
        proc.wait()
        print("It's killed now")
    command_line_array[0] = "command-scripts/"+command_line_array[0]
    command_line_array = ['python3']+command_line_array
    proc = subprocess.Popen(command_line_array)


class Hello(tornado.websocket.WebSocketHandler):
    def check_origin(self, origin):
        # allow any websockets connections to connect
        return True

    def open(self):
        self.write_message("Hello web page")
        print("Said hello to the web page")

    def on_message(self, message):
        global proc
        print("Received message: '"+message+"'")
        if robot_ready:
            robot.message_all(message)
            if "down" in message:
                robot.move(Dir.DOWN)
            if "up" in message:
                robot.move(Dir.UP)
            if "left" in message:
                robot.move(Dir.LEFT)
            if "right" in message:
                robot.move(Dir.RIGHT)
            if "forward" in message:
                robot.move(Dir.FORWARD)
            if "backward" in message or "back" in message:
                robot.move(Dir.BACKWARD)
                
            # Detecting Action
            action = False
            if message_has_substring(message, ["stop","quit"]):
                action = Actions.Stop
            elif message_has_substring(message, ["where"]):
                action = Actions.Where
            elif message_has_substring(message, ["what"]):
                action = Actions.What
            elif message_has_substring(message, ["why"]):
                action = Actions.Why
            elif message_has_substring(message, ["build","make"]):
                action = Actions.Build
            elif message_has_substring(message, ["find","search","look for","get","gather","collect","cut","mine","pick","obtain","destroy","dig","chop"]):
                action = Actions.Get
            elif message_has_substring(message, ["come"]):
                action = Actions.Come
            elif message_has_substring(message, ["hello","hi","hey","howdy","high"]):
                action = Actions.Hello
            elif message_has_substring(message, ["flat","clear"]):
                action = Actions.Flatten
            elif message_has_substring(message, ["do you have","inventory","how much"]):
                action = Actions.CheckInventory
            else:
                action = False

            # Detecting object
            obj = False
            if message_has_substring(message, ["house","hut","shelter","place to sleep","fort","home","building","structure"]):
                obj = Objects.House
            elif message_has_substring(message, ["tunnel","cave"]):
                obj = Objects.Tunnel
            elif message_has_substring(message, ["tree","wood","log"]):
                obj = Objects.Tree
            elif message_has_substring(message, ["coal","goal","cool"]):
                obj = Objects.Coal
            elif message_has_substring(message, ["dirt","ground","earth"]):
                obj = Objects.Dirt
            elif message_has_substring(message, ["sand"]):
                obj = Objects.Sand
            elif message_has_substring(message, ["water"]):
                obj = Objects.Water
            elif message_has_substring(message, ["stone","rock","mountain","gray","grey"]):
                obj = Objects.Stone
            elif message_has_substring(message, ["iron"]):
                obj = Objects.Iron
            elif message_has_substring(message, ["diamond"]):
                obj = Objects.Diamond
            elif message_has_substring(message, ["grass","weed"]):
                obj = Objects.Grass
            elif message_has_substring(message, ["inventory"]):
                obj = Objects.Inventory
            elif message_has_substring(message, ["this","that","those","these","there"]):
                obj = Objects.That
            elif message_has_substring(message, ["you","Jack"]): #keep this last
                obj = Objects.Jack
            else:
                obj = False

            # Making Jack do thing based on an action, obj combo
            if action is Actions.Build:
                if obj is Objects.House:
                    run_new_command(['buildhut.py', MINECRAFT_USERNAME])
                if obj is Objects.Tunnel:
                    run_new_command(['minetunnel.py', MINECRAFT_USERNAME])
                else:
                    robot.message_owner("I don't know how to build that.")
            if action is Actions.Get:
                if obj in objToBlockTypes:
                    run_new_command(['gatherblock.py', 
                                    MINECRAFT_USERNAME, 
                                    str(objToBlockTypes[obj]).replace(' ','')])
            if action is Actions.Stop:
                if proc is not False:
                    proc.terminate() # if not forceful enough use .kill()
                    proc.wait()
                    proc = False
            if action is Actions.Come:
                run_new_command(['comehere.py', MINECRAFT_USERNAME])
            if action is Actions.Hello:
                robot.message_all("Hello, I'm Jack!  Let's play Minecraft together!")
            if action is Actions.What:
                if obj is Objects.Inventory:
                    Utilities.get_inventory(robot)
                if obj is Objects.Jack:
                    robot.message_all("I do the things you tell me to, such as build a house or find coal.")
                if obj is Objects.That:
                    owner_target_block = robot.get_owner_target_block()
                    owner_target_block_type = robot.get_block_type_at(owner_target_block)
                    if owner_target_block_type is not None:
                        owner_target_block_type_str = str(owner_target_block_type).replace("_","").lower().replace("stationary","")
                        if owner_target_block_type_str[-1] in "0123456789":
                            owner_target_block_type_str = owner_target_block_type_str[:-1]
                        if owner_target_block_type_str == "pumpkin":
                            if owner_target_block == robot.get_location():
                                owner_target_block_type_str = "me"
                            else:
                                owner_target_block_type_str = "my cousin"
                        robot.message_owner("That is "+owner_target_block_type_str)
            if action is Actions.Where:
                if obj is Objects.Jack:
                    dist = round(robot.get_location().distance(robot.get_owner_location()), 2)
                    robot.message_all("I am " + str(dist) + " units away from you.")
            if action is Actions.Why:
                robot.message_all("I don't know why.")
            if action is Actions.CheckInventory:
                if obj in objToBlockTypes:
                    run_new_command(['checkinventory.py', 
                                    MINECRAFT_USERNAME, 
                                    str(objToBlockTypes[obj]).replace(' ','')])
                else:
                    Utilities.get_inventory(robot)
            if action is Actions.Flatten:
                run_new_command(['flatten.py', MINECRAFT_USERNAME])

    def on_close(self):
        print("CLOSING SERVER")

class Utilities:
    def get_inventory(robot):
        inventoryItems = [str(key).lower() for (key, val) in robot.get_inventory()]
        robot.message_all("In my inventory, I have: "
                          + str(inventoryItems).strip('[').strip(']').replace("'", ""))

class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render("index.html")

class Application(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True, 
            'static_path': os.path.join(os.path.dirname(__file__), 'static')
        }
        handlers = [
            (r"/", Main),
            (r"/websocket", Hello),
        ]
        tornado.web.Application.__init__(self, handlers, **settings)

if __name__ == "__main__":
    app = Application()
    data_dir = os.path.dirname(__file__)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(8888)
    print("Starting Tornado Server at localhost:8888")
    tornado.ioloop.IOLoop.instance().start()
