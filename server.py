import tornado.ioloop
import tornado.web
import tornado.websocket
from botchallenge import *
import os
import sys

# from buildhut import build_house
from minetunnel import mine_tunnel
from gatherblock import gather_block
from findblock import find_block

import subprocess
import signal

class Actions:
    Build, Find, Get, Stop, Come, Hello, What = range(7)

class Objects:
    House, Tunnel, Tree, Coal, Dirt, Sand, Water, Stone, Iron, Diamond = range(10)

objToBlockTypes = {Objects.Tree: [BlockType.LOG, BlockType.LOG_2],
                          Objects.Coal: [BlockType.COAL_BLOCK, BlockType.COAL_ORE],
                          Objects.Dirt: [BlockType.DIRT, BlockType.GRASS],
                          Objects.Sand: [BlockType.SAND, BlockType.GRAVEL],
                          Objects.Water: [BlockType.WATER, BlockType.STATIONARY_WATER],
                          Objects.Stone: [BlockType.STONE, BlockType.COBBLESTONE],
                          Objects.Iron: [BlockType.IRON_ORE],
                          Objects.Diamond: [BlockType.DIAMOND_ORE, BlockType.DIAMOND_BLOCK]}

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


class Hello(tornado.websocket.WebSocketHandler):
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
            if message_has_substring(message, ["build","make"]):
                action = Actions.Build
            elif message_has_substring(message, ["find","search","look for"]):
                action = Actions.Find
            elif message_has_substring(message, ["get","gather","collect","cut","mine","pick","obtain","destroy","dig"]):
                action = Actions.Get
            elif message_has_substring(message, ["stop","quit"]):
                action = Actions.Stop
            elif message_has_substring(message, ["come"]):
                action = Actions.Come
            elif message_has_substring(message, ["hello","hi","hey","howdy"]):
                action = Actions.Hello
            elif message_has_substring(message, ["what"]):
                action = Actions.What
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
            elif message_has_substring(message, ["dirt","ground","grass","earth"]):
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
            else:
                obj = False

            # Making Jack do thing based on an action, obj combo
            if action is Actions.Build:
                if obj is Objects.House:
                    if proc is False:
                        proc = subprocess.Popen(['python3', 'buildhut.py', MINECRAFT_USERNAME])
                    else:
                        print("processing running already")
                    # thread.start_new_thread(build_house, (robot))
                    # robot.message_owner("Maybe I shouldn't build a house right now.")
                    #threading.Thread(target=build_house, args=(robot,)).start()
                    #print("CREATED NEW THREAD FOR BUILDING A HOUSE")
                if obj is Objects.Tunnel:
                    mine_tunnel(robot)
            if action is Actions.Find:
                if obj in objToBlockTypes:
                    find_block(robot, objToBlockTypes[obj])
            if action is Actions.Get:
                if obj in objToBlockTypes:
                    gather_block(robot, objToBlockTypes[obj])
            if action is Actions.Stop:
                os.kill(proc.pid, signal.SIGUSR1)
                proc = False
            if action is Actions.Come:
                ownerLoc = robot.get_owner_location()
                robot.message_owner("I'm coming from " + str(int(robot.get_location().distance(ownerLoc))) + " units away.")
                while robot.get_location().distance(ownerLoc) > 2:
                    direction = robot.find_path(ownerLoc)
                    robot.turn(direction)
                    robot.move(direction)
                while robot.get_block_type(Dir.DOWN) == BlockType.AIR:
                    robot.move(Dir.DOWN)
                robot.message_owner("I'm here!")
            if action is Actions.Hello:
                robot.message_all("Hello, I'm Jack!  Let's play Minecraft together!")
            if action is Actions.What:
                robot.message_all("I do the things you tell me to, such as build a house or find coal.")
            if action is Actions.Stop:
                stopit.stop = True

    def on_close(self):
        print("CLOSING SERVER")


class Main(tornado.web.RequestHandler):
    def get(self):
        # This could be a template, too.
        self.render("webspeechdemo.html")

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
    app.listen(8888)
    print("Starting Tornado Server at localhost:8888")
    tornado.ioloop.IOLoop.instance().start()
